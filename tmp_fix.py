import os

profile_css_path = r"c:\Users\khami\OneDrive\Documents\notesbridge django\static\css\pages\profile.css"
views_py_path = r"c:\Users\khami\OneDrive\Documents\notesbridge django\resources\views.py"

profile_append = """
.profile-img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  border: 4px solid white;
  box-shadow: var(--shadow-md);
  margin: var(--spacing-md) auto;
  display: block;
}
"""

views_append = """

@login_required
def dashboard(request):
    role = _user_role(request)
    resources = load_resources()
    bookmarks = load_bookmarks()

    # Calculate stats
    total_resources = len(resources)
    user_resources = [r for r in resources if r.get("uploaded_by") == request.user.username]
    user_bookmarks = [b for b in bookmarks if b.get("user") == request.user.username]

    return render(
        request,
        "resources/dashboard.html",
        {
            "role": role,
            "total_resources": total_resources,
            "user_uploads": len(user_resources),
            "user_bookmarks": len(user_bookmarks),
            "recent_resources": resources[:5],
        }
    )
"""

with open(profile_css_path, "a") as f:
    f.write(profile_append)

with open(views_py_path, "a") as f:
    f.write(views_append)

print("Successfully appended content to files.")
