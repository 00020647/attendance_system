"""Middleware to attach a simple user role to the request based on group membership
or Django staff/superuser flags.

Roles set on request.user_role:
- 'admin'  : user.is_superuser or user.is_staff
- 'tutor'  : user belongs to group "Tutors"
- 'student': user belongs to group "Students" (or fallback)
- 'anonymous': not authenticated

This allows templates and views to render different content depending on role.
"""

from django.utils.deprecation import MiddlewareMixin


class RoleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        role = 'anonymous'
        user = getattr(request, 'user', None)

        if user and user.is_authenticated:
            try:
                if user.is_superuser or user.is_staff:
                    role = 'admin'
                elif user.groups.filter(name='Tutors').exists():
                    role = 'tutor'
                elif user.groups.filter(name='Students').exists():
                    role = 'student'
                else:
                    # Fallback role for authenticated users without groups
                    role = 'student'
            except Exception:
                # In case auth system not ready, default to anonymous
                role = 'anonymous'

        request.user_role = role
        return None
