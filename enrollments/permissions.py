from rest_framework import permissions
from accounts.models import User

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Roles.STUDENT

class IsEnrollmentOwnerOrInstructor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin can access everything
        if request.user.role == User.Roles.ADMIN:
            return True
        # Student can view their own enrollment
        if request.user.role == User.Roles.STUDENT:
            return obj.student == request.user
        # Instructor can view enrollments for their own courses
        if request.user.role == User.Roles.INSTRUCTOR:
            return obj.course.instructor == request.user
            
        return False