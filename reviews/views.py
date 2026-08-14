from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsReviewAuthorOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('student', 'course').all()
    serializer_class = ReviewSerializer
    
    # Anyone can view reviews, but you must be authenticated to create one,
    # and you must be the author to edit/delete it.
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsReviewAuthorOrReadOnly
    ]
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'rating']
    ordering_fields = ['created_at', 'rating']
    
    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the author of the review
        serializer.save(student=self.request.user)