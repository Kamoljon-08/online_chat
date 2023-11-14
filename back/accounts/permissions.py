from rest_framework import permissions

class IsAuthorOrReadOnly (permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser 

