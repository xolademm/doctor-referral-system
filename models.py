from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from database import db
from datetime import datetime

# Initialize Bcrypt instance
bcrypt = Bcrypt()

# -------------------------
# USER MODEL
# -------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))  # 'patient', 'doctor', 'admin'

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # Optional helper properties
    @property
    def is_doctor(self):
        return self.role == 'doctor'

    @property
    def is_patient(self):
        return self.role == 'patient'


# -------------------------
# DOCTOR MODEL
# -------------------------
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship back to User
    user = db.relationship('User', backref='doctor_profile')


# -------------------------
# PATIENT MODEL
# -------------------------
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='patient_profile')


# -------------------------
# REFERRAL MODEL
# -------------------------
class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    from_doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    to_doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=True)
    notes = db.Column(db.Text)
    prescription = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='pending')  # pending | completed | referred
    appointment_date = db.Column(db.DateTime, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='referrals')
    from_doctor = db.relationship('Doctor', foreign_keys=[from_doctor_id])
    to_doctor = db.relationship('Doctor', foreign_keys=[to_doctor_id])


# -------------------------
# MESSAGE MODEL
# -------------------------
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50))  # 'user' or 'ai'
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
