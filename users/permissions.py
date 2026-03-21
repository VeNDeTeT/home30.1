from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Только модераторы"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='Модераторы').exists()


class IsOwnerOrModerator(permissions.BasePermission):
    """Владелец ИЛИ модератор"""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.groups.filter(name='Модераторы').exists()
