import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.conf import settings

from .forms import ResourceForm
from .storage import (
    load_resources,
    save_resources,
    load_bookmarks,
    save_bookmarks,
    load_doubts,
    save_doubts,
    load_downloads,
    save_downloads
)

from accounts.models import Profile


def _user_role(request):

    if not request.user.is_authenticated:
        return None

    try:
        profile = Profile.objects.get(user=request.user)
        return profile.role
    except Profile.DoesNotExist:
        return "junior"


@login_required
def resource_list(request):

    items = load_resources()
    bookmarks = load_bookmarks()

    q = (request.GET.get("q", "") or "").lower()
    dept = (request.GET.get("department", "") or "").lower()
    sem = request.GET.get("semester", "")
    rtype = request.GET.get("type", "")

    def match(it):
        blob = f'{it.get("title","")} {it.get("subject","")} {it.get("description","")}'.lower()
        if q and q not in blob:
            return False
        if dept and dept != 'all':
            res_dept = it.get("department", "").lower()
            if res_dept != dept and res_dept != 'all':
                return False
        if sem and str(it.get("semester","")) != str(sem):
            return False
        if rtype and it.get("resource_type") != rtype:
            return False
        return True

    filtered = [it for it in items if match(it)]

    return render(
        request,
        "resources/list.html",
        {
            "items": filtered,
            "role": _user_role(request),
            "bookmarks": bookmarks
        }
    )


@login_required
def resource_detail(request, rid):

    items = load_resources()

    for it in items:

        if it.get("id") == rid:

            return render(
                request,
                "resources/detail.html",
                {
                    "item": it,
                    "role": _user_role(request)
                }
            )

    raise Http404("Resource not found")


@login_required
def upload_resource(request):

    role = _user_role(request)

    if role != "senior":
        messages.error(request, "Only Seniors can upload resources.")
        return redirect("resource_list")

    if request.method == "POST":

        form = ResourceForm(request.POST, request.FILES)

        if form.is_valid():

            items = load_resources()
            resource_id = uuid.uuid4().hex
            file_url = ""

            if "file" in request.FILES:
                f = request.FILES["file"]
                ext = f.name.split(".")[-1] if "." in f.name else "bin"
                fname = f"{uuid.uuid4().hex}.{ext}"
                rel_path = f"uploads/{fname}"
                abs_path = settings.MEDIA_ROOT / rel_path
                abs_path.parent.mkdir(parents=True, exist_ok=True)
                with open(abs_path, "wb+") as dest:
                    for chunk in f.chunks():
                        dest.write(chunk)
                file_url = settings.MEDIA_URL + rel_path

            items.insert(0, {
                "id": resource_id,
                "title": form.cleaned_data["title"],
                "description": form.cleaned_data["description"],
                "department": form.cleaned_data["department"],
                "semester": form.cleaned_data["semester"],
                "subject": form.cleaned_data["subject"],
                "resource_type": form.cleaned_data["resource_type"],
                "file_url": file_url,
                "external_url": form.cleaned_data.get("external_url", ""),
                "uploaded_by": request.user.username,
            })

            save_resources(items)

            messages.success(request, "Resource uploaded successfully!")

            return redirect("resource_list")

    else:

        form = ResourceForm()

    return render(
        request,
        "resources/upload.html",
        {
            "form": form,
            "role": role
        }
    )


@login_required
def bookmark_resource(request, rid):

    bookmarks = load_bookmarks()

    for b in bookmarks:

        if b["user"] == request.user.username and b["resource_id"] == rid:

            messages.info(request, "Already bookmarked!")
            return redirect("resource_list")

    bookmarks.append({
        "user": request.user.username,
        "resource_id": rid
    })

    save_bookmarks(bookmarks)

    messages.success(request, "Resource bookmarked!")

    return redirect("resource_list")


@login_required
def remove_bookmark(request, rid):

    bookmarks = load_bookmarks()

    bookmarks = [
        b for b in bookmarks
        if not (
            b["user"] == request.user.username
            and b["resource_id"] == rid
        )
    ]

    save_bookmarks(bookmarks)

    messages.success(request, "Bookmark removed!")

    return redirect("resource_list")


@login_required
def bookmark_list(request):

    role = _user_role(request)

    bookmarks = load_bookmarks()
    resources = load_resources()

    user_bookmarks = [
        b["resource_id"]
        for b in bookmarks
        if b["user"] == request.user.username
    ]

    items = [
        r for r in resources
        if r["id"] in user_bookmarks
    ]

    return render(
        request,
        "resources/bookmarks.html",
        {
            "items": items,
            "role": role
        }
    )


# =========================
# DOUBT SYSTEM
# =========================

