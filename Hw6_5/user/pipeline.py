def save_user_role(strategy, details, backend, user=None, *args, **kwargs):
    
    if user and not user.role:
        user.role = "user"
        user.save()
    return {"user": user}