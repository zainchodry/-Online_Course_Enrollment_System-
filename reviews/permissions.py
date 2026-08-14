from rest_framework import permissions
from accounts.models import User

class IsReviewAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the author of a review to edit or delete it.
    Admins have full access.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Admin can do anything
        if request.user and request.user.role == User.Roles.ADMIN:
            return True

        # Write permissions are only allowed to the student who created the review
        return obj.student == request.user