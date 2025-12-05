# Attendance System - Complete Code Reference

## Quick Overview
Django 4.2.7 attendance management system with:
- **4 Models**: Course, Student, Tutor, AttendanceRecord
- **15+ Views**: CRUD operations + custom dashboard/marking views
- **2 Auth Backends**: StudentAuthBackend, TutorAuthBackend (custom ID + passport_data)
- **3 Roles**: Student, Tutor, Admin (middleware-based role assignment)
- **DB**: MySQL with unique_together constraints

---

## 📊 Models (attendance_records/models.py)

### Course
```python
class Course(models.Model):
    name = CharField(max_length=200)
    code = CharField(max_length=20, unique=True)  # e.g., "CS101"
    # M2M: students, tutors
```

### Student
```python
class Student(models.Model):
    first_name, last_name = CharField(max_length=100)
    student_id = CharField(max_length=30, unique=True)  # Login username
    passport_data = CharField(max_length=128)  # Hashed PBKDF2_SHA256
    email = EmailField(blank=True)
    courses = ManyToManyField(Course)  # Courses enrolled
    created_at = DateTimeField(auto_now_add=True)
    
    def set_passport_data(raw_password):
        """Hash and store"""
        self.passport_data = make_password(raw_password)
    
    def check_passport_data(raw_password):
        """Verify hashed password"""
        return check_password(raw_password, self.passport_data)
```

### Tutor
```python
class Tutor(models.Model):
    # IDENTICAL TO STUDENT but with tutor_id instead of student_id
    first_name, last_name, tutor_id, passport_data, email, courses, created_at
    set_passport_data(), check_passport_data()
```

### AttendanceRecord
```python
class AttendanceRecord(models.Model):
    STATUS_CHOICES = [('P', 'Present'), ('A', 'Absent'), ('E', 'Late')]
    SEMESTER_CHOICES = [(1, 'Semester 1'), (2, 'Semester 2')]
    
    student = ForeignKey(Student, CASCADE, related_name='attendances')
    course = ForeignKey(Course, CASCADE, related_name='attendances')
    semester = IntegerField(choices=SEMESTER_CHOICES, default=1)
    week = IntegerField(1-18)
    status = CharField(max_length=1, choices=STATUS_CHOICES)
    date = DateField(null=True, blank=True)
    notes = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'course', 'semester', 'week')
        # One attendance record per student per course per week
```

---

## 🌐 URLs (attendance_records/urls.py)

```
/                           → index (dashboard)
/login/                     → LoginView (custom backend auth)
/logout/                    → LogoutView
/my-attendance/             → StudentDashboardView (student only)
/mark-attendance/           → TutorMarkAttendanceView (tutor/admin)
/students/                  → StudentListView
/students/add/              → StudentCreateView
/students/<pk>/edit/        → StudentUpdateView
/students/<pk>/delete/      → StudentDeleteView
/tutors/[add/edit/delete]   → Similar CRUD
/courses/[add/edit/delete]  → Admin only
/attendance/[add/edit/delete]→ Tutor/admin only
```

---

## 🔐 Authentication (attendance_records/backends.py)

### StudentAuthBackend
```python
def authenticate(request, username=None, password=None):
    # username = student_id (not email)
    # password = raw passport_data
    try:
        student = Student.objects.get(student_id=username)
        if student.check_passport_data(password):
            # Auto-create Django User if doesn't exist
            user, _ = User.objects.get_or_create(
                username=student.student_id,
                defaults={'first_name': ..., 'last_name': ..., 'email': ...}
            )
            # Add to 'Students' group
            group, _ = Group.objects.get_or_create(name='Students')
            user.groups.clear()
            user.groups.add(group)
            return user
    except Student.DoesNotExist:
        return None
```

### TutorAuthBackend
- **Identical to StudentAuthBackend but:**
- Uses `tutor_id` instead of `student_id`
- Looks up `Tutor` model instead of `Student`
- Adds to 'Tutors' group instead of 'Students'

### Settings Configuration
```python
AUTHENTICATION_BACKENDS = [
    'attendance_records.backends.StudentAuthBackend',
    'attendance_records.backends.TutorAuthBackend',
    'django.contrib.auth.backends.ModelBackend',  # Admin/superuser
]
```

