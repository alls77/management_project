from rest_framework import permissions


class IsReviewer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Reviewers').exists()
