import json
from pathlib import Path
from django.conf import settings

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


def load_resources():
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text("[]", encoding="utf-8")
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_resources(items):
    DATA_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")


def load_bookmarks():
    if not BOOKMARK_FILE.exists():
        BOOKMARK_FILE.parent.mkdir(parents=True, exist_ok=True)
        BOOKMARK_FILE.write_text("[]", encoding="utf-8")
    return json.loads(BOOKMARK_FILE.read_text(encoding="utf-8"))


def save_bookmarks(items):
    BOOKMARK_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")


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