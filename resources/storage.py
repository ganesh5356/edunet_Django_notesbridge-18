import json
from pathlib import Path
from django.conf import settings
from django.contrib.auth.models import User

DATA_FILE = Path(settings.BASE_DIR) / "resources" / "data" / "resources.json"
BOOKMARK_FILE = Path(settings.BASE_DIR) / "resources" / "data" / "bookmarks.json"
DOUBT_FILE = Path(settings.BASE_DIR) / "resources" / "data" / "doubts.json"
DOWNLOAD_FILE = Path(settings.BASE_DIR) / "resources" / "data" / "downloads.json"


def load_downloads():
    if not DOWNLOAD_FILE.exists():
        DOWNLOAD_FILE.parent.mkdir(parents=True, exist_ok=True)
        DOWNLOAD_FILE.write_text("[]", encoding="utf-8")
    return json.loads(DOWNLOAD_FILE.read_text(encoding="utf-8"))


def save_downloads(items):
    DOWNLOAD_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")


def get_chat_response(query):
    """Fallback chat response using local knowledge base when Gemini quota is exceeded."""
    chat_knowledge = {
        "project": "NotesBridge is a Senior-to-Junior Learning Network that centralizes study materials like Notes, Books, NPTEL, and Previous Papers.",
        "notesbridge": "NotesBridge is a platform designed to connect Seniors and Juniors for knowledge sharing through study materials.",
        "notes": "You can find and search for various study materials like Notes, Books, and Papers in the Resources section.",
        "study": "We provide centralized study materials including Notes, Books, NPTEL resources, and Previous Papers.",
        "books": "Our library includes various books categorized by subject and semester in the Resources section.",
        "senior": "Seniors are mentors who can upload study materials to help their juniors learn efficiently.",
        "junior": "Juniors can search for, view, and learn from resources shared by experienced Seniors.",
        "upload": "Only users with the 'Senior' role can upload new resources to the platform.",
        "role": "Roles (Junior or Senior) are chosen during signup and determine your permissions on the site.",
        "signup": "Create an account by clicking 'Sign Up'. You'll need to choose if you are a Junior or a Senior.",
        "login": "Use the 'Login' page to access your account with your username and password.",
        "signin": "Click 'Login' in the navigation bar to access your NotesBridge account.",
        "logout": "You can end your session by clicking 'Logout' in the top navigation bar.",
        "nptel": "We host NPTEL study materials and links to help you with your specialized courses.",
        "papers": "Previous year question papers and model answers are available in the Resources section.",
        "about": "NotesBridge aims to empower students through collaborative peer learning and easy access to materials.",
        "help": "I can assist you with questions about NotesBridge features, roles, and navigation. Ask me about notes, roles, or how to join!",
        "contact": "You can reach out to us at info@notesbridge.com for any specific support queries.",
        "download": "You can download resources by clicking on the download button in the resource card.",
        "bookmark": "You can bookmark resources by clicking on the bookmark button in the resource card.",
        "remove-bookmark": "You can remove bookmarks by clicking on the bookmark button in the resource card.",
        "dashboard": "You can view and search for resources in the dashboard.",
        "resources": "You can view and search for resources in the resources section.",
        "doubts": "You can view and search for doubts in the doubts section.",
        "upload": "You can upload resources by clicking on the upload button in the resources section.",
        "profile": "You can view and edit your profile in the profile section.",
        "edit-profile": "You can view and edit your profile in the profile section.",
        "bookmarks": "You can view your bookmarks in the bookmarks section.",
        "delete": "Only seniors can delete resources from the resources list.",
        "senior delete": "Seniors can delete resources they uploaded by clicking the delete button on the resource card.",
        "quota": "The AI chat service has a quota limit. When exceeded, it falls back to a local knowledge base.",
        "gemini": "Gemini is the AI model used for the chat feature, but it has usage limits.",
        "ai": "The chat uses Gemini AI, but falls back to local responses when quota is exceeded.",
    }

    lower_query = query.lower()

    for key in chat_knowledge:
        if key in lower_query:
            return chat_knowledge[key]

    return "I'm sorry, I don't have information on that topic. Please ask about NotesBridge features, roles, or navigation."
    # Sync to DB
    from .models import Download
    for it in items:
        Download.objects.get_or_create(
            resource_id=it.get("resource_id"),
            user=it.get("user")
        )


def load_resources():
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text("[]", encoding="utf-8")
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_resources(items):
    DATA_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")
    # Sync to DB
    from .models import Resource
    for it in items:
        user = User.objects.filter(username=it.get("uploaded_by")).first()
        if not user:
            user = User.objects.filter(is_superuser=True).first()
        Resource.objects.update_or_create(
            id=it.get("id"),
            defaults={
                "title": it.get("title"),
                "description": it.get("description"),
                "department": it.get("department"),
                "semester": it.get("semester"),
                "subject": it.get("subject"),
                "resource_type": it.get("resource_type"),
                "file": it.get("file_path", ""),
                "uploaded_by": user,
            }
        )


def load_bookmarks():
    if not BOOKMARK_FILE.exists():
        BOOKMARK_FILE.parent.mkdir(parents=True, exist_ok=True)
        BOOKMARK_FILE.write_text("[]", encoding="utf-8")
    return json.loads(BOOKMARK_FILE.read_text(encoding="utf-8"))


def save_bookmarks(items):
    BOOKMARK_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")
    # Sync to DB
    from .models import Bookmark, Resource
    for it in items:
        user = User.objects.filter(username=it.get("user")).first()
        resource = Resource.objects.filter(id=it.get("resource_id")).first()
        if user and resource:
            Bookmark.objects.get_or_create(user=user, resource=resource)


def load_doubts():
    if not DOUBT_FILE.exists():
        DOUBT_FILE.parent.mkdir(parents=True, exist_ok=True)
        DOUBT_FILE.write_text("[]", encoding="utf-8")

    doubts = json.loads(DOUBT_FILE.read_text(encoding="utf-8"))

    # ensure resolved field exists
    for d in doubts:
        if "resolved" not in d:
            d["resolved"] = False

    return doubts


def save_doubts(items):
    DOUBT_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")
    # Sync to DB
    from .models import Doubt
    for it in items:
        Doubt.objects.update_or_create(
            id=it.get("id"),
            defaults={
                "subject": it.get("subject", ""),
                "question": it.get("question"),
                "asked_by": it.get("asked_by") or it.get("user") or "unknown",
                "resolved": it.get("resolved", False),
            }
        )