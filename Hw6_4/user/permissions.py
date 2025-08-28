from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdminPermission(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user.is_authenticated:
            return False
        if getattr(user, "role", "user") == "admin":
            return True
        return getattr(obj, "owner_id", None) == user.id