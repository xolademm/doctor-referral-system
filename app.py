from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database import db, init_app
from models import User, Doctor, Patient, Referral, Message, bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize app
app = init_app()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super_secret_key')

# ----------------------
# JWT Configuration
# ----------------------
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super_jwt_secret_key')
app.config['JWT_TOKEN_LOCATION'] = ['headers']  
app.config['JWT_HEADER_NAME'] = 'Authorization'  
app.config['JWT_HEADER_TYPE'] = 'Bearer'  
jwt = JWTManager(app)


@jwt.invalid_token_loader
def invalid_token_callback(error):
    print("Invalid token error:", error)
    return jsonify({"error": "Invalid token", "details": str(error)}), 422

@jwt.unauthorized_loader
def unauthorized_callback(error):
    print("Unauthorized error:", error)
    return jsonify({"error": "Missing or invalid Authorization header", "details": str(error)}), 422

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    print("Expired token")
    return jsonify({"error": "Token has expired"}), 422

# Initialize bcrypt
bcrypt.init_app(app)

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Home
@app.route('/')
def home():
    return {"message": "Backend running successfully!"}


# -------------------------
# REGISTER ROUTE
# -------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    role = data.get("role")

    if User.query.filter((User.username == data["username"]) | (User.email == data["email"])).first():
        return jsonify({"error": "Username or email already exists"}), 400

    new_user = User(
        username=data["username"],
        email=data["email"],
        role=role
    )
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.flush()

    if role == "doctor":
        new_doctor = Doctor(
            user_id=new_user.id,
            name=data.get("name", new_user.username),
            specialty=data.get("specialty", "General Practitioner"),
            email=new_user.email
        )
        db.session.add(new_doctor)
    elif role == "patient":
        new_patient = Patient(
            user_id=new_user.id,
            name=data.get("name", new_user.username),
            email=new_user.email,
            age=data.get("age", 0),
            gender=data.get("gender", "unspecified")
        )
        db.session.add(new_patient)

    db.session.commit()
    return jsonify({"message": f"{role.capitalize()} registered successfully!"})


# -------------------------
# LOGIN ROUTE
# -------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT token with email as identity
    access_token = create_access_token(identity=email)  

    return jsonify({
        "message": "Login successful",
        "role": user.role,
        "token": access_token
    }), 200

