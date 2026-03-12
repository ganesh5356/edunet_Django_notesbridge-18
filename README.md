# 🎓 NotesBridge: Senior-to-Junior Learning Network

NotesBridge is a powerful, centralized hub designed to bridge the gap between Senior and Junior students. It streamlines the sharing of high-quality study materials, including notes, books, NPTEL resources, and previous years' question papers, ensuring academic success is accessible to all.

---

## 🚀 Key Features

### 👥 User Roles & Permissions
- **Seniors (Mentors)**: Empowered to upload resources, share their knowledge, and resolve doubts posted by juniors.
- **Juniors (Learners)**: Access a library of resources, download study materials, bookmark important items, and seek help via the doubt system.

### 📚 Resource Management
- **Centralized Repository**: Organize materials by Department (CSE, ECE, ME, etc.), Semester (1-8), and Subject.
- **Rich Media Support**: Handles both local file uploads and external resource links (like NPTEL videos).
- **Advanced Filtering**: Search by title, subject, or description, and filter by department or semester.

### 🤖 AI-Powered Assistance
- **Ask Anything Bot**: Integrated with **Google Gemini 2.0 Flash** to provide instant answers to academic queries and complex doubts.

### 💬 Engagement & Analytics
- **Doubt System**: A dedicated space for juniors to post questions and for seniors to provide expert replies.
- **Bookmarks**: Save essential resources for quick access later.
- **Download Tracking**: Insights into which resources are most beneficial to the community.
- **Dual Dashboards**: Personalized views for Seniors and Juniors with real-time stats on uploads, downloads, and doubts.

---

## 🛠 Tech Stack

- **Backend**: Python 3.x, Django 5.x
- **Frontend**: HTML5, CSS3 (Modern, responsive UI with Light/Dark mode), JavaScript
- **Database**: SQLite3 (Synced with JSON for high performance and portability)
- **AI Integration**: Google Gemini API (`gemini-2.0-flash`)
- **Storage**: Mixed local file storage and JSON-based metadata persistence.

---

## 📂 Project Structure

```text
NotesBridge/
├── accounts/           # User authentication, profiles, and role management
├── core/               # Landing pages, "Ask Anything" AI feature, and core views
├── resources/          # Main logic for resource handling, storage, and doubts
│   ├── data/           # JSON files for persistent storage
│   └── management/     # Custom Django commands (e.g., sync_json_to_db)
├── templates/          # Consolidated HTML templates
├── static/             # CSS styles, JS scripts, and brand assets
├── media/              # User-uploaded resource files
└── manage.py           # Django management utility
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Clone and Configure
```bash
# Clone the repository
git clone <repository-url>
cd notesbridge-django

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install django google-genai
```

### 3. Initialize Database
```bash
python manage.py migrate
python manage.py sync_json_to_db
```

### 4. Configure AI (Optional)
To enable the "Ask Anything" feature, add your Gemini API key in `notesbridge/settings.py`:
```python
GEMINI_API_KEY = "your-api-key-here"
```

### 5. Run the Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` to start exploring!

---

## 📖 Usage Guide

- **Login**: Use `/accounts/login/` to access the platform.
- **Dashboard**: Your command center for recent resources and personal stats.
- **Resource List**: Browse the library, use filters to find specific subjects.
- **Ask Anything**: Use the chatbot icon to get instant AI help on any topic.

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit Pull Requests or open issues for feature requests and bug reports.

---
"Thank you".

*NotesBridge - Empowering students through collective knowledge.*
