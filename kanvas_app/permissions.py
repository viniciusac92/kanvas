from rest_framework.permissions import BasePermission


class SpecificUser(BasePermission):
    def has_permission(self, request, view):
        return
