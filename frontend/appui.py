# Add this RIGHT AFTER your imports at the top of your Streamlit file (appui.py)
# Place it before st.set_page_config()

import streamlit as st
import requests

# Medical Theme Styling
st.markdown("""
    <style>
    /* Main background */
    .stApp {
       background: #ebd1dc;
        background: radial-gradient(circle,rgba(235, 209, 220, 1) 0%, rgba(177, 228, 240, 1) 100%);
        background-attachment: fixed;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #cae0ed;
        background: linear-gradient(90deg, rgba(202, 224, 237, 1) 0%, rgba(141, 184, 247, 1) 86%, rgba(141, 184, 247, 1) 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: black !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    h1 {
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
    }
    
    /* Buttons - Primary (Medical Blue) */
    .stButton>button {
        background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #2980b9 0%, #21618c 100%);
        box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
        transform: translateY(-2px);
    }
    
    /* Text inputs */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border: 2px solid #bdc3c7;
        border-radius: 8px;
        padding: 10px;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid #3498db;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: #d4edda;
        border-left: 5px solid #27ae60;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Error messages */
    .stError {
        background-color: #f8d7da;
        border-left: 5px solid #e74c3c;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Warning messages */
    .stWarning {
        background-color: #fff3cd;
        border-left: 5px solid #f39c12;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Info messages */
    .stInfo {
        background-color: #d1ecf1;
        border-left: 5px solid #3498db;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #ecf0f1;
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        background-color: transparent;
        color: #2c3e50;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
        color: white !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #ecf0f1;
        border-radius: 8px;
        font-weight: 600;
        color: #2c3e50;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #d5dbdb;
    }
    
    /* Selectbox */
    .stSelectbox>div>div {
        border-radius: 8px;
        border: 2px solid #bdc3c7;
    }
    
    /* Radio buttons */
    .stRadio>div {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
    }
    
    /* Columns */
    [data-testid="column"] {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #3498db, transparent);
        margin: 2rem 0;
    }
    
    /* Number input */
    .stNumberInput>div>div>input {
        border: 2px solid #bdc3c7;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Date input */
    .stDateInput>div>div>input {
        border: 2px solid #bdc3c7;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Logout button special styling */
    [data-testid="stSidebar"] .stButton>button {
        background: linear-gradient(90deg, #e74c3c 0%, #c0392b 100%);
        box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background: linear-gradient(90deg, #c0392b 0%, #a93226 100%);
    }
    
    /* Professional card-like appearance for patient info */
    .element-container {
        transition: all 0.3s ease;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #ecf0f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #3498db 0%, #2980b9 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #2980b9 0%, #21618c 100%);
    }
    </style>
""", unsafe_allow_html=True)

BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Doctor-Patient App", page_icon="💬", layout="wide")
st.title("💬 MediGrid")

# Rest of your code continues here...



# ---------------------
# Initialize session state
# ---------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = {}
if "token" not in st.session_state:
    st.session_state.token = None

