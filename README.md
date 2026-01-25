# School Management System Backend

---
# Django Project Setup Guide

This repository contains a Django application that uses environment-based configuration.
Follow the steps below to set up and run the project locally or in production

---

## Prerequisites

Ensure you have the following installed:

* Python **3.9+** (or the version required by your project)
* pip
* virtualenv (recommended)
* PostgreSQL / MySQL / SQLite (depending on project configuration)
* Git

---

## Project Structure (Relevant Files)

```
.
├── apps
├── config
├── requirements/
│   └── base.txt
├── .env.development
├── .env.production
├── manage.py
└── README.md
```

---

## 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
```

---

## 2. Create and Activate a Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

All required libraries are defined in `requirements/base.txt`.

```bash
pip install -r requirements/base.txt
```

---

## 4. Environment Configuration

The project requires **environment-specific variables**.

### Required Files

* `.env.development` → for local development
* `.env.production` → for production deployment

### Example `.env.development`

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
ENVIRONMENT=production

# Database
DB_NAME=school_db
DB_USER=school_user
DB_PASSWORD=secure_password_here
DB_HOST=db
DB_PORT=3306
DB_ROOT_PASSWORD=root_password_here

# Security
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
CSRF_TRUSTED_ORIGINS=http://localhost:8000

# Email (Optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

> ⚠️ **Never commit `.env` files to version control.**
> Ensure they are listed in `.gitignore`.

---

## 5. Apply Database Migrations

Run the following commands to prepare the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6. Create a Superuser (Admin Access)

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to set:

* Email
* Password

---

## 7. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:

```
http://127.0.0.1:8000/
```

Admin panel:

```
http://127.0.0.1:8000/admin/
```

Swagger API Docs:

```
http://127.0.0.1:8000/api/docs
```

---

## 8. Running in Production

1. Ensure `.env.production` is properly configured
2. Set `DEBUG=False`
3. Configure allowed hosts and security settings
4. Run migrations:

   ```bash
   python manage.py migrate
   ```
5. Collect static files:

   ```bash
   python manage.py collectstatic
   ```
6. Use a production-grade server (e.g. Gunicorn + Nginx)

---

## Common Commands Summary

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py collectstatic
```

---

## Notes

* Always activate the virtual environment before running commands
* Keep environment variables secure
* Update `requirements/base.txt` when adding new dependencies

---
