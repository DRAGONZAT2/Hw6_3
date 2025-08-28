from rest_framework import permissions


class IsOwnerOrAdminPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user or request.user.role == 'admin'
        return obj == request.user or request.user.role == 'admin'