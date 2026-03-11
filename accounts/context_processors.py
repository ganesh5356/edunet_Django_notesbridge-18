def user_role(request):
    """Returns the logged-in user's role and, for seniors, how many
    resources they themselves have uploaded.

    This processor is used across all dashboard pages so the sidebar can
    show a personalised count without each view having to compute it.
    """
    if not request.user.is_authenticated:
        return {}

    from accounts.models import Profile
    context = {}
    try:
        profile = Profile.objects.get(user=request.user)
        context["role"] = profile.role
    except Profile.DoesNotExist:
        context["role"] = "junior"

    # only seniors upload resources, so count theirs for sidebar display
    if context.get("role") == "senior":
        try:
            from resources.storage import load_resources
            resources = load_resources()
            count = sum(1 for r in resources if r.get("uploaded_by") == request.user.username)
            context["my_uploads_count"] = count
        except Exception:
            # in case storage can't be imported (e.g. during migrations)
            context["my_uploads_count"] = 0

    return context