# ---------------------
# Login/Register Section
# ---------------------
if not st.session_state.logged_in:
    st.sidebar.header("Welcome")
    
    # Toggle between Login and Register
    auth_mode = st.sidebar.radio("Choose an option:", ["Login", "Register"], key="auth_mode")
    
    if auth_mode == "Login":
        # LOGIN FORM
        st.sidebar.subheader("Login")
        email = st.sidebar.text_input("Email", key="login_email")
        password = st.sidebar.text_input("Password", type="password", key="login_password")

        if st.sidebar.button("Login", key="login_button"):
            try:
                response = requests.post(
                    f"{BASE_URL}/login", 
                    json={"email": email, "password": password}
                )
                try:
                    data = response.json()
                except Exception:
                    st.sidebar.error("Backend did not return valid JSON.")
                    data = {}

                if response.status_code == 200:
                    st.session_state.logged_in = True
                    st.session_state.user = {
                        "email": email,
                        "role": data.get("role", "")
                    }
                    st.session_state.token = data.get("token", "")
                    st.sidebar.success(f"Logged in as {st.session_state.user['role'].capitalize()}")
                    st.rerun()
                else:
                    st.sidebar.error(data.get("error", "Login failed"))

            except requests.exceptions.RequestException as e:
                st.sidebar.error(f"Cannot connect to backend: {e}")
            except Exception as e:
                st.sidebar.error(f"Unexpected error: {e}")
    
    else:
        # REGISTRATION FORM
        st.sidebar.subheader("Register")
        
        reg_role = st.sidebar.selectbox("I am a:", ["patient", "doctor"], key="reg_role")
        reg_username = st.sidebar.text_input("Username", key="reg_username")
        reg_email = st.sidebar.text_input("Email", key="reg_email")
        reg_password = st.sidebar.text_input("Password", type="password", key="reg_password")
        reg_name = st.sidebar.text_input("Full Name", key="reg_name")
        
        # fields based on role
        if reg_role == "patient":
            reg_age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=25, key="reg_age")
            reg_gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"], key="reg_gender")
        else:  # doctor
            reg_specialty = st.sidebar.text_input("Specialty", value="General Practitioner", key="reg_specialty")
        
        if st.sidebar.button("Register", key="register_button"):
            # Validation
            if not all([reg_username, reg_email, reg_password, reg_name]):
                st.sidebar.error("Please fill in all required fields")
            else:
                try:
                    # registration payload
                    payload = {
                        "username": reg_username,
                        "email": reg_email,
                        "password": reg_password,
                        "name": reg_name,
                        "role": reg_role
                    }
                    
                    # role-specific fields
                    if reg_role == "patient":
                        payload["age"] = reg_age
                        payload["gender"] = reg_gender.lower()
                    else:
                        payload["specialty"] = reg_specialty
                    
                    response = requests.post(f"{BASE_URL}/register", json=payload)
                    data = response.json()
                    
                    if response.status_code == 200:
                        st.sidebar.success("Registration successful! Logging you in...")
                        
                        # Automatically log in the user
                        login_response = requests.post(
                            f"{BASE_URL}/login",
                            json={"email": reg_email, "password": reg_password}
                        )
                        
                        if login_response.status_code == 200:
                            login_data = login_response.json()
                            st.session_state.logged_in = True
                            st.session_state.user = {
                                "email": reg_email,
                                "role": login_data.get("role", "")
                            }
                            st.session_state.token = login_data.get("token", "")
                            st.rerun()
                        else:
                            st.sidebar.info("Registration successful! Please login manually.")
                            st.rerun()
                    else:
                        st.sidebar.error(data.get("error", "Registration failed"))
                
                except requests.exceptions.RequestException as e:
                    st.sidebar.error(f"Cannot connect to backend: {e}")
                except Exception as e:
                    st.sidebar.error(f"Unexpected error: {e}")

# ---------------------
if st.session_state.logged_in:
    # Logout button in sidebar
    st.sidebar.write(f"**Logged in as:** {st.session_state.user.get('role', '').capitalize()}")
   
    
    if st.sidebar.button("🚪 Logout", key="logout_button"):
        # Clear all session state
        st.session_state.logged_in = False
        st.session_state.user = {}
        st.session_state.token = None
        if "conversation_ended" in st.session_state:
            st.session_state.conversation_ended = False
        if "chat_history" in st.session_state:
            st.session_state.chat_history = []
        st.rerun()
    
    st.sidebar.markdown("---") 
    
    role = st.session_state.user.get("role", "")

