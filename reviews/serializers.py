from rest_framework import serializers
from .models import Review
from courses.models import Course
from enrollments.models import Enrollment

class ReviewSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField(read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    # Accept the course ID when creating a review
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), 
        source='course', 
        write_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id', 'course_id', 'course_title', 'student_name', 
            'rating', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}".strip() or obj.student.email

    def validate(self, attrs):
        request = self.context.get('request')
        
        # We only need to run these checks during review creation (POST)
        if request and request.method == 'POST':
            course = attrs.get('course')
            student = request.user

            # 1. Check if the student is enrolled in the course
            is_enrolled = Enrollment.objects.filter(student=student, course=course, is_active=True).exists()
            if not is_enrolled:
                raise serializers.ValidationError({"course_id": "You can only review courses you are currently enrolled in."})

            # 2. Check if the student has already reviewed this course
            if Review.objects.filter(student=student, course=course).exists():
                raise serializers.ValidationError({"course_id": "You have already reviewed this course."})

        return attrs