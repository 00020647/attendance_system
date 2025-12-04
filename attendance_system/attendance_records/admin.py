from django.contrib import admin
from .models import Student, Course, AttendanceRecord, Tutor


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'created_at')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')
    exclude = ('passport_data',)


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('tutor_id', 'first_name', 'last_name', 'email', 'created_at')
    search_fields = ('tutor_id', 'first_name', 'last_name', 'email')
    filter_horizontal = ('courses',)
    exclude = ('passport_data',) 


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'student', 'course', 'status')
    list_filter = ('course', 'date', 'status')
    search_fields = ('student__first_name', 'student__last_name', 'student__student_id')