# ---------------------
# Role-based Interface
# ---------------------
if st.session_state.logged_in:
    role = st.session_state.user.get("role", "")

    # ----------------- Patient Chat -----------------


    if role == "patient":
        # Create tabs for Chat and Consultations
        tab1, tab2 = st.tabs(["💬 Chat with AI", "📋 My Consultations"])
        
        with tab1:
            st.subheader("🧍 Patient Chat")
            
            # Initialize conversation ended state
            if "conversation_ended" not in st.session_state:
                st.session_state.conversation_ended = False
            
            # Initialize chat history with AI greeting
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = [
                    {"role": "assistant", "content": "Hello! I'm here to help. Can you please describe your main symptoms?"}
                ]
            
            # Display previous messages
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.chat_message("user").markdown(msg["content"])
                else:
                    st.chat_message("assistant").markdown(msg["content"])
            
            # Check if conversation has ended
            if st.session_state.conversation_ended:
                st.success("✅ Your consultation has been sent to a doctor for review. They will contact you soon!")
                if st.button("Start New Consultation"):
                    st.session_state.conversation_ended = False
                    st.session_state.chat_history = [
                        {"role": "assistant", "content": "Hello! I'm here to help. Can you please describe your main symptoms?"}
                    ]
                    st.rerun()
            else:
                message = st.text_input("Type here:", key=f"patient_msg_{len(st.session_state.chat_history)}")

                if st.button("Send", key="send_patient"):
                    if not message.strip():
                        st.warning("Please type a message.")
                    elif not st.session_state.token:
                        st.error("Missing authentication token. Log in again.")
                    else:
                        try:
                            headers = {
                                "Authorization": f"Bearer {st.session_state.token}",
                                "Content-Type": "application/json"
                            }
                            res = requests.post(
                                f"{BASE_URL}/chat",
                                json={"message": message},
                                headers=headers
                            )
                            data = res.json()

                            if res.ok:
                                reply = data.get("reply", "")
                                
                                # Add to chat history
                                st.session_state.chat_history.append({"role": "user", "content": message})
                                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                                
                                # Check if conversation ended
                                if data.get("conversation_ended", False):
                                    st.session_state.conversation_ended = True
                                
                                # Rerun to update the display
                                st.rerun()
                            else:
                                st.error(data.get("error", f"Backend error {res.status_code}"))

                        except requests.exceptions.RequestException as e:
                            st.error(f"Cannot reach backend: {e}")
        
        with tab2:
            st.subheader("📋 My Consultations")
            
            try:
                # Fetch patient's consultations
                res = requests.get(
                    f"{BASE_URL}/patient/consultations",
                    headers={"Authorization": f"Bearer {st.session_state.token}"}
                )
                
                if res.ok:
                    consultations = res.json()
                    
                    if not consultations or len(consultations) == 0:
                        st.info("No consultations yet. Complete an AI chat to get started!")
                    else:
                        st.write(f"**Total Consultations:** {len(consultations)}")
                        st.markdown("---")
                        
                        for i, consult in enumerate(consultations, 1):
                            with st.expander(f"📅 Consultation #{i} - {consult['date']} with {consult['doctor_name']}"):
                                st.write(f"**Doctor:** {consult['doctor_name']} ({consult['specialty']})")
                                st.write(f"**Date:** {consult['date']}")
                                st.write(f"**Status:** {consult['status']}")
                                
                                if consult.get('prescription'):
                                    st.markdown("#### 💊 Prescription")
                                    st.info(consult['prescription'])
                                
                                if consult.get('notes'):
                                    st.markdown("#### 📝 Doctor's Notes")
                                    st.write(consult['notes'])
                                
                                if consult.get('appointment_date'):
                                    st.markdown("#### 📅 Follow-up Appointment")
                                    st.success(f"Scheduled for: {consult['appointment_date']}")
                                
                                # Show chat history for this consultation
                                if consult.get('messages'):
                                    with st.expander("View Full Conversation"):
                                        for msg in consult['messages']:
                                            if msg['sender'] == 'patient':
                                                st.chat_message("user").markdown(msg['content'])
                                            elif msg['sender'] == 'ai':
                                                st.chat_message("assistant").markdown(msg['content'])
                                            elif msg['sender'] in ['doctor', 'specialist']:
                                                st.chat_message("🩺 Doctor").markdown(msg['content'])
                else:
                    st.error("Unable to load consultations. Please try again later.")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Cannot connect to backend: {e}")
            except Exception as e:
                st.error(f"Error: {e}")



