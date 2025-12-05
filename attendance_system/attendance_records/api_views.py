from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Student, Course, AttendanceRecord
from .serializers import (
    StudentSerializer,
    CourseSerializer,
    AttendanceRecordSerializer,
)


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Student.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(student_id__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset.order_by('last_name', 'first_name')
    
    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        student = self.get_object()
        records = student.attendances.all().order_by('-created_at')
        course_id = request.query_params.get('course', None)
        if course_id:
            records = records.filter(course_id=course_id)
        serializer = AttendanceRecordSimpleSerializer(records, many=True)
        return Response(serializer.data)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for courses
    - List all courses: GET /api/courses/
    - Get specific course: GET /api/courses/{id}/
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Course.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) |
                Q(name__icontains=search)
            )
        return queryset.order_by('code')
    
    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        course = self.get_object()
        records = course.attendances.all().order_by('-created_at', 'student__last_name')
        date = request.query_params.get('date', None)
        if date:
            records = records.filter(created_at__date=date)
        serializer = AttendanceRecordSimpleSerializer(records, many=True)
        return Response(serializer.data)


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = AttendanceRecord.objects.all()
        student_id = self.request.query_params.get('student', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        course_id = self.request.query_params.get('course', None)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        date = self.request.query_params.get('date', None)
        if date:
            queryset = queryset.filter(created_at__date=date)
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset.order_by('-created_at', 'student__last_name')
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsTutorOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class IsTutorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_staff or
            request.user.is_superuser or
            request.user.groups.filter(name='Tutors').exists()
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_attendance(request):
    try:
        student = Student.objects.get(student_id=request.user.username)
        records = student.attendances.all().order_by('-created_at')
        course_id = request.query_params.get('course', None)
        if course_id:
            records = records.filter(course_id=course_id)
        serializer = AttendanceRecordSerializer(records, many=True)
        return Response({
            'student': StudentSerializer(student).data,
            'attendance_records': serializer.data
        })
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student profile not found for this user'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_stats(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_records = AttendanceRecord.objects.count()
    
    # Calculate attendance rate
    if total_records > 0:
        present_count = AttendanceRecord.objects.filter(status='P').count()
        attendance_rate = round((present_count / total_records) * 100, 2)
    else:
        attendance_rate = 0
    
    return Response({
        'total_students': total_students,
        'total_courses': total_courses,
        'total_attendance_records': total_records,
        'overall_attendance_rate': f'{attendance_rate}%',
        'status_breakdown': {
            'present': AttendanceRecord.objects.filter(status='P').count(),
            'absent': AttendanceRecord.objects.filter(status='A').count(),
            'late': AttendanceRecord.objects.filter(status='L').count(),
        }
    })