**Login Process:**
1. User enters ID (e.g., "S001") and passport_data
2. Django tries each backend in order
3. If StudentAuthBackend finds match → authenticate
4. Else if TutorAuthBackend finds match → authenticate
5. Else if ModelBackend (username/password) → authenticate
6. User authenticated with appropriate group

---

## 👥 Authorization (attendance_records/middleware.py + views.py)

### RoleMiddleware (middleware.py)
```python
def process_request(request):
    role = 'anonymous'
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            role = 'admin'
        elif request.user.groups.filter(name='Tutors').exists():
            role = 'tutor'
        elif request.user.groups.filter(name='Students').exists():
            role = 'student'
    request.user_role = role
    return None
```
**Result:** `request.user_role` available in all views/templates

### Access Control Mixins (views.py)
```python
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return getattr(self.request, 'user_role', 'anonymous') == 'admin'
    
    def handle_no_permission(self):
        return redirect('attendance_records:login')

class TutorAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user_role = getattr(self.request, 'user_role', 'anonymous')
        return user_role in ('tutor', 'admin')

class RoleContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = getattr(self.request, 'user_role', 'anonymous')
        return context
```

**Usage in Views:**
```python
@method_decorator(login_required, name='dispatch')
class StudentListView(RoleContextMixin, generic.ListView):
    # Available to all authenticated users
    model = Student

@method_decorator(login_required, name='dispatch')
class StudentDeleteView(AdminRequiredMixin, RoleContextMixin, generic.DeleteView):
    # Only admin can delete
    model = Student
```

---

## 📝 Forms (attendance_records/views.py)

### StudentForm & TutorForm (Identical Pattern)
```python
class StudentForm(forms.ModelForm):
    passport_data = CharField(
        widget=PasswordInput(render_value=False),
        help_text="Enter passport data (will be encrypted)",
        required=False
    )
    passport_data_confirm = CharField(
        widget=PasswordInput(render_value=False),
        label="Confirm Passport Data",
        required=False
    )
    
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_id', 'email', 'passport_data', 'courses']
        widgets = {'courses': CheckboxSelectMultiple()}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Editing existing
            self.fields['passport_data'].required = False
            self.fields['passport_data'].help_text = "Leave blank to keep current"
        else:  # Creating new
            self.fields['passport_data'].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        passport_data = cleaned_data.get('passport_data')
        passport_data_confirm = cleaned_data.get('passport_data_confirm')
        
        if not self.instance.pk and not passport_data:
            raise ValidationError("Passport data required for new students")
        
        if passport_data:
            if not passport_data_confirm:
                raise ValidationError("Please confirm passport data")
            if passport_data != passport_data_confirm:
                raise ValidationError("Passport data fields must match")
        
        return cleaned_data
    
    def save(self, commit=True):
        student = super().save(commit=False)
        
        if passport_data := self.cleaned_data.get('passport_data'):
            student.set_passport_data(passport_data)
        
        if commit:
            student.save()
            self.save_m2m()
            
            # Create/update Django User and assign group
            user, _ = User.objects.get_or_create(
                username=student.student_id,
                defaults={'first_name': ..., 'last_name': ..., 'email': ...}
            )
            group, _ = Group.objects.get_or_create(name='Students')
            user.groups.clear()
            user.groups.add(group)
        
        return student
```

### CourseForm
```python
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code']
```

### AttendanceForm
```python
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['student', 'course', 'semester', 'week', 'status', 'notes']
```

---

## 🎯 Key Views

### StudentDashboardView
```python
class StudentDashboardView(RoleContextMixin, TemplateView):
    template_name = 'student_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        
        if course_id := self.request.GET.get('course'):
            course = get_object_or_404(Course, pk=course_id)
            context['selected_course'] = course
            context['attendance_records'] = AttendanceRecord.objects.filter(
                student__student_id=self.request.user.username,
                course=course
            ).order_by('-date')
        
        return context
```

