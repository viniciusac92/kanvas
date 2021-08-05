from rest_framework.permissions import BasePermission


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        import ipdb

        ipdb.set_trace()
        return user.is_admin
