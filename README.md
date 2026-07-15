# SchoolMS — School Management System

A full-featured school management system built with Django, deployed on AWS with CI/CD pipeline.

## 🌐 Live Demo
**URL:** http://35.154.5.116:8080

**Test Credentials:**
- Admin: `/admin/` (superuser)
- Student: Register at `/accounts/register/`
- Teacher: Created by admin

---

## 🚀 Tech Stack

### Backend
- **Django 4.2** — Web framework
- **Django REST Framework** — REST APIs
- **SimpleJWT** — JWT Authentication
- **PostgreSQL** — Production database (AWS RDS)
- **Gunicorn** — WSGI HTTP Server

### Frontend
- **Bootstrap 5** — UI Framework
- **Bootstrap Icons** — Icon library

### AWS Services
- **EC2** — Application server (Ubuntu)
- **RDS** — PostgreSQL database
- **S3** — File storage (photos, PDFs, school images)
- **CDN** - integrated cloudfront cdn with s3 bucket

### DevOps
- **Nginx** — Reverse proxy & static files
- **GitHub Actions** — CI/CD pipeline
- **Git** — Version control
- **Docker** - Dockerized django app

---

## ✨ Features

### Student
- Register with profile photo (uploaded to S3)
- Upload admission documents (PDF → S3)
- View admission status (pending/approved/rejected)
- Browse subjects with assigned teachers
- Enroll in subjects
- View attendance per subject
- Password reset via email

### Teacher
- Login and view dashboard
- See enrolled students per subject
- Mark daily attendance (present/absent)
- View subject-wise student list

### Admin
- Approve/reject admission requests
- View uploaded documents directly from admin panel
- Email notification sent automatically on approval/rejection
- Manage subjects and assign teachers
- Upload school images (banner, gallery, facilities)
- Bulk approve/reject admissions

### APIs (JWT Protected)
- `POST /api/login/` — Login
- `POST /api/register/` — Register
- `POST /api/logout/` — Logout (token blacklist)
- `POST /api/token/refresh/` — Refresh token
- `GET /api/student/profile/` — Student profile
- `PUT /api/student/profile/update/` — Update profile
- `GET /api/student/admission/` — Admission status
- `GET /api/student/subjects/` — Enrolled subjects
- `GET /api/subjects/` — All subjects
- `GET /api/subjects/<id>/` — Subject detail

---

## 🏗️ Project Structure

```
schoolms/
├── accounts/          # User, StudentProfile, TeacherProfile
├── admissions/        # AdmissionRequest model & admin
├── subjects/          # Subject, Attendance, Enrollment
├── core/              # Home page, SchoolImage
├── api/               # REST API views & serializers
├── templates/         # HTML templates
├── school_mgmt/       # Django settings & urls
├── .github/
│   └── workflows/
│       └── deploy.yml # GitHub Actions CI/CD
├──  requirements.txt
├── .dockerignore
├── .env
├── docker-compose.yml
├── Dockerfile
└── manage.py
```

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.12+
- PostgreSQL
- AWS Account (S3)

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/Sarth4k/schoolms.git
cd schoolms

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env
# Fill in your credentials

# 4. Run migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

---

## 🔐 Environment Variables

Create a `.env` file in project root:

```dotenv
SECRET_KEY=your-django-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain-or-ip

# Database
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=your-rds-endpoint
DB_PORT=5432

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=ap-south-1

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## 🚀 Deployment (AWS EC2)

### Server Stack
```
Internet → Nginx (port 80/8080) → Gunicorn (port 8001) → Django
```

### CI/CD Pipeline
Every push to `master` branch:
1. GitHub Actions SSH into EC2
2. Pull latest code
3. Install dependencies
4. Run migrations
5. Collect static files
6. Restart Gunicorn & Nginx

```yaml
# .github/workflows/deploy.yml
on:
  push:
    branches: [master]
```

---

## 📸 Screenshots

### Home Page
- School banner/slider (images from S3)
 <img width="1901" height="891" alt="image" src="https://github.com/user-attachments/assets/3ae9966e-edbb-423d-8421-769a1965b970" />

- Stats (students, teachers, subjects)
 <img width="1900" height="1080" alt="image" src="https://github.com/user-attachments/assets/3d4ff7ab-1b9a-40b8-8cbf-cca74a9c59c9" />

### Student Dashboard
- Admission status
 <img width="1920" height="881" alt="image" src="https://github.com/user-attachments/assets/35d0017a-047c-4554-83d3-f6e531063f8b" />

- Enrolled subjects
 <img width="1915" height="879" alt="image" src="https://github.com/user-attachments/assets/d95d1939-efcf-452f-9d77-c4136f527aa1" />

- Attendance summary
 <img width="1916" height="851" alt="image" src="https://github.com/user-attachments/assets/08b8b87c-a3ad-4ebf-a9b0-befd77067885" />


### Teacher Dashboard
- Subject list with enrolled students
 <img width="1920" height="780" alt="image" src="https://github.com/user-attachments/assets/132c9104-4f6f-41fd-9c88-02baa5146762" />

- Mark attendance
 <img width="1916" height="718" alt="image" src="https://github.com/user-attachments/assets/1293d756-bda5-4681-b798-84942bed4ee0" />

---

## 🔄 API Flow

```
POST /api/login/
→ Returns access + refresh token

GET /api/student/profile/
Headers: Authorization: Bearer <access_token>
→ Returns student profile data

POST /api/token/refresh/
Body: { "refresh": "token" }
→ Returns new access token

POST /api/logout/
Body: { "refresh": "token" }
→ Blacklists refresh token
```

---

## 👨‍💻 Developer

**Sarthak** — [@Sarth4k](https://github.com/Sarth4k)

- 📧 sarth4ks@gmail.com
- 🎓 Amity University Punjab, Mohali
