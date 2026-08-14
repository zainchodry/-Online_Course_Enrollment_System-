from django.contrib import admin
from .models import Enrollment, Payment, LessonProgress

class PaymentInline(admin.StackedInline):
    model = Payment
    can_delete = False

class LessonProgressInline(admin.TabularInline):
    model = LessonProgress
    extra = 0
    readonly_fields = ('completed_at',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'is_active', 'enrolled_at')
    list_filter = ('is_active', 'enrolled_at')
    search_fields = ('student__email', 'course__title')
    inlines = [PaymentInline, LessonProgressInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'amount', 'status', 'transaction_id', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('transaction_id', 'enrollment__student__email')