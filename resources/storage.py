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