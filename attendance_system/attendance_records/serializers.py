from rest_framework import serializers
from .models import Student, Course, AttendanceRecord


class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    # Add attendance statistics
    total_records = serializers.SerializerMethodField()
    attendance_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'first_name', 'last_name', 'full_name',
            'email', 'created_at', 'total_records', 'attendance_percentage'
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
    student_count = serializers.SerializerMethodField()
    total_records = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'student_count', 'total_records']
        read_only_fields = ['id']
    
    def get_total_records(self, obj):
        return obj.attendances.count()


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_detail = StudentSerializer(source='student', read_only=True)
    course_detail = CourseSerializer(source='course', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = AttendanceRecord
        fields = [
            'id', 'student', 'student_detail', 'course', 'course_detail',
            'status', 'status_display', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']