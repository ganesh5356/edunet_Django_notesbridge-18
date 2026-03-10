import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from resources.models import Resource, Bookmark, Doubt, Download
from datetime import datetime
import django.utils.timezone as timezone

class Command(BaseCommand):
    help = 'Syncs data from JSON files to the Database for Admin view'

    def handle(self, *args, **options):
        base_dir = Path(settings.BASE_DIR)
        
        # 1. Sync Resources
        resource_file = base_dir / "resources" / "data" / "resources.json"
        if resource_file.exists():
            data = json.loads(resource_file.read_text(encoding="utf-8"))
            for item in data:
                user = User.objects.filter(username=item.get("uploaded_by")).first()
                if not user:
                    user = User.objects.filter(is_superuser=True).first()
                
                Resource.objects.update_or_create(
                    id=item.get("id"),
                    defaults={
                        "title": item.get("title"),
                        "description": item.get("description"),
                        "department": item.get("department"),
                        "semester": item.get("semester"),
                        "subject": item.get("subject"),
                        "resource_type": item.get("resource_type"),
                        "file": item.get("file_path", ""),
                        "uploaded_by": user,
                    }
                )
            self.stdout.write(self.style.SUCCESS(f'Synced {len(data)} resources'))

        # 2. Sync Doubts
        doubt_file = base_dir / "resources" / "data" / "doubts.json"
        if doubt_file.exists():
            data = json.loads(doubt_file.read_text(encoding="utf-8"))
            for item in data:
                Doubt.objects.update_or_create(
                    id=item.get("id"),
                    defaults={
                        "subject": item.get("subject", ""),
                        "question": item.get("question"),
                        "asked_by": item.get("asked_by") or item.get("user") or "unknown",
                        "resolved": item.get("resolved", False),
                    }
                )
            self.stdout.write(self.style.SUCCESS(f'Synced {len(data)} doubts'))

        # 3. Sync Bookmarks
        bookmark_file = base_dir / "resources" / "data" / "bookmarks.json"
        if bookmark_file.exists():
            data = json.loads(bookmark_file.read_text(encoding="utf-8"))
            for item in data:
                user = User.objects.filter(username=item.get("user")).first()
                resource = Resource.objects.filter(id=item.get("resource_id")).first()
                if user and resource:
                    Bookmark.objects.get_or_create(
                        user=user,
                        resource=resource
                    )
            self.stdout.write(self.style.SUCCESS(f'Synced {len(data)} bookmarks'))

        # 4. Sync Downloads
        download_file = base_dir / "resources" / "data" / "downloads.json"
        if download_file.exists():
            data = json.loads(download_file.read_text(encoding="utf-8"))
            for item in data:
                Download.objects.get_or_create(
                    resource_id=item.get("resource_id"),
                    user=item.get("user"),
                )
            self.stdout.write(self.style.SUCCESS(f'Synced {len(data)} downloads'))

        self.stdout.write(self.style.SUCCESS('Data sync to Admin complete!'))
