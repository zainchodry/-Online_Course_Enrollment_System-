from rest_framework import serializers
from .models import Enrollment, Payment, LessonProgress
from courses.models import Course

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'status', 'transaction_id', 'timestamp']
        read_only_fields = ['amount', 'status', 'timestamp']

class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ['id', 'lesson', 'is_completed', 'completed_at']
        read_only_fields = ['completed_at']

class EnrollmentSerializer(serializers.ModelSerializer):
    student_email = serializers.EmailField(source='student.email', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    payment = PaymentSerializer(read_only=True)
    progress = LessonProgressSerializer(many=True, read_only=True)
    
    # Required for creation
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.filter(is_published=True), 
        source='course', 
        write_only=True
    )

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student_email', 'course_id', 'course_title', 
            'enrolled_at', 'is_active', 'completed_at', 'payment', 'progress'
        ]
        read_only_fields = ['enrolled_at', 'is_active', 'completed_at']

    def validate(self, attrs):
        user = self.context['request'].user
        course = attrs['course']
        
        # Check if already enrolled
        if Enrollment.objects.filter(student=user, course=course).exists():
            raise serializers.ValidationError("You are already enrolled in this course.")
        return attrs

    def create(self, validated_data):
        # Create enrollment
        enrollment = super().create(validated_data)
        course = validated_data['course']

        # Automatically generate a Payment record based on course price
        if course.price > 0:
            Payment.objects.create(
                enrollment=enrollment,
                amount=course.price,
                status=Payment.Status.PENDING
            )
        else:
            # Free courses are instantly successful
            Payment.objects.create(
                enrollment=enrollment,
                amount=0.00,
                status=Payment.Status.SUCCESSFUL,
                transaction_id=f"FREE_{enrollment.id}"
            )
            
        return enrollment