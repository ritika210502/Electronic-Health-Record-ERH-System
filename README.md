# Objective
Clinic360 is a scalable web application for managing electronic health records (EHR), patient
appointments,
and doctor schedules. This platform is designed to streamline patient and doctor interactions in a
clinic setting,
providing secure access to health records and easy appointment booking.
# Tech Stack:
- Backend: Django, Django Rest Framework (DRF), JWT Authentication
- Database: PostgreSQL
- Frontend: Bootstrap 5 (for responsive UI)
- Asynchronous Tasks: Celery (for email notifications)
- Deployment: Local development, pending production deployment
- Version Control: Git
# Features:
## 1. Electronic Health Records (EHR) System:
 - Patient Registration
 - Create and Manage Medical Records
 - View Patient Health Records
 - Secure API Access with JWT Authentication
## 2. Appointment Booking System:
 - Doctor Availability Management
 - Appointment Booking, Rescheduling, and Cancellation
 - Email Notifications for Successful Bookings and Changes
## 3. User Interface:
 - Patient Portal:
 - Register/Login
 - View and Update Personal Details
 - Book, Reschedule, or Cancel Appointments
 - View Medical Records (EHR)
 - Doctor Portal:
 - Register/Login
 - Manage Available Appointment Slots
 - View Scheduled Appointments
 - Access and Update Patient Medical Records
# Setup and Installation:
## 1. Clone the repository:
 git clone <repository-url>
 cd Clinic360
## 2. Install dependencies:
 pip install -r requirements.txt
## 3. Set up PostgreSQL database:
 - Create a database and user in PostgreSQL
 - Update your database credentials in settings.py under DATABASES
## 4. Run migrations:
 python manage.py migrate
## 5. Create a superuser:
 python manage.py createsuperuser
## 6. Run the development server:
 python manage.py runserver
# API Usage Guide:
## Authentication:
- POST /register-patient/ - Register a patient
- POST /login/ - Login a patient or doctor (JWT token returned)
- Use the JWT token in the Authorization header for all protected endpoints.
## Patient Endpoints:
- POST /register-patient/ - Register a patient with details like name, age, gender, contact, and medical history.
- POST /create-record/ - Create a new medical record for the patient.
- GET /view-records/{patient_id}/ - View all medical records of a patient.
- PUT /update-record/{record_id}/ - Update a medical record.
- DELETE /delete-record/{record_id}/ - Delete a medical record.
## Doctor Endpoints:
- POST /register-doctor/ - Register a doctor.
- POST /create-availability/ - Create doctor availability time slots.
- GET /view-appointments/ - Get the list of appointments for the doctor.
- GET /view-patient-records/{patient_id}/ - Access and update patient medical records.
## Appointment Endpoints:
- POST /book-appointment/ - Book an appointment for a patient.
- POST /reschedule-appointment/ - Reschedule an existing appointment.
- POST /cancel-appointment/ - Cancel an appointment.
## Frontend Deployment:
Once the backend is set up, you can deploy the frontend using a platform like Vercel or Netlify.
Ensure that the frontend is connected to the backend via API endpoints.
