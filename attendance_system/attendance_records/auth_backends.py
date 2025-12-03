from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User, Group
from .models import Student


class StudentAuthBackend(BaseBackend):
    """
    Custom authentication backend for students using student_id and passport_data
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Find student by student_id
            student = Student.objects.get(student_id=username)
            
            # Verify passport_data
            if student.check_passport_data(password):
                # Get or create a Django User for this student
                user, created = User.objects.get_or_create(
                    username=student.student_id,
                    defaults={
                        'first_name': student.first_name,
                        'last_name': student.last_name,
                        'email': student.email,
                    }
                )
                
                # Add user to Students group
                students_group, _ = Group.objects.get_or_create(name='Students')
                user.groups.add(students_group)
                
                return user
        except Student.DoesNotExist:
            return None
        
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None