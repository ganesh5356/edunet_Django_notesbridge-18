def user_role(request):
    if not request.user.is_authenticated:
        return {}
    from accounts.models import Profile
    try:
        profile = Profile.objects.get(user=request.user)
        return {"role": profile.role}
    except:
        return {"role": "junior"}
