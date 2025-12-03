from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'attendance_records'

urlpatterns = [
    path('', views.index, name='index'),
    
    # Auth routes
    path('login/', auth_views.LoginView.as_view(template_name='attendance_records/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='attendance_records:index'), name='logout'),
    
    # Student dashboard
    path('my-attendance/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    
    # Tutor attendance marking
    path('mark-attendance/', views.TutorMarkAttendanceView.as_view(), name='tutor_mark'),
    
    # Student CRUD
    path('students/', views.StudentListView.as_view(), name='students_list'),
    path('students/add/', views.StudentCreateView.as_view(), name='students_add'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='students_edit'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='students_delete'),
    
    # Tutor CRUD
    path('tutors/', views.TutorListView.as_view(), name='tutors_list'),
    path('tutors/add/', views.TutorCreateView.as_view(), name='tutors_add'),
    path('tutors/<int:pk>/edit/', views.TutorUpdateView.as_view(), name='tutors_edit'),
    path('tutors/<int:pk>/delete/', views.TutorDeleteView.as_view(), name='tutors_delete'),
    
    # Course CRUD
    path('courses/', views.CourseListView.as_view(), name='courses_list'),
    path('courses/add/', views.CourseCreateView.as_view(), name='courses_add'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='courses_edit'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='courses_delete'),
    
    # Attendance CRUD
    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/add/', views.AttendanceCreateView.as_view(), name='attendance_add'),
    path('attendance/<int:pk>/edit/', views.AttendanceUpdateView.as_view(), name='attendance_edit'),
    path('attendance/<int:pk>/delete/', views.AttendanceDeleteView.as_view(), name='attendance_delete'),
]
