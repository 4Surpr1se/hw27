from rest_framework import permissions

from ads.models import User


class SelectionPermission(permissions.BasePermission):
    message = 'Adding podboro4ki in not your profile is not allowed.'

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET' or int(request.user.id) == int(obj.owner.id):
            return True
        return False


class DeleteOrUpdateAdPermission(permissions.BasePermission):
    message = 'DENIED'

    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.user.id or request.user.role in [User.moderator, User.admin]:
            return True
        return False