@login_required
def ask_doubt(request):

    role = _user_role(request)

    doubts = load_doubts()

    if request.method == "POST" and role == "junior":

        question = request.POST.get("question", "").strip()

        if not question:
            messages.error(request, "Question cannot be empty.")
            return redirect("ask_doubt")

        doubts.insert(0, {
            "id": uuid.uuid4().hex,
            "question": question,
            "asked_by": request.user.username,
            "replies": [],
            "resolved": False
        })

        save_doubts(doubts)

        messages.success(request, "Doubt posted successfully!")

        return redirect("ask_doubt")

    if role == "junior":
        doubts = [d for d in doubts if d["asked_by"] == request.user.username]

    return render(
        request,
        "resources/doubts.html",
        {
            "doubts": doubts,
            "role": role
        }
    )


@login_required
def reply_doubt(request, did):

    role = _user_role(request)

    if role != "senior":
        return redirect("ask_doubt")

    if request.method == "POST":

        message = request.POST.get("message", "").strip()

        doubts = load_doubts()

        for d in doubts:

            if d["id"] == did and not d.get("resolved"):

                d["replies"].append({
                    "user": request.user.username,
                    "message": message
                })

        save_doubts(doubts)

    return redirect("ask_doubt")


@login_required
def resolve_doubt(request, did):

    role = _user_role(request)

    if role != "junior":
        return redirect("ask_doubt")

    doubts = load_doubts()

    for d in doubts:

        if d["id"] == did and d["asked_by"] == request.user.username:

            d["resolved"] = True

    save_doubts(doubts)

    messages.success(request, "Doubt marked as resolved!")

    return redirect("ask_doubt")

@login_required
def track_download(request, rid):
    items = load_resources()
    resource = None
    for it in items:
        if it.get("id") == rid:
            resource = it
            break
    
    if not resource:
        raise Http404("Resource not found")
    
    downloads = load_downloads()
    downloads.append({
        "resource_id": rid,
        "user": request.user.username,
        "timestamp": uuid.uuid4().hex[:8],
        "date": uuid.uuid4().hex[:6]
    })
    save_downloads(downloads)
    
    return redirect(resource.get("file_url"))


@login_required
def dashboard(request):
    role = _user_role(request)
    resources = load_resources()
    bookmarks = load_bookmarks()
    doubts = load_doubts()
    downloads = load_downloads()
    
    user_name = request.user.username
    
    # Global Stats
    total_resources = len(resources)
    
    if role == "senior":
        # Senior specific
        my_resources = [r for r in resources if r.get("uploaded_by") == user_name]
        my_resource_ids = [r["id"] for r in my_resources]
        
        # How many bookmarked my notes
        bookmarks_on_my_notes = [b for b in bookmarks if b.get("resource_id") in my_resource_ids]
        
        # Total downloads of my notes
        downloads_of_my_notes = [d for d in downloads if d.get("resource_id") in my_resource_ids]
        
        # Doubts asked and resolved (Global for Seniors to see what needs attention)
        total_doubts_asked = len(doubts)
        total_doubts_resolved = len([d for d in doubts if d.get("resolved")])
        
        stats = {
            "total_resources": total_resources,
            "bookmarks_on_my_notes": len(bookmarks_on_my_notes),
            "total_downloads": len(downloads_of_my_notes),
            "total_doubts_asked": total_doubts_asked,
            "total_doubts_resolved": total_doubts_resolved,
        }
    else:
        # Junior specific
        my_bookmarks = [b for b in bookmarks if b.get("user") == user_name]
        
        # Total downloads (how many times I downloaded)
        my_downloads = [d for d in downloads if d.get("user") == user_name]
        
        # My doubts
        my_doubts = [d for d in doubts if d.get("asked_by") == user_name]
        my_doubts_resolved = [d for d in my_doubts if d.get("resolved")]
        
        stats = {
            "total_resources": total_resources,
            "my_bookmarks": len(my_bookmarks),
            "my_downloads": len(my_downloads),
            "my_doubts_asked": len(my_doubts),
            "my_doubts_resolved": len(my_doubts_resolved),
        }
    
    # Filtering for items if search is used
    q = (request.GET.get("q", "") or "").lower()
    dept = (request.GET.get("department", "") or "").lower()
    sem = request.GET.get("semester", "")
    
    is_search = bool(q or dept or sem)
    display_resources = resources

    if is_search:
        def match(it):
            blob = f'{it.get("title","")} {it.get("subject","")} {it.get("description","")}'.lower()
            if q and q not in blob: return False
            if dept and dept != 'all':
                res_dept = it.get("department", "").lower()
                if res_dept != dept and res_dept != 'all':
                    return False
            if sem and str(it.get("semester","")) != str(sem): return False
            return True
        display_resources = [it for it in resources if match(it)]
    else:
        # If no search, just show recent 10
        display_resources = resources[:10]

    return render(
        request,
        "resources/dashboard.html",
        {
            "role": role,
            "stats": stats,
            "recent_resources": display_resources,
            "is_search": is_search,
        }
    )
