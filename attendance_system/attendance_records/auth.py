"""Custom authentication backend for student and tutor login using passport data."""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Student, Tutor

User = get_user_model()


class PassportAuthBackend(ModelBackend):
    """
    Authenticate using student_id/passport_data or tutor_id/passport_data.
    Creates a Django user if it doesn't exist.
    """

    def authenticate(self, request, username=None, password=None, user_type=None, **kwargs):
        """
        Authenticate a student or tutor using ID and passport data.
        
        Args:
            request: The request object
            username: The student_id or tutor_id
            password: The passport_data
            user_type: Either 'student' or 'tutor'
        """
        if not username or not password or not user_type:
            return None

        try:
            if user_type == 'student':
                student = Student.objects.get(student_id=username)
                if student.check_passport_data(password):
                    # Try to get or create Django user
                    user, _ = User.objects.get_or_create(
                        username=f"student_{username}",
                        defaults={
                            'email': student.email or '',
                            'first_name': student.first_name,
                            'last_name': student.last_name,
                        }
                    )
                    # Ensure user has 'Students' group
                    from django.contrib.auth.models import Group
                    group, _ = Group.objects.get_or_create(name='Students')
                    user.groups.add(group)
                    return user
            
            elif user_type == 'tutor':
                tutor = Tutor.objects.get(tutor_id=username)
                if tutor.check_passport_data(password):
                    # Try to get or create Django user
                    user, _ = User.objects.get_or_create(
                        username=f"tutor_{username}",
                        defaults={
                            'email': tutor.email or '',
                            'first_name': tutor.first_name,
                            'last_name': tutor.last_name,
                        }
                    )
                    # Ensure user has 'Tutors' group
                    from django.contrib.auth.models import Group
                    group, _ = Group.objects.get_or_create(name='Tutors')
                    user.groups.add(group)
                    return user
        except (Student.DoesNotExist, Tutor.DoesNotExist):
            pass

        return None

    def get_user(self, user_id):
        """Get a user by ID."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