# -------------------------
# CHAT ROUTE (JWT Protected)
# -------------------------
@app.route('/chat', methods=['POST'])
@jwt_required()
def chat_with_ai():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415

        data = request.get_json()
        message_text = data.get("message", "").strip()
        if not message_text:
            return jsonify({"error": "Message cannot be empty"}), 400

        # --- Identify user from JWT token ---
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.role != "patient":
            return jsonify({"error": "Only patients can chat"}), 403

        # --- Ensure Patient profile exists ---
        patient = Patient.query.filter_by(user_id=user.id).first()
        if not patient:
            return jsonify({"error": "Patient profile not found"}), 404

        # --- Save patient message ---
        user_msg = Message(sender="patient", content=message_text, patient_id=patient.id)
        db.session.add(user_msg)

        # --- Count patient messages in CURRENT session ---
        # Check if there's already a pending referral (means previous session ended)
        existing_referral = Referral.query.filter_by(
            patient_id=patient.id,
            status='pending'
        ).first()
        
        if existing_referral:
            # Session already ended, don't count old messages
            # Get messages only after the last referral was created
            patient_message_count = Message.query.filter(
                Message.patient_id == patient.id,
                Message.sender == "patient",
                Message.timestamp > existing_referral.timestamp
            ).count()
        else:
            # No referral yet, count all messages
            patient_message_count = Message.query.filter_by(
                patient_id=patient.id, 
                sender="patient"
            ).count()

        # --- Simulated AI response ---
        # After 5 patient messages, end conversation and refer to doctor
        if patient_message_count >= 5:
            ai_reply_text = ("Thank you for sharing your symptoms. Based on what you've told me, "
                           "I recommend you see a doctor for a proper examination. "
                           "Your case has been sent to a doctor who will review it shortly.")
            
            # Check if patient already has a pending referral (avoid duplicates)
            if not existing_referral:
                # FOR TESTING: Assign all patients to Dr. Xola (email: drxola@email.com)
                doctor = Doctor.query.filter_by(email='drxola@email.com').first()
                
                if doctor:
                    # Create referral to connect patient with doctor
                    referral = Referral(
                        patient_id=patient.id,
                        from_doctor_id=doctor.id,  # Assigned to Dr. Xola
                        to_doctor_id=None,  # No specialist referral yet
                        notes="AI consultation completed. Patient symptoms recorded in chat history.",
                        status='pending'
                    )
                    db.session.add(referral)
                    print(f"✅ Referral created: Patient {patient.id} → Doctor {doctor.id} ({doctor.name})")
                else:
                    # No doctors available
                    ai_reply_text = ("Thank you for sharing your symptoms. However, no doctors are currently available. "
                                   "Please try again later or contact support.")
                    print("❌ Dr. Xola not found!")
            
            conversation_ended = True
        else:
            conversation_responses = [
                "Thank you for sharing. How long have you been experiencing these symptoms?",
                "I see. Have you noticed any other symptoms accompanying this? For example, fever, fatigue, or pain in other areas?",
                "That's helpful information. On a scale of 1-10, how would you rate the severity of your symptoms?",
                "Thank you for providing those details. Are you currently taking any medications, or do you have any known allergies? Also before i end this brief consultation, is there any more information you would like to share"
            ]
            
            # Get response based on current message count (adjusted for frontend greeting)
            response_index = min(patient_message_count - 1, len(conversation_responses) - 1)
            ai_reply_text = conversation_responses[response_index]
            
            conversation_ended = False

        ai_msg = Message(sender="ai", content=ai_reply_text, patient_id=patient.id)
        db.session.add(ai_msg)
        db.session.commit()

        return jsonify({
            "reply": ai_reply_text,
            "conversation_ended": conversation_ended
        }), 200

    except Exception as e:
        db.session.rollback()
        print("Chat route error:", e)
        return jsonify({"error": f"Server error: {str(e)}"}), 500
    
# -------------------------
# LOGOUT ROUTE
# -------------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"})


# -------------------------
# CREATE PROFILES
# -------------------------
@app.route("/create_doctor", methods=["POST"])
@login_required
def create_doctor():
    if current_user.role != 'doctor':
        return jsonify({"error": "Access denied"}), 403
    data = request.get_json()
    if Doctor.query.filter_by(user_id=current_user.id).first():
        return jsonify({"error": "Doctor profile already exists"}), 400
    new_doctor = Doctor(
        user_id=current_user.id,
        name=data.get("name", current_user.username),
        specialty=data.get("specialty", "General Practitioner"),
        email=current_user.email
    )
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({"message": "Doctor profile created successfully!"})


