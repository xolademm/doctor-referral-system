# 🏥 Doctor Referral System

## 📘 Overview
The **Doctor Referral System** is a web-based platform designed to streamline communication and collaboration between **patients**, **general practitioners**, and **specialist doctors**.

The system simplifies the referral process by documenting every patient interaction, referral, and test with **timestamps** while ensuring data security and accessibility. It incorporates an **AI assistant** that interacts with patients upon sign-in, collects their symptoms and history, and organizes the information neatly for doctors to review — **without performing any diagnosis**.

---

## 🎯 Project Objectives
- Improve coordination between doctors and specialists.  
- Allow structured, timestamped documentation of patient interactions.  
- Ensure patient data security and controlled access via authentication.  
- Integrate an AI assistant for patient data collection and organization.  
- Store and manage all data in a PostgreSQL database.  
- Deploy a fully functional web app using Vercel (frontend) and an online backend host.  

---

## 🧩 System Architecture

### **Frontend**
- Built with **Next.js** and hosted on **Streamlit**.  
- User roles: Patient, Doctor, Admin.  
- Interactive dashboards for communication and record viewing.

### **Backend**
- Built with **Node.js** and **Express.js**.  
- RESTful API endpoints for authentication, patient management, and referrals.  
- Integrated with **PostgreSQL** for persistent data storage.

### **Database (PostgreSQL)**
**Core Tables:**
- **Users:** Stores login info and user roles (patient/doctor/admin).  
- **Patients:** Contains personal info and medical history.  
- **Doctors:** Contains doctor details and specialties.  
- **Referrals:** Logs all referrals and statuses with timestamps.  
- **Logs:** Records every system action for traceability.  

### **AI Assistant**
- Initiates the first conversation with patients.  
- Collects and structures symptom details and visit reasons.  
- Automatically timestamps and saves data to the database.  
- Does **not** diagnose or give medical advice.

---

## ⚙️ Technology Stack

| Component | Technology |
|------------|-------------|
| Frontend | Next.js (React Framework) |
| Backend | Node.js + Express.js |
| Database | PostgreSQL |
| Hosting | Vercel (Frontend), Render/Railway (Backend) |
| Version Control | Git & GitHub |
| Authentication | JSON Web Tokens (JWT) |
| AI Integration | OpenAI API or Python-based NLP model (optional) |

---

## 🧪 Features
- 🧍‍♀️ **Patient Module:** Profile creation, AI-assisted symptom entry, record viewing.  
- ⚕️ **Doctor Module:** Patient review, referrals, test documentation.  
- 🩺 **Specialist Module:** Review referrals, update tests and recommendations.  
- 🔐 **Admin Module:** Manage users, access logs, and system data.  
- 🧾 **Timestamped Activity Logs:** Tracks all actions for accountability.  
- 🤖 **AI Assistant:** Conversational data intake, structured reporting.  

---



