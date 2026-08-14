from rest_framework import serializers
from .models import Category, Course, Module, Lesson
from django.db.models import Avg

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'description']
        read_only_fields = ['slug']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url', 'order', 'is_free_preview']

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'lessons']

class CourseListSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.title', read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'instructor_name', 'category_name', 'price', 'thumbnail', 'is_published', 'average_rating']

    def get_average_rating(self, obj):
            avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
            return round(avg, 1) if avg else 0.0    

class CourseDetailSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    modules = ModuleSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'instructor', 'instructor_name', 
            'category', 'category_id', 'price', 'thumbnail', 'is_published', 
            'created_at', 'updated_at', 'modules', 'average_rating'
        ]
        read_only_fields = ['instructor', 'slug', 'created_at', 'updated_at']

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0.0