# ----------------- Doctor Interface (Check if GP or Specialist) -----------------

    elif role.lower() in ["gp", "doctor"]:
        # First, check if this doctor is actually a specialist
        try:
            res = requests.get(
                f"{BASE_URL}/check_doctor_type",
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )
            if res.ok:
                doctor_info = res.json()
                is_specialist = doctor_info.get("specialty") != "General Practitioner"
                specialty_name = doctor_info.get("specialty")
            else:
                is_specialist = False
                specialty_name = "Unknown"
        except:
            is_specialist = False
            specialty_name = "Unknown"
        
        # ========== SPECIALIST DASHBOARD ==========
        if is_specialist:
            st.subheader(f"🏥 Specialist Dashboard - {specialty_name}")

            # View all patients referred to this specialist
            st.write("### 👥 Patients referred to you")

            try:
                res = requests.get(
                    f"{BASE_URL}/doctor/patients", 
                    headers={"Authorization": f"Bearer {st.session_state.token}"}
                )
                data = res.json() if res.ok else []
                
                if not data:
                    st.info("No patients referred to you yet.")
                else:
                    patient_names = [p["name"] for p in data]
                    selected_patient = st.selectbox("Select a patient to view:", patient_names, key="specialist_patient_select")

                    # Show patient chat history
                    patient = next((p for p in data if p["name"] == selected_patient), None)
                    if patient:
                        st.write(f"**Email:** {patient['email']}")
                        st.write(f"**Age:** {patient['age']}")
                        st.write(f"**Gender:** {patient['gender']}")

                        st.write("#### 💬 Chat History with AI & GP")
                        for msg in patient["messages"]:
                            if msg["sender"] == "ai":
                                sender = "🤖 AI Assistant"
                            elif msg["sender"] == "doctor":
                                sender = "🩺 GP"
                            else:
                                sender = "🧍 Patient"
                            st.chat_message(sender).markdown(msg["content"])

                        # Specialist consultation form
                        st.write("### 📋 Specialist Consultation")
                        specialist_prescription = st.text_input("Prescription", key="specialist_prescription")
                        specialist_notes = st.text_area("Specialist Notes", key="specialist_notes")
                        appointment_date = st.date_input("Follow-up Appointment Date (optional)", key="specialist_date")
                        
                        if st.button("Submit Specialist Consultation", key="submit_specialist"):
                            if not specialist_notes.strip():
                                st.warning("Please provide consultation notes.")
                            else:
                                payload = {
                                    "patient_id": patient["id"],
                                    "prescription": specialist_prescription,
                                    "notes": specialist_notes,
                                    "appointment_date": str(appointment_date) if appointment_date else None
                                }
                                submit_res = requests.post(
                                    f"{BASE_URL}/specialist/end_consultation",
                                    json=payload,
                                    headers={"Authorization": f"Bearer {st.session_state.token}"}
                                )
                                if submit_res.ok:
                                    st.success("Specialist consultation recorded successfully!")
                                else:
                                    st.error(submit_res.json().get("error", "Error submitting consultation."))
            except Exception as e:
                st.error(f"Error loading patients: {e}")
        
        # ========== GP DASHBOARD ==========
        else:
            st.subheader("🩺 GP Dashboard")

            # View all patients
            st.write("### 👥 Patients under your care")

            try:
                res = requests.get(
                    f"{BASE_URL}/doctor/patients", 
                    headers={"Authorization": f"Bearer {st.session_state.token}"}
                )
                data = res.json() if res.ok else []
                
                if not data:
                    st.info("No patients available right now.")
                else:
                    patient_names = [p["name"] for p in data]
                    selected_patient = st.selectbox("Select a patient to view chat:", patient_names)

                    # Show patient chat history
                    patient = next((p for p in data if p["name"] == selected_patient), None)
                    if patient:
                        st.write(f"**Email:** {patient['email']}")
                        st.write(f"**Age:** {patient['age']}")
                        st.write(f"**Gender:** {patient['gender']}")

                        st.write("#### 💬 Chat History")
                        for msg in patient["messages"]:
                            sender = "🤖 AI Assistant" if msg["sender"] == "ai" else "🧍 Patient"
                            st.chat_message(sender).markdown(msg["content"])

                        # Columns for Consultation and Referral
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Add new consultation
                            st.write("### 📓 Add Consultation Notes")
                            prescription = st.text_input("Prescription", key="gp_prescription")
                            notes = st.text_area("Notes", key="gp_notes")
                            if st.button("Submit Consultation", key="submit_consultation"):
                                payload = {
                                    "patient_id": patient["id"],
                                    "prescription": prescription,
                                    "notes": notes
                                }
                                submit_res = requests.post(
                                    f"{BASE_URL}/doctor/end_consultation",
                                    json=payload,
                                    headers={"Authorization": f"Bearer {st.session_state.token}"}
                                )
                                if submit_res.ok:
                                    st.success("Consultation recorded successfully!")
                                else:
                                    st.error(submit_res.json().get("error", "Error submitting consultation."))
                        
                        with col2:
                            # Refer to Specialist
                            st.write("### 🏥 Refer to Specialist")
                            specialty_options = [
                                "Cardiology",
                                "Dermatology", 
                                "Orthopedics",
                                "Neurology",
                                "Pediatrics",
                                "Psychiatry",
                                "Ophthalmology",
                                "ENT (Ear, Nose, Throat)"
                            ]
                            selected_specialty = st.selectbox(
                                "Select Specialty", 
                                specialty_options,
                                key="specialist_select"
                            )
                            referral_notes = st.text_area(
                                "Referral Reason", 
                                placeholder="Why are you referring this patient?",
                                key="referral_notes"
                            )
                            
                            if st.button("Refer to Specialist", key="refer_button"):
                                if not referral_notes.strip():
                                    st.warning("Please provide a reason for referral.")
                                else:
                                    referral_payload = {
                                        "patient_id": patient["id"],
                                        "specialty": selected_specialty,
                                        "notes": referral_notes
                                    }
                                    referral_res = requests.post(
                                        f"{BASE_URL}/doctor/refer_to_specialist",
                                        json=referral_payload,
                                        headers={"Authorization": f"Bearer {st.session_state.token}"}
                                    )
                                    if referral_res.ok:
                                        st.success(f"Patient referred to Department of {selected_specialty} successfully!")
                                    else:
                                        st.error(referral_res.json().get("error", "Error referring patient."))
            except Exception as e:
                st.error(f"Error loading patients: {e}")

                
