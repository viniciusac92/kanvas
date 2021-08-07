from rest_framework.permissions import BasePermission


class IsInstructorOrReadOnly(BasePermission):
    def has_permission(self, request, _):
        if request.method == "GET":
            return True

        user = request.user
        return user.is_staff and user.is_superuser


class TeamMemberOnly(BasePermission):
    def has_permission(self, request, _):
        user = request.user
        return user.is_staff


class StudentOnly(BasePermission):
    def has_permission(self, request, _):
        user = request.user
        return not user.is_staff
