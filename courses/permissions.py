from rest_framework import permissions
from accounts.models import User

class IsInstructorOrReadOnly(permissions.BasePermission):
    """
    Allows read access to anyone, but only INSTRUCTOR or ADMIN roles can create items.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in [User.Roles.INSTRUCTOR, User.Roles.ADMIN]

class IsCourseOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows read access to anyone. Edit/Delete access restricted to the instructor who owns the course.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Admin can do anything
        if request.user.role == User.Roles.ADMIN:
            return True
            
        # Check if the object is a Course or a child (Module/Lesson)
        if hasattr(obj, 'instructor'):
            return obj.instructor == request.user
        elif hasattr(obj, 'course'):
            return obj.course.instructor == request.user
        elif hasattr(obj, 'module'):
            return obj.module.course.instructor == request.user
            
        return False