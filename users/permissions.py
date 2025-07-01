from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'moderator_profile')

class IsModeratorOrReadOnly(IsModerator):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return False  # Модераторы не могут удалять
        return True