@app.route("/create_patient", methods=["POST"])
@login_required
def create_patient():
    data = request.get_json()
    if Patient.query.filter_by(user_id=current_user.id).first():
        return jsonify({"error": "Patient profile already exists"}), 400
    new_patient = Patient(
        user_id=current_user.id,
        name=data["name"],
        email=data.get("email", current_user.email),
        age=data.get("age", 0),
        gender=data.get("gender", "unspecified")
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient profile created successfully!"})


# -------------------------
# DOCTOR ROUTES
# -------------------------
@app.route('/doctor/review', methods=['GET'])
@login_required
def doctor_review():
    if current_user.role != 'doctor':
        return jsonify({"error": "Access denied"}), 403
    data = []
    for patient in Patient.query.all():
        messages = Message.query.filter_by(patient_id=patient.id).order_by(Message.timestamp).all()
        chat_history = [{"sender": m.sender, "content": m.content, "timestamp": m.timestamp} for m in messages]
        data.append({"patient_id": patient.id, "patient_name": patient.name, "messages": chat_history})
    return jsonify(data)


@app.route('/doctor/patients', methods=['GET'])
@jwt_required()  
def doctor_patients():
    # Get user from JWT token
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    
    if not user or user.role not in ['doctor', 'gp']:
        return jsonify({"error": "Access denied"}), 403

    doctor = Doctor.query.filter_by(user_id=user.id).first()
    if not doctor:
        return jsonify({"error": "Doctor profile not found"}), 404

    # Get all referrals where this doctor is assigned
    interacted_patient_ids = set()
    interacted_patient_ids.update(r.patient_id for r in Referral.query.filter_by(from_doctor_id=doctor.id).all())
    interacted_patient_ids.update(r.patient_id for r in Referral.query.filter_by(to_doctor_id=doctor.id).all())

    print(f"🔍 Doctor ID: {doctor.id}, Found patient IDs: {interacted_patient_ids}")  # Debug

    patients_data = []
    for pid in interacted_patient_ids:
        patient = Patient.query.get(pid)
        if not patient:
            continue
        messages = Message.query.filter_by(patient_id=patient.id).order_by(Message.timestamp).all()
        chat_history = [{"sender": m.sender, "content": m.content, "timestamp": str(m.timestamp)} for m in messages]

        patients_data.append({
            "id": patient.id,
            "name": patient.name,
            "email": patient.email,
            "age": patient.age,
            "gender": patient.gender,
            "messages": chat_history
        })

    print(f"✅ Returning {len(patients_data)} patients")  # Debug
    return jsonify(patients_data)

# -------------------------
# DEBUG ROUTES
# -------------------------
@app.route('/debug/referrals', methods=['GET'])
def debug_referrals():
    referrals = Referral.query.all()
    data = []
    for r in referrals:
        patient = Patient.query.get(r.patient_id)
        from_doc = Doctor.query.get(r.from_doctor_id)
        data.append({
            "id": r.id,
            "patient_id": r.patient_id,
            "patient_name": patient.name if patient else "Unknown",
            "from_doctor_id": r.from_doctor_id,
            "from_doctor_name": from_doc.name if from_doc else "Unknown",
            "to_doctor_id": r.to_doctor_id,
            "status": r.status,
            "notes": r.notes
        })
    return jsonify({"referrals": data, "total": len(data)})

@app.route('/debug/doctors', methods=['GET'])
def debug_doctors():
    doctors = Doctor.query.all()
    data = []
    for d in doctors:
        data.append({
            "id": d.id,
            "name": d.name,
            "specialty": d.specialty,
            "email": d.email
        })
    return jsonify({"doctors": data, "total": len(data)})



@app.route('/doctor/refer_to_specialist', methods=['POST'])
@jwt_required()
def refer_to_specialist():
    try:
        # Get the referring doctor
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()
        
        if not user or user.role not in ['doctor', 'gp']:
            return jsonify({"error": "Access denied"}), 403
        
        referring_doctor = Doctor.query.filter_by(user_id=user.id).first()
        if not referring_doctor:
            return jsonify({"error": "Doctor profile not found"}), 404
        
        data = request.get_json()
        patient_id = data.get("patient_id")
        specialty = data.get("specialty")
        notes = data.get("notes", "")
        
        if not patient_id or not specialty:
            return jsonify({"error": "Missing patient_id or specialty"}), 400
        
        # FOR TESTING: Hardcode to specialist with user_id 6
        specialist_user = User.query.get(17)
        if not specialist_user:
            return jsonify({"error": "Test specialist (ID 17) not found"}), 404
        
        selected_specialist = Doctor.query.filter_by(user_id=specialist_user.id).first()
        if not selected_specialist:
            return jsonify({"error": "Specialist doctor profile not found"}), 404
        
        print(f"🔍 Referring to specialist: {selected_specialist.name} (Doctor ID: {selected_specialist.id})")
        
        # Create the referral
        new_referral = Referral(
            patient_id=patient_id,
            from_doctor_id=referring_doctor.id,
            to_doctor_id=selected_specialist.id,
            notes=f"Referral to {specialty}: {notes}",
            status='pending'
        )
        
        db.session.add(new_referral)
        db.session.commit()
        
        print(f"✅ Referral created: Patient {patient_id} → Specialist {selected_specialist.id}")
        
        return jsonify({
            "message": f"Patient successfully referred to {selected_specialist.name} ({specialty})",
            "specialist_name": selected_specialist.name,
            "specialty": specialty
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Referral error: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500


# -------------------------
# PAGE ROUTES
# -------------------------
@app.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
    if current_user.role != 'doctor':
        return jsonify({"error": "Access denied"}), 403
    return render_template('doctor_dashboard.html')


@app.route('/chat_page')
@login_required
def chat_page():
    if current_user.role != 'patient':
        return jsonify({"error": "Access denied"}), 403
    return render_template('chat.html')



@app.route('/doctor/end_consultation', methods=['POST'])
@jwt_required()
def end_consultation():
    try:
        # Get the doctor
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()
        
        if not user or user.role not in ['doctor', 'gp']:
            return jsonify({"error": "Access denied"}), 403
        
        doctor = Doctor.query.filter_by(user_id=user.id).first()
        if not doctor:
            return jsonify({"error": "Doctor profile not found"}), 404
        
        data = request.get_json()
        patient_id = data.get("patient_id")
        prescription = data.get("prescription", "")
        notes = data.get("notes", "")
        
        if not patient_id:
            return jsonify({"error": "Missing patient_id"}), 400
        
        # Save consultation as a message
        consultation_msg = Message(
            sender="doctor",
            content=f"Consultation notes: {notes}\nPrescription: {prescription}",
            patient_id=patient_id
        )
        db.session.add(consultation_msg)
        
        # Update referral status to completed
        referral = Referral.query.filter_by(
            patient_id=patient_id,
            from_doctor_id=doctor.id,
            status='pending'
        ).first()
        
        if referral:
            referral.status = 'completed'
            referral.prescription = prescription
            referral.notes = notes
        
        db.session.commit()
        
        return jsonify({
            "message": "Consultation recorded successfully",
            "patient_id": patient_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"End consultation error: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500
    


@app.route('/check_doctor_type', methods=['GET'])
@jwt_required()
def check_doctor_type():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    doctor = Doctor.query.filter_by(user_id=user.id).first()
    
    if not doctor:
        return jsonify({"error": "Not a doctor"}), 404
    
    return jsonify({
        "name": doctor.name,
        "specialty": doctor.specialty,
        "is_gp": doctor.specialty == "General Practitioner"
    }), 200

@app.route('/specialist/end_consultation', methods=['POST'])
@jwt_required()
def specialist_end_consultation():
    try:
        # Get the specialist
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()
        
        if not user or user.role != 'doctor':
            return jsonify({"error": "Access denied"}), 403
        
        specialist = Doctor.query.filter_by(user_id=user.id).first()
        if not specialist or specialist.specialty == "General Practitioner":
            return jsonify({"error": "Only specialists can use this endpoint"}), 403
        
        data = request.get_json()
        patient_id = data.get("patient_id")
        prescription = data.get("prescription", "")
        notes = data.get("notes", "")
        appointment_date = data.get("appointment_date")
        
        if not patient_id:
            return jsonify({"error": "Missing patient_id"}), 400
        
        # Save specialist consultation as a message
        consultation_content = f"Specialist Consultation ({specialist.specialty})\nNotes: {notes}\nPrescription: {prescription}"
        if appointment_date:
            consultation_content += f"\nFollow-up: {appointment_date}"
        
        consultation_msg = Message(
            sender="specialist",
            content=consultation_content,
            patient_id=patient_id
        )
        db.session.add(consultation_msg)
        
        # Update referral status to completed
        referral = Referral.query.filter_by(
            patient_id=patient_id,
            to_doctor_id=specialist.id,
            status='pending'
        ).first()
        
        if referral:
            referral.status = 'completed'
            if prescription:
                referral.prescription = prescription
            if notes:
                referral.notes = f"{referral.notes}\n\nSpecialist notes: {notes}"
            if appointment_date:
                from datetime import datetime
                referral.appointment_date = datetime.fromisoformat(appointment_date)
        
        db.session.commit()
        
        print(f"✅ Specialist consultation saved: Patient {patient_id} by {specialist.name}")
        
        return jsonify({
            "message": "Specialist consultation recorded successfully",
            "patient_id": patient_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Specialist consultation error: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500   
    

@app.route('/patient/consultations', methods=['GET'])
@jwt_required()
def patient_consultations():
    try:
        # Get patient from JWT
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()
        
        if not user or user.role != 'patient':
            return jsonify({"error": "Access denied - patients only"}), 403
        
        patient = Patient.query.filter_by(user_id=user.id).first()
        if not patient:
            return jsonify({"error": "Patient profile not found"}), 404
        
        # Get all referrals for this patient
        referrals = Referral.query.filter_by(patient_id=patient.id).order_by(Referral.timestamp.desc()).all()
        
        consultations = []
        
        for referral in referrals:
            # Get doctor info
            doctor = Doctor.query.get(referral.from_doctor_id)
            if not doctor:
                continue
            
            # Get specialist info if referred
            specialist = None
            if referral.to_doctor_id:
                specialist = Doctor.query.get(referral.to_doctor_id)
            
            # Get messages related to this consultation period
            messages = Message.query.filter_by(patient_id=patient.id).order_by(Message.timestamp).all()
            message_list = [
                {
                    "sender": msg.sender,
                    "content": msg.content,
                    "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                }
                for msg in messages
            ]
            
            # Create consultation entry for GP
            consultation = {
                "id": referral.id,
                "doctor_name": doctor.name,
                "specialty": doctor.specialty,
                "date": referral.timestamp.strftime("%Y-%m-%d %H:%M"),
                "status": referral.status.capitalize(),
                "prescription": referral.prescription if referral.prescription else None,
                "notes": referral.notes if referral.notes else None,
                "appointment_date": referral.appointment_date.strftime("%Y-%m-%d") if referral.appointment_date else None,
                "messages": message_list,
                "type": "GP Consultation"
            }
            consultations.append(consultation)
            
            # If there's a specialist referral, add it as separate consultation
            if specialist:
                specialist_consultation = {
                    "id": f"{referral.id}_specialist",
                    "doctor_name": specialist.name,
                    "specialty": specialist.specialty,
                    "date": referral.timestamp.strftime("%Y-%m-%d %H:%M"),
                    "status": referral.status.capitalize(),
                    "prescription": referral.prescription if referral.prescription else None,
                    "notes": referral.notes if referral.notes else None,
                    "appointment_date": referral.appointment_date.strftime("%Y-%m-%d") if referral.appointment_date else None,
                    "messages": message_list,
                    "type": "Specialist Consultation",
                    "referred_from": doctor.name
                }
                consultations.append(specialist_consultation)
        
        return jsonify(consultations), 200
        
    except Exception as e:
        print(f"Patient consultations error: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500
    
@app.route('/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    try:
        # Verify user is admin
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()
        
        if not user or user.role != 'admin':
            return jsonify({"error": "Access denied - admins only"}), 403
        
        # Get all patients
        all_patients = Patient.query.all()
        patients_data = []
        for patient in all_patients:
            messages = Message.query.filter_by(patient_id=patient.id).count()
            referrals = Referral.query.filter_by(patient_id=patient.id).all()
            
            patients_data.append({
                "id": patient.id,
                "name": patient.name,
                "email": patient.email,
                "age": patient.age,
                "gender": patient.gender,
                "total_messages": messages,
                "total_referrals": len(referrals),
                "created_at": patient.created_at.strftime("%Y-%m-%d") if patient.created_at else "N/A"
            })
        
        # Get all doctors
        all_doctors = Doctor.query.all()
        doctors_data = []
        for doctor in all_doctors:
            patients_count = Referral.query.filter(
                (Referral.from_doctor_id == doctor.id) | (Referral.to_doctor_id == doctor.id)
            ).distinct(Referral.patient_id).count()
            
            doctors_data.append({
                "id": doctor.id,
                "name": doctor.name,
                "specialty": doctor.specialty,
                "email": doctor.email,
                "patients_count": patients_count,
                "created_at": doctor.created_at.strftime("%Y-%m-%d") if doctor.created_at else "N/A"
            })
        
        # Get all admins
        all_admins = User.query.filter_by(role='admin').all()
        admins_data = [{
            "username": admin.username,
            "email": admin.email
        } for admin in all_admins]
        
        # Overall statistics
        stats = {
            "total_patients": len(patients_data),
            "total_doctors": len(doctors_data),
            "total_admins": len(admins_data),
            "total_messages": Message.query.count(),
            "total_referrals": Referral.query.count(),
            "pending_referrals": Referral.query.filter_by(status='pending').count(),
            "completed_referrals": Referral.query.filter_by(status='completed').count()
        }
        
        return jsonify({
            "stats": stats,
            "patients": patients_data,
            "doctors": doctors_data,
            "admins": admins_data
        }), 200
        
    except Exception as e:
        print(f"Admin dashboard error: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
