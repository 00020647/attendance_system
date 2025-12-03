from django.contrib import admin
from .models import Student, Course, AttendanceRecord


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'created_at')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')
    exclude = ('passport_data',)  # Don't show raw hash in admin
    
    def save_model(self, request, obj, form, change):
        # If you want to set passport via admin, you'd need a custom form
        # For now, use the web interface to set passwords
        super().save_model(request, obj, form, change)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'student', 'course', 'status')
    list_filter = ('course', 'date', 'status')
    search_fields = ('student__first_name', 'student__last_name', 'student__student_id')
