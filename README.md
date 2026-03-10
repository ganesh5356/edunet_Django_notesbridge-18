# NotesBridge (Django-only)

NotesBridge is a Senior-to-Junior Learning Network that centralizes study materials (Notes, Books, NPTEL, Previous Papers).
This version uses **Django templates + Python** and stores resource metadata in a **JSON file** (no custom DB models).

## Modules
- Accounts: Signup/Login/Logout (role: Junior/Senior stored in session)
- Resources: List/Search/Filter, Detail, Upload (Senior only)
- Core: Landing, About

## Run
```bash
pip install django
python manage.py migrate
python manage.py runserver
```

Open:
- http://127.0.0.1:8000/
