from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import Student, Course, AttendanceRecord
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_id', 'email', 'courses']
        widgets = {
            'courses': forms.CheckboxSelectMultiple(),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['student', 'course', 'semester', 'week', 'status', 'notes']


class RoleContextMixin:
    """Mixin to add request.user_role into template context for class-based views."""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = getattr(self.request, 'user_role', 'anonymous')
        return context


class TutorAdminRequiredMixin(UserPassesTestMixin):
    """Restrict access to tutors and admins only."""
    def test_func(self):
        user_role = getattr(self.request, 'user_role', 'anonymous')
        return user_role in ('tutor', 'admin')

    def handle_no_permission(self):
        return redirect('attendance_records:login')


class AdminRequiredMixin(UserPassesTestMixin):
    """Restrict access to admins only."""
    def test_func(self):
        user_role = getattr(self.request, 'user_role', 'anonymous')
        return user_role == 'admin'

    def handle_no_permission(self):
        return redirect('attendance_records:login')


@method_decorator(login_required(login_url='attendance_records:login'), name='dispatch')
class StudentListView(RoleContextMixin, generic.ListView):
    model = Student
    template_name = 'attendance_records/student_list.html'
    context_object_name = 'students'


@method_decorator(login_required(login_url='attendance_records:login'), name='dispatch')
class StudentCreateView(TutorAdminRequiredMixin, RoleContextMixin, generic.CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'attendance_records/student_form.html'
    success_url = reverse_lazy('attendance_records:students_list')


@method_decorator(login_required(login_url='attendance_records:login'), name='dispatch')
class StudentUpdateView(TutorAdminRequiredMixin, RoleContextMixin, generic.UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'attendance_records/student_form.html'
    success_url = reverse_lazy('attendance_records:students_list')


@method_decorator(login_required(login_url='attendance_records:login'), name='dispatch')
class StudentDeleteView(AdminRequiredMixin, RoleContextMixin, generic.DeleteView):
    model = Student
    template_name = 'attendance_records/student_confirm_delete.html'
    success_url = reverse_lazy('attendance_records:students_list')


@method_decorator(login_required(login_url='attendance_records:login'), name='dispatch')
class AttendanceListView(RoleContextMixin, generic.ListView):
    model = AttendanceRecord
    template_name = 'attendance_records/attendance_list.html'
    context_object_name = 'records'


@method_decorator(login_required(login_url='attendance_records:login'), name='dispatch')
class AttendanceCreateView(TutorAdminRequiredMixin, RoleContextMixin, generic.CreateView):
    model = AttendanceRecord
    form_class = AttendanceForm
    template_name = 'attendance_records/attendance_form.html'
    success_url = reverse_lazy('attendance_records:attendance_list')


@method_decorator(login_required(login_url='attendance_records:login'), name='dispatch')
class AttendanceUpdateView(TutorAdminRequiredMixin, RoleContextMixin, generic.UpdateView):
    model = AttendanceRecord
    form_class = AttendanceForm
    template_name = 'attendance_records/attendance_form.html'
    success_url = reverse_lazy('attendance_records:attendance_list')


@method_decorator(login_required(login_url='attendance_records:login'), name='dispatch')
class AttendanceDeleteView(AdminRequiredMixin, RoleContextMixin, generic.DeleteView):
    model = AttendanceRecord
    template_name = 'attendance_records/attendance_confirm_delete.html'
    success_url = reverse_lazy('attendance_records:attendance_list')


def index(request):
    return render(request, 'attendance_records/index.html')


@method_decorator(login_required(login_url='attendance_records:login'), name='dispatch')
class StudentDashboardView(RoleContextMixin, generic.TemplateView):
    template_name = 'attendance_records/student_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.request.GET.get('course')
        courses = Course.objects.all()
        context['courses'] = courses
        context['selected_course'] = None

        if course_id:
            selected_course = get_object_or_404(Course, pk=course_id)
            context['selected_course'] = selected_course
            records = AttendanceRecord.objects.filter(
                student__student_id=self.request.user.username,
                course=selected_course
            ).order_by('-date')
            context['attendance_records'] = records

        return context


@method_decorator(login_required(login_url='attendance_records:login'), name='dispatch')
class TutorMarkAttendanceView(TutorAdminRequiredMixin, RoleContextMixin, generic.TemplateView):
    template_name = 'attendance_records/tutor_mark_attendance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.all()
        context['courses'] = courses
        context['selected_course'] = None
        context['students'] = []
        context['weeks'] = range(1, 19)  # 18 weeks
        context['semesters'] = [(1, 'Semester 1'), (2, 'Semester 2')]

        course_id = self.request.GET.get('course')
        semester = self.request.GET.get('semester')
        week = self.request.GET.get('week')

        if course_id and semester and week:
            selected_course = get_object_or_404(Course, pk=course_id)
            context['selected_course'] = selected_course
            context['selected_semester'] = int(semester)
            context['selected_week'] = int(week)
            
            # Filter students who are enrolled in the selected course
            students = Student.objects.filter(
                courses=selected_course
            ).order_by('last_name', 'first_name')
            
            context['students'] = students
            context['attendance_records'] = {
                record.student_id: record
                for record in AttendanceRecord.objects.filter(
                    course=selected_course,
                    semester=semester,
                    week=week
                )
            }

        return context

    def post(self, request, *args, **kwargs):
        course_id = request.POST.get('course')
        semester = request.POST.get('semester')
        week = request.POST.get('week')
        course = get_object_or_404(Course, pk=course_id)

        # Filter students who are enrolled in this course
        students = Student.objects.filter(courses=course)
        
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            notes = request.POST.get(f'notes_{student.id}', '')

            if status:
                record, _ = AttendanceRecord.objects.get_or_create(
                    student=student,
                    course=course,
                    semester=semester,
                    week=week,
                    defaults={'status': status, 'notes': notes}
                )
                record.status = status
                record.notes = notes
                record.save()

        return redirect(f"{reverse_lazy('attendance_records:tutor_mark')}?course={course_id}&semester={semester}&week={week}")


@method_decorator(login_required(login_url='attendance_records:login'), name='dispatch')
class CourseListView(AdminRequiredMixin, RoleContextMixin, generic.ListView):
    model = Course
    template_name = 'attendance_records/course_list.html'
    context_object_name = 'courses'


@method_decorator(login_required(login_url='attendance_records:login'), name='dispatch')
class CourseCreateView(AdminRequiredMixin, RoleContextMixin, generic.CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'attendance_records/course_form.html'
    success_url = reverse_lazy('attendance_records:courses_list')


@method_decorator(login_required(login_url='attendance_records:login'), name='dispatch')
class CourseUpdateView(AdminRequiredMixin, RoleContextMixin, generic.UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'attendance_records/course_form.html'
    success_url = reverse_lazy('attendance_records:courses_list')


@method_decorator(login_required(login_url='attendance_records:login'), name='dispatch')
class CourseDeleteView(AdminRequiredMixin, RoleContextMixin, generic.DeleteView):
    model = Course
    template_name = 'attendance_records/course_confirm_delete.html'
    success_url = reverse_lazy('attendance_records:courses_list')
