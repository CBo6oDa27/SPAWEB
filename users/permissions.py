from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверка на доступ к объекту только для владельца."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
