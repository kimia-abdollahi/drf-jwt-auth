# DRF JWT Auth API

A clean Django REST Framework project with JWT authentication & Swagger UI.

## Features
- User registration
- JWT login / refresh / logout (blacklist)
- Protected profile endpoint
- Admin-only endpoint
- Swagger (`/api/docs/`) and Redoc (`/api/redoc/`) documentation

## Setup
```bash
git clone https://github.com/<YOUR-USERNAME>/drf-jwt-auth.git
cd drf-jwt-auth
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
