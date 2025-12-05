# attendance_records/urls.py

from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views

app_name = 'attendance_records'

# API Router - automatically creates routes for viewsets
router = DefaultRouter()
router.register(r'students', api_views.StudentViewSet, basename='api-student')
router.register(r'courses', api_views.CourseViewSet, basename='api-course')
router.register(r'attendance', api_views.AttendanceRecordViewSet, basename='api-attendance')

urlpatterns = [
    # Web Interface Routes
    path('', views.index, name='index'),
    
    # Auth routes
    path('login/', auth_views.LoginView.as_view(template_name='attendance_records/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='attendance_records:index'), name='logout'),

    # Student dashboard
    path('my-attendance/', views.StudentDashboardView.as_view(), name='student_dashboard'),

    # Tutor attendance marking
    path('mark-attendance/', views.TutorMarkAttendanceView.as_view(), name='tutor_mark'),

    # Admin CRUD - Students
    path('students/', views.StudentListView.as_view(), name='students_list'),
    path('students/add/', views.StudentCreateView.as_view(), name='students_add'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='students_edit'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='students_delete'),

    # Admin CRUD - Tutors
    path('tutors/', views.TutorListView.as_view(), name='tutors_list'),
    path('tutors/add/', views.TutorCreateView.as_view(), name='tutors_add'),
    path('tutors/<int:pk>/edit/', views.TutorUpdateView.as_view(), name='tutors_edit'),
    path('tutors/<int:pk>/delete/', views.TutorDeleteView.as_view(), name='tutors_delete'),

    # Admin CRUD - Courses
    path('courses/', views.CourseListView.as_view(), name='courses_list'),
    path('courses/add/', views.CourseCreateView.as_view(), name='courses_add'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='courses_edit'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='courses_delete'),

    # Admin CRUD - Attendance
    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/add/', views.AttendanceCreateView.as_view(), name='attendance_add'),
    path('attendance/<int:pk>/edit/', views.AttendanceUpdateView.as_view(), name='attendance_edit'),
    path('attendance/<int:pk>/delete/', views.AttendanceDeleteView.as_view(), name='attendance_delete'),
    
    # API Routes
    path('api/', include(router.urls)),
    path('api/my-attendance/', api_views.my_attendance, name='api-my-attendance'),
    path('api/stats/', api_views.api_stats, name='api-stats'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]