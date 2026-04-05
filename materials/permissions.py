from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsModer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Модераторы").exists()
