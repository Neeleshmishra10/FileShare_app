from rest_framework.permissions import BasePermission

from rest_framework import permissions

class IsOpsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_uploader

class IsClientUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_client


class IsClientUser(permissions.BasePermission):
    """
    Custom permission to allow access only to client users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client