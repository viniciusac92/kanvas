from rest_framework.permissions import BasePermission


class IsInstructorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        user = request.user
        return user.is_staff and user.is_superuser
