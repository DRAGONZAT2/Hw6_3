from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsManagerOrAdmin(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["admin", "manager"]

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        elif request.user.role == "manager":
            return hasattr(obj, "manager") and obj.manager == request.user
        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        elif request.user.role == "manager":
             return hasattr(obj, "manager") and obj.manager == request.user
        else:  
            return hasattr(obj, "user") and obj.user == request.user