### TutorMarkAttendanceView (GET + POST)
```python
class TutorMarkAttendanceView(TutorAdminRequiredMixin, RoleContextMixin, TemplateView):
    template_name = 'tutor_mark_attendance.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['weeks'] = range(1, 19)
        context['semesters'] = [(1, 'Semester 1'), (2, 'Semester 2')]
        
        if all([
            course_id := self.request.GET.get('course'),
            semester := self.request.GET.get('semester'),
            week := self.request.GET.get('week')
        ]):
            course = get_object_or_404(Course, pk=course_id)
            context['selected_course'] = course
            context['selected_semester'] = int(semester)
            context['selected_week'] = int(week)
            
            # Students enrolled in this course
            context['students'] = Student.objects.filter(
                courses=course
            ).order_by('last_name', 'first_name')
            
            # Existing attendance records (dict by student.id)
            context['attendance_records'] = {
                record.student_id: record
                for record in AttendanceRecord.objects.filter(
                    course=course, semester=semester, week=week
                )
            }
        
        return context
    
    def post(self, request, *args, **kwargs):
        course_id = request.POST.get('course')
        semester = request.POST.get('semester')
        week = request.POST.get('week')
        course = get_object_or_404(Course, pk=course_id)
        
        students = Student.objects.filter(courses=course)
        
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            remove = request.POST.get(f'remove_{student.id}')
            notes = request.POST.get(f'notes_{student.id}', '')
            
            if remove:
                # Delete attendance record if "Remove" button clicked
                AttendanceRecord.objects.filter(
                    student=student, course=course,
                    semester=semester, week=week
                ).delete()
            elif status:
                # Create/update attendance record
                record, _ = AttendanceRecord.objects.get_or_create(
                    student=student, course=course,
                    semester=semester, week=week,
                    defaults={'status': status, 'notes': notes}
                )
                record.status = status
                record.notes = notes
                record.save()
        
        return redirect(f"/mark-attendance/?course={course_id}&semester={semester}&week={week}")
```

---

## 🎨 Templates Structure

