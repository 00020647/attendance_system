from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User, Group
from .models import Student, Tutor


class StudentAuthBackend(BaseBackend):
    """Custom authentication backend for students"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            student = Student.objects.get(student_id=username)
            
            if student.check_passport_data(password):
                user, created = User.objects.get_or_create(
                    username=student.student_id,
                    defaults={
                        'first_name': student.first_name,
                        'last_name': student.last_name,
                        'email': student.email,
                    }
                )
                
                students_group, _ = Group.objects.get_or_create(name='Students')
                user.groups.clear()
                user.groups.add(students_group)
                
                return user
        except Student.DoesNotExist:
            pass
        
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class TutorAuthBackend(BaseBackend):
    """Custom authentication backend for tutors"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            tutor = Tutor.objects.get(tutor_id=username)
            
            if tutor.check_password(password):
                user, created = User.objects.get_or_create(
                    username=tutor.tutor_id,
                    defaults={
                        'first_name': tutor.first_name,
                        'last_name': tutor.last_name,
                        'email': tutor.email,
                    }
                )
                
                tutors_group, _ = Group.objects.get_or_create(name='Tutors')
                user.groups.clear()
                user.groups.add(tutors_group)
                
                return user
        except Tutor.DoesNotExist:
            pass
        
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None