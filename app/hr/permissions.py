from rest_framework.permissions import BasePermission

class IsHRManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.email == 'hradmin@company.com'