### Base Template (base.html)
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <style>
        /* 450+ lines of CSS with gradient purple theme #667eea to #764ba2 */
        .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .btn-primary { background: #667eea; }
        .badge-student { background-color: #667eea; }
        .badge-tutor { background-color: #f093fb; }
        .badge-admin { background-color: #ff6b6b; }
    </style>
</head>
<body>
    <nav class="navbar sticky-top">
        <a href="{% url 'attendance_records:index' %}" class="navbar-brand">
            <i class="bi bi-calendar-check"></i> Attendance System
        </a>
        {% if user.is_authenticated %}
            <span class="badge badge-{{ user_role }}">{{ user_role|upper }}</span>
            <a href="{% url 'attendance_records:logout' %}" class="btn btn-sm btn-light">Logout</a>
        {% endif %}
    </nav>
    
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

### Login Template (login.html)
```html
{% extends 'base.html' %}
{% block title %}Login - Attendance System{% endblock %}
{% block content %}
<div class="login-card">
    <h2><i class="bi bi-calendar-check"></i> Login</h2>
    <form method="post">
        {% csrf_token %}
        <div class="form-group">
            <label>Student/Tutor ID</label>
            <input type="text" name="username" class="form-control" required>
        </div>
        <div class="form-group">
            <label>Passport Data</label>
            <input type="password" name="password" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
    </form>
    {% if form.non_field_errors %}
        <div class="alert alert-danger">{{ form.non_field_errors }}</div>
    {% endif %}
</div>
{% endblock %}
```

### Mark Attendance Template (tutor_mark_attendance.html)
```html
{% extends 'base.html' %}
{% block content %}
<div class="card mb-4">
    <h5>Select Course, Semester, Week</h5>
    <form method="get">
        <select name="course" class="form-select" required>
            {% for course in courses %}
                <option value="{{ course.id }}" {% if selected_course.id == course.id %}selected{% endif %}>
                    {{ course.code }}
                </option>
            {% endfor %}
        </select>
        <button type="submit" class="btn btn-primary">Load Students</button>
    </form>
</div>

{% if selected_course and students %}
    <form method="post">
        {% csrf_token %}
        <input type="hidden" name="course" value="{{ selected_course.id }}">
        <input type="hidden" name="semester" value="{{ selected_semester }}">
        <input type="hidden" name="week" value="{{ selected_week }}">
        
        <table class="table">
            <thead>
                <tr>
                    <th>Student ID</th>
                    <th>Name</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for student in students %}
                    {% with record=attendance_records|get_item:student.id %}
                    <tr>
                        <td>{{ student.student_id }}</td>
                        <td>{{ student.first_name }} {{ student.last_name }}</td>
                        <td>
                            <div class="d-flex gap-2">
                                <div class="form-check">
                                    <input type="radio" name="status_{{ student.id }}" 
                                           id="present_{{ student.id }}" value="P"
                                           {% if record.status == 'P' %}checked{% endif %}>
                                    <label for="present_{{ student.id }}">
                                        <i class="bi bi-check-circle text-success"></i> Present
                                    </label>
                                </div>
                                <div class="form-check">
                                    <input type="radio" name="status_{{ student.id }}" 
                                           id="absent_{{ student.id }}" value="A"
                                           {% if record.status == 'A' %}checked{% endif %}>
                                    <label for="absent_{{ student.id }}">
                                        <i class="bi bi-x-circle text-danger"></i> Absent
                                    </label>
                                </div>
                                <div class="form-check">
                                    <input type="radio" name="status_{{ student.id }}" 
                                           id="excused_{{ student.id }}" value="E"
                                           {% if record.status == 'E' %}checked{% endif %}>
                                    <label for="excused_{{ student.id }}">
                                        <i class="bi bi-exclamation-circle text-warning"></i> Excused
                                    </label>
                                </div>
                                {% if record %}
                                    <button type="submit" name="remove_{{ student.id }}" value="1" 
                                            class="btn btn-sm btn-outline-danger">
                                        <i class="bi bi-trash"></i> Remove
                                    </button>
                                {% endif %}
                            </div>
                        </td>
                    </tr>
                    {% endwith %}
                {% endfor %}
            </tbody>
        </table>
        
        <button type="submit" class="btn btn-success">Save Attendance</button>
    </form>
{% endif %}
{% endblock %}
```

### Custom Template Filter (templatetags/custom_filters.py)
```python
from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary in templates"""
    return dictionary.get(key)
```

---

## 📦 Requirements

```
Django==4.2.7
Pillow==10.1.0
djangorestframework==3.14.0
django-cors-headers==4.3.0
python-decouple==3.8
django-filter==23.3
```

---

## ⚙️ Settings Configuration (settings.py)

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'attendance_records',  # Main app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'attendance_records.middleware.RoleMiddleware',  # Custom role assignment
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'attendance_system',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

AUTHENTICATION_BACKENDS = [
    'attendance_records.backends.StudentAuthBackend',
    'attendance_records.backends.TutorAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SECRET_KEY = 'django-insecure-61iu%@h*h=%g8b%*)agbx!rkcxv!6zew+8w_r%n7^yz0fxrc_#'
DEBUG = True
ALLOWED_HOSTS = ['*']
```

---

## 🚀 How to Use This Reference

When sharing with another AI assistant, provide:

1. **This entire document** - Copy & paste as context
2. **Specific file** - If making changes to one area
3. **The request** - What feature/bug needs fixing

Example prompt for AI assistant:
```
"Here's my Django project structure [paste this document]. 
I need to add pagination to StudentListView. 
The view is in views.py around line 200. 
Can you refactor it?"
```

---

## 🔑 Key Implementation Details

| Aspect | Implementation |
|--------|-----------------|
| **User ID** | student_id or tutor_id (not email) |
| **Password** | Called "passport_data" (hashed PBKDF2_SHA256) |
| **Authentication** | Custom backends, not Django's default |
| **Groups** | Students, Tutors (auto-created on login) |
| **Role Assignment** | Middleware sets request.user_role |
| **Database** | MySQL with pymysql driver |
| **Attendance Key** | unique_together(student, course, semester, week) |
| **Status Values** | 'P' (Present), 'A' (Absent), 'E' (Excused/Late) |
| **CSS Theme** | Bootstrap 5.3.0 + gradient purple (#667eea to #764ba2) |
| **Forms** | Always use forms (StudentForm, TutorForm) not raw saves |

---

**Last Updated:** December 5, 2025  
**Version:** Complete with Remove Attendance feature
