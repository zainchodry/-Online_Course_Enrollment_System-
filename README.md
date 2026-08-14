# 📚 Online Course Enrollment System — Django REST Framework

A full-featured **RESTful API** for an online course enrollment platform built with **Django REST Framework**. The system supports multi-role authentication (Admin, Instructor, Student), course management with modular content, student enrollments with payment tracking, lesson progress, and course reviews.

---

## 🏗️ Architecture

```
core/                   → Django project settings & root URL configuration
accounts/               → Custom user model, JWT auth, profile, password reset
courses/                → Course, Category, Module, Lesson CRUD
enrollments/            → Student enrollment, payment, lesson progress tracking
reviews/                → Course review & rating system
```

---

## ✨ Features

### 🔐 Authentication & Accounts
- Custom user model with **email-based login** (no username)
- **Role-based access control** — `ADMIN`, `INSTRUCTOR`, `STUDENT`
- **JWT authentication** via `djangorestframework-simplejwt`
- User registration with password confirmation & validation
- User profile management (headline, bio, avatar, qualification)
- Change password & password reset via email

### 📖 Courses
- **Categories** — Admin-managed course categories with slug generation
- **Courses** — Instructors can create/manage courses with thumbnails, pricing, and publish status
- **Modules & Lessons** — Hierarchical content structure (Course → Modules → Lessons)
- Search, filtering, and ordering support
- Instructors see their own drafts; students see only published courses

### 📝 Enrollments
- Students can enroll in published courses
- **Automatic payment record** generation (free vs. paid courses)
- **Lesson progress tracking** — mark individual lessons as complete
- Role-scoped querysets (students see own, instructors see their courses' enrollments, admin sees all)

### ⭐ Reviews
- Students can review courses they're enrolled in (1-5 star rating + comment)
- One review per student per course enforcement
- Average rating calculation on course listings
- Filter and order reviews

---

## 🛠️ Tech Stack

| Component          | Technology                              |
| ------------------ | --------------------------------------- |
| Framework          | Django 5.2 + Django REST Framework      |
| Authentication     | JWT (Simple JWT) with token blacklist   |
| Database           | SQLite (default, swappable)             |
| Filtering          | django-filter                           |
| Email              | SMTP (Gmail) with threaded sending      |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the Repository
```bash
git clone https://github.com/zainchodry/-Online_Course_Enrollment_System-.git
cd Online\ Course\ Enrollment\ System\ Drf
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies
```bash
pip install django djangorestframework djangorestframework-simplejwt django-filter Pillow
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## 📡 API Endpoints

### Accounts (`/api/accounts/`)
| Method | Endpoint                        | Description                  | Auth     |
| ------ | ------------------------------- | ---------------------------- | -------- |
| POST   | `/api/accounts/register/`       | Register a new user          | Public   |
| POST   | `/api/accounts/login/`          | Obtain JWT token pair        | Public   |
| POST   | `/api/accounts/token/refresh/`  | Refresh JWT access token     | Public   |
| GET    | `/api/accounts/profile/`        | View current user profile    | Required |
| PUT    | `/api/accounts/profile/`        | Update current user profile  | Required |
| PUT    | `/api/accounts/change-password/`| Change password              | Required |
| POST   | `/api/accounts/request-reset-email/` | Request password reset  | Public   |
| PATCH  | `/api/accounts/password-reset-complete/` | Set new password    | Public   |

### Courses (`/api/courses/`)
| Method | Endpoint                          | Description               | Auth              |
| ------ | --------------------------------- | ------------------------- | ----------------- |
| GET    | `/api/courses/categories/`        | List categories           | Public            |
| POST   | `/api/courses/categories/`        | Create category           | Admin only        |
| GET    | `/api/courses/courses/`           | List courses              | Public            |
| POST   | `/api/courses/courses/`           | Create course             | Instructor/Admin  |
| GET    | `/api/courses/courses/{id}/`      | Course detail             | Public            |
| PUT    | `/api/courses/courses/{id}/`      | Update course             | Owner/Admin       |
| DELETE | `/api/courses/courses/{id}/`      | Delete course             | Owner/Admin       |
| GET    | `/api/courses/modules/`           | List modules              | Public            |
| POST   | `/api/courses/modules/`           | Create module             | Instructor/Admin  |
| GET    | `/api/courses/lessons/`           | List lessons              | Public            |
| POST   | `/api/courses/lessons/`           | Create lesson             | Instructor/Admin  |

### Enrollments (`/api/enrollments/`)
| Method | Endpoint                                       | Description              | Auth          |
| ------ | ---------------------------------------------- | ------------------------ | ------------- |
| GET    | `/api/enrollments/`                             | List enrollments         | Required      |
| POST   | `/api/enrollments/`                             | Enroll in a course       | Student only  |
| GET    | `/api/enrollments/{id}/`                        | Enrollment detail        | Owner/Admin   |
| PATCH  | `/api/enrollments/{id}/update_progress/`        | Mark lesson complete     | Student only  |

### Reviews (`/api/reviews/`)
| Method | Endpoint                   | Description           | Auth          |
| ------ | -------------------------- | --------------------- | ------------- |
| GET    | `/api/reviews/`            | List all reviews      | Public        |
| POST   | `/api/reviews/`            | Create a review       | Enrolled only |
| GET    | `/api/reviews/{id}/`       | Review detail         | Public        |
| PUT    | `/api/reviews/{id}/`       | Update own review     | Author only   |
| DELETE | `/api/reviews/{id}/`       | Delete own review     | Author/Admin  |

---

## 👥 Role Permissions

| Action                    | Admin | Instructor | Student |
| ------------------------- | ----- | ---------- | ------- |
| Manage Categories         | ✅    | ❌         | ❌      |
| Create/Edit Own Courses   | ✅    | ✅         | ❌      |
| View Published Courses    | ✅    | ✅         | ✅      |
| Enroll in Courses         | ❌    | ❌         | ✅      |
| Track Lesson Progress     | ❌    | ❌         | ✅      |
| Review Enrolled Courses   | ❌    | ❌         | ✅      |
| View All Enrollments      | ✅    | Own Courses| Own     |

---

## ⚙️ Configuration

### Email (Password Reset)
Update `core/settings.py` with your SMTP credentials:
```python
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

### Database
The project uses SQLite by default. To switch to PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
