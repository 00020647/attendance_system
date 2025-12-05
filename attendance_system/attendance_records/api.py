from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, Tutor, Course, AttendanceRecord
from .serializers import StudentSerializer, TutorSerializer, CourseSerializer, AttendanceRecordSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Allow users to see all students (adjust based on your needs)
        return Student.objects.all()

    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get attendance records for a specific student"""
        student = self.get_object()
        attendance_records = AttendanceRecord.objects.filter(student=student)
        serializer = AttendanceRecordSerializer(attendance_records, many=True)
        return Response(serializer.data)


class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tutor.objects.all()

    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        """Get courses taught by a specific tutor"""
        tutor = self.get_object()
        courses = tutor.courses.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Course.objects.all()

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get students enrolled in a specific course"""
        course = self.get_object()
        students = course.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def tutors(self, request, pk=None):
        """Get tutors teaching a specific course"""
        course = self.get_object()
        tutors = course.tutors.all()
        serializer = TutorSerializer(tutors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get attendance records for a specific course"""
        course = self.get_object()
        attendance_records = AttendanceRecord.objects.filter(course=course)
        
        # Optional filtering by semester and week
        semester = request.query_params.get('semester')
        week = request.query_params.get('week')
        
        if semester:
            attendance_records = attendance_records.filter(semester=semester)
        if week:
            attendance_records = attendance_records.filter(week=week)
            
        serializer = AttendanceRecordSerializer(attendance_records, many=True)
        return Response(serializer.data)


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = AttendanceRecord.objects.all()
        
        # Filter by student_id if provided
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student__student_id=student_id)
        
        # Filter by course_code if provided
        course_code = self.request.query_params.get('course_code')
        if course_code:
            queryset = queryset.filter(course__code=course_code)
        
        # Filter by semester if provided
        semester = self.request.query_params.get('semester')
        if semester:
            queryset = queryset.filter(semester=semester)
        
        # Filter by week if provided
        week = self.request.query_params.get('week')
        if week:
            queryset = queryset.filter(week=week)
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')
