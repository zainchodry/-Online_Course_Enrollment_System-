from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Enrollment, LessonProgress
from .serializers import EnrollmentSerializer, LessonProgressSerializer
from .permissions import IsEnrollmentOwnerOrInstructor
from accounts.models import User
from courses.models import Lesson

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsEnrollmentOwnerOrInstructor]

    def get_queryset(self):
        user = self.request.user
        
        if user.role == User.Roles.STUDENT:
            return Enrollment.objects.filter(student=user)
        elif user.role == User.Roles.INSTRUCTOR:
            # Instructors see all enrollments for their own courses
            return Enrollment.objects.filter(course__instructor=user)
        elif user.role == User.Roles.ADMIN:
            return Enrollment.objects.all()
            
        return Enrollment.objects.none()

    def perform_create(self, serializer):
        # Force the logged-in user as the student
        serializer.save(student=self.request.user)

    def create(self, request, *args, **kwargs):
        # Only students can trigger enrollments
        if request.user.role != User.Roles.STUDENT:
            return Response(
                {"detail": "Only students can enroll in courses."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['patch'])
    def update_progress(self, request, pk=None):
        """
        Custom endpoint for students to mark a lesson as complete.
        URL: /api/enrollments/<id>/update_progress/
        Payload: {"lesson_id": 5, "is_completed": true}
        """
        enrollment = self.get_object()
        
        if request.user != enrollment.student:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        lesson_id = request.data.get('lesson_id')
        is_completed = request.data.get('is_completed', True)

        try:
            lesson = Lesson.objects.get(id=lesson_id, module__course=enrollment.course)
        except Lesson.DoesNotExist:
            return Response({"detail": "Lesson not found in this course."}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create the progress tracker for this specific lesson
        progress, created = LessonProgress.objects.get_or_create(
            enrollment=enrollment, 
            lesson=lesson
        )
        
        progress.is_completed = is_completed
        progress.completed_at = timezone.now() if is_completed else None
        progress.save()

        return Response(LessonProgressSerializer(progress).data, status=status.HTTP_200_OK)