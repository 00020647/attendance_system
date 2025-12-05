from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=30, unique=True)
    passport_data = models.CharField(max_length=128, default='')
    email = models.EmailField(blank=True)
    courses = models.ManyToManyField(Course, related_name='students', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    def set_passport_data(self, raw_password):
        """Hash and set the passport data"""
        self.passport_data = make_password(raw_password)

    def check_passport_data(self, raw_password):
        """Verify the passport data"""
        return check_password(raw_password, self.passport_data)


class Tutor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    tutor_id = models.CharField(max_length=30, unique=True)
    passport_data = models.CharField(max_length=128, default='')
    email = models.EmailField(blank=True)
    courses = models.ManyToManyField(Course, related_name='tutors', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.tutor_id})"

    def set_passport_data(self, raw_password):
        """Hash and set the passport data"""
        self.passport_data = make_password(raw_password)

    def check_passport_data(self, raw_password):
        """Verify the passport data"""
        return check_password(raw_password, self.passport_data)


class AttendanceRecord(models.Model):
    STATUS_PRESENT = 'P'
    STATUS_ABSENT = 'A'
    STATUS_EXCUSED = 'E'
    STATUS_CHOICES = [
        (STATUS_PRESENT, 'Present'),
        (STATUS_ABSENT, 'Absent'),
        (STATUS_EXCUSED, 'Excused'),
    ]
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances')
    semester = models.IntegerField(choices=SEMESTER_CHOICES, default=1)
    week = models.IntegerField(help_text='Week number (1-18)')
    date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_PRESENT)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-semester', '-week', 'student']
        unique_together = ('student', 'course', 'semester', 'week')

    def __str__(self):
        return f"Sem {self.semester} Week {self.week} - {self.student} - {self.get_status_display()}"