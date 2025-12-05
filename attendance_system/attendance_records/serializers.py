# attendance_records/serializers.py
"""
Serializers convert complex data (Django models) into JSON format
and validate incoming data from API requests.
"""

from rest_framework import serializers
from .models import Student, Course, AttendanceRecord


class StudentSerializer(serializers.ModelSerializer):
    """Convert Student model to/from JSON"""
    
    # Add computed field for full name
    full_name = serializers.SerializerMethodField()
    
    # Add attendance statistics
    total_records = serializers.SerializerMethodField()
    attendance_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id',
            'student_id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'created_at',
            'total_records',
            'attendance_percentage'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def get_total_records(self, obj):
        return obj.attendances.count()
    
    def get_attendance_percentage(self, obj):
        total = obj.attendances.count()
        if total == 0:
            return 0
        present = obj.attendances.filter(status='P').count()
        return round((present / total) * 100, 2)


class CourseSerializer(serializers.ModelSerializer):
    """Convert Course model to/from JSON"""
    
    # Add computed field for student count
    student_count = serializers.SerializerMethodField()
    total_records = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id',
            'code',
            'name',
            'student_count',
            'total_records'
        ]
        read_only_fields = ['id']
    
    def get_student_count(self, obj):
        return Student.objects.filter(attendances__course=obj).distinct().count()
    
    def get_total_records(self, obj):
        return obj.attendances.count()


class AttendanceRecordSerializer(serializers.ModelSerializer):
    """Convert AttendanceRecord model to/from JSON"""
    
    # Nested serializers to show full student/course info
    student_detail = StudentSerializer(source='student', read_only=True)
    course_detail = CourseSerializer(source='course', read_only=True)
    
    # Display-friendly status
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = AttendanceRecord
        fields = [
            'id',
            'student',
            'student_detail',
            'course',
            'course_detail',
            'date',
            'status',
            'status_display',
            'notes',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_date(self, value):
        """Ensure date is not in the future"""
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Date cannot be in the future")
        return value


class AttendanceRecordSimpleSerializer(serializers.ModelSerializer):
    """Simplified version without nested data - faster for lists"""
    
    student_name = serializers.CharField(source='student.__str__', read_only=True)
    course_name = serializers.CharField(source='course.__str__', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = AttendanceRecord
        fields = [
            'id',
            'student',
            'student_name',
            'course',
            'course_name',
            'date',
            'status',
            'status_display',
            'notes'
        ]