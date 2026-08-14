from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Course, Module, Lesson
from .serializers import (
    CategorySerializer, CourseListSerializer, CourseDetailSerializer, 
    ModuleSerializer, LessonSerializer
)
from .permissions import IsInstructorOrReadOnly, IsCourseOwnerOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        """Only Admin can create/update/delete categories; anyone can read."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsInstructorOrReadOnly, IsCourseOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['category', 'is_published']
    ordering_fields = ['created_at', 'price']

    def get_queryset(self):
        """
        Students see only published courses. 
        Instructors see published courses PLUS their own drafts.
        """
        user = self.request.user
        if user.is_authenticated and user.role == 'INSTRUCTOR':
            return Course.objects.filter(is_published=True) | Course.objects.filter(instructor=user)
        return Course.objects.filter(is_published=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer

    def perform_create(self, serializer):
        # Automatically assign the logged-in instructor
        serializer.save(instructor=self.request.user)

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsInstructorOrReadOnly, IsCourseOwnerOrReadOnly]

    def get_queryset(self):
        if 'course_pk' in self.kwargs:
            return Module.objects.filter(course_id=self.kwargs['course_pk'])
        return super().get_queryset()

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsInstructorOrReadOnly, IsCourseOwnerOrReadOnly]

    def get_queryset(self):
        if 'module_pk' in self.kwargs:
            return Lesson.objects.filter(module_id=self.kwargs['module_pk'])
        return super().get_queryset()