# ----------------- Admin Interface -----------------
    elif role == "admin":
        st.subheader(" Admin Dashboard")
        st.write(f"**Logged in as:** {st.session_state.user.get('email')}")
        
        try:
            res = requests.get(
                f"{BASE_URL}/admin/dashboard",
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )
            
            if res.ok:
                data = res.json()
                stats = data['stats']
                
                # Display statistics
                st.write("### 📊 System Statistics")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Patients", stats['total_patients'])
                with col2:
                    st.metric("Total Doctors", stats['total_doctors'])
                with col3:
                    st.metric("Pending Referrals", stats['pending_referrals'])
                with col4:
                    st.metric("Total Messages", stats['total_messages'])
                
                st.markdown("---")
                
                # Tabs for different views
                tab1, tab2, tab3 = st.tabs(["👥 All Patients", "🩺 All Doctors", "👥 Admins"])
                
                with tab1:
                    st.write("### All Patients")
                    if data.get('patients'):
                        for patient in data['patients']:
                            # Use patient name and email as the expander title
                            expander_title = f"{patient.get('name', 'Unknown')} - {patient.get('email', 'No email')}"
                            with st.expander(expander_title):
                                st.write(f"**Patient ID:** {patient.get('id', 'N/A')}")
                                st.write(f"**Name:** {patient.get('name', 'N/A')}")
                                st.write(f"**Email:** {patient.get('email', 'N/A')}")
                                st.write(f"**Age:** {patient.get('age', 'N/A')}")
                                st.write(f"**Gender:** {patient.get('gender', 'N/A').capitalize()}")
                                st.write(f"**Total Messages:** {patient.get('total_messages', 0)}")
                                st.write(f"**Total Referrals:** {patient.get('total_referrals', 0)}")
                                st.write(f"**Registered:** {patient.get('created_at', 'N/A')}")
                    else:
                        st.info("No patients in the system")
                
                with tab2:
                    st.write("### All Doctors")
                    if data.get('doctors'):
                        for doctor in data['doctors']:
                            # Use doctor name and specialty as the expander title
                            expander_title = f"{doctor.get('name', 'Unknown')} - {doctor.get('specialty', 'No specialty')}"
                            with st.expander(expander_title):
                                st.write(f"**Doctor ID:** {doctor.get('id', 'N/A')}")
                                st.write(f"**Name:** {doctor.get('name', 'N/A')}")
                                st.write(f"**Specialty:** {doctor.get('specialty', 'N/A')}")
                                st.write(f"**Email:** {doctor.get('email', 'N/A')}")
                                st.write(f"**Patients Handled:** {doctor.get('patients_count', 0)}")
                                st.write(f"**Registered:** {doctor.get('created_at', 'N/A')}")
                    else:
                        st.info("No doctors in the system")
                
                with tab3:
                    st.write("### System Admins")
                    if data.get('admins'):
                        for admin in data['admins']:
                            st.write(f"- **{admin.get('username', 'Unknown')}** ({admin.get('email', 'No email')})")
                    else:
                        st.info("No admins in the system")
            else:
                st.error("Unable to load admin dashboard")
        
        except Exception as e:
            st.error(f"Error: {e}")
    
    else:
        st.error("Unknown role. Contact admin.")