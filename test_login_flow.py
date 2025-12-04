#!/usr/bin/env python
"""
Test script to verify the complete login flow for tutors and students.
This simulates what a user would do: create a tutor/student in admin, then login.

Run with: python manage.py shell < test_login_flow.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from attendance_records.models import Tutor, Student
from attendance_records.auth_backends import TutorAuthBackend, StudentAuthBackend
from django.contrib.auth.models import User, Group

print("=" * 70)
print("TESTING COMPLETE LOGIN FLOW")
print("=" * 70)

# Simulate creating a tutor through admin form
print("\n1. SIMULATING TUTOR CREATION VIA ADMIN FORM")
print("-" * 70)

# Create the tutor directly (simulating what the admin form does)
tutor, created = Tutor.objects.get_or_create(
    tutor_id='LOGIN_TEST_T001',
    defaults={
        'first_name': 'Login',
        'last_name': 'Tester',
        'email': 'login.tester@tutor.com'
    }
)

# Set passport data (simulating form submission)
admin_entered_passport = 'AdminEnteredPassword123!'
tutor.set_passport_data(admin_entered_passport)
tutor.save()

print(f"✓ Tutor created via admin:")
print(f"  - Tutor ID: {tutor.tutor_id}")
print(f"  - Name: {tutor.first_name} {tutor.last_name}")
print(f"  - Email: {tutor.email}")
print(f"  - Passport: (hashed - {tutor.passport_data[:40]}...)")

# The admin form should have also created the Django user
django_user = User.objects.get(username=tutor.tutor_id)
print(f"\n✓ Django User created automatically:")
print(f"  - Username: {django_user.username}")
print(f"  - First Name: {django_user.first_name}")
print(f"  - Groups: {list(django_user.groups.values_list('name', flat=True))}")

# Now test login with the SAME credentials
print("\n2. TESTING LOGIN WITH CREDENTIALS FROM ADMIN FORM")
print("-" * 70)

backend = TutorAuthBackend()

class MockRequest:
    pass

request = MockRequest()

# Try to login using the tutor_id and passport_data that admin entered
auth_user = backend.authenticate(
    request,
    username=tutor.tutor_id,  # Use the tutor_id
    password=admin_entered_passport  # Use the passport data they entered
)

if auth_user:
    print(f"✓ LOGIN SUCCESSFUL!")
    print(f"  - Username: {auth_user.username}")
    print(f"  - Full Name: {auth_user.first_name} {auth_user.last_name}")
    print(f"  - Groups: {list(auth_user.groups.values_list('name', flat=True))}")
else:
    print(f"✗ LOGIN FAILED!")
    print(f"  - Could not authenticate with provided credentials")

# Test with wrong password
auth_user_wrong = backend.authenticate(
    request,
    username=tutor.tutor_id,
    password='WrongPassword123!'
)

if auth_user_wrong is None:
    print(f"\n✓ Wrong password correctly rejected")
else:
    print(f"\n✗ ERROR: Wrong password was accepted!")

# Now test student login flow
print("\n3. SIMULATING STUDENT CREATION VIA ADMIN FORM")
print("-" * 70)

student, created = Student.objects.get_or_create(
    student_id='LOGIN_TEST_S001',
    defaults={
        'first_name': 'Student',
        'last_name': 'Logintest',
        'email': 'student.logintest@example.com'
    }
)

admin_entered_student_passport = 'StudentPassport456!'
student.set_passport_data(admin_entered_student_passport)
student.save()

print(f"✓ Student created via admin:")
print(f"  - Student ID: {student.student_id}")
print(f"  - Name: {student.first_name} {student.last_name}")
print(f"  - Passport: (hashed - {student.passport_data[:40]}...)")

django_user_student = User.objects.get(username=student.student_id)
print(f"\n✓ Django User created automatically:")
print(f"  - Username: {django_user_student.username}")
print(f"  - Groups: {list(django_user_student.groups.values_list('name', flat=True))}")

# Test student login
print("\n4. TESTING STUDENT LOGIN")
print("-" * 70)

student_backend = StudentAuthBackend()

auth_student = student_backend.authenticate(
    request,
    username=student.student_id,
    password=admin_entered_student_passport
)

if auth_student:
    print(f"✓ STUDENT LOGIN SUCCESSFUL!")
    print(f"  - Username: {auth_student.username}")
    print(f"  - Groups: {list(auth_student.groups.values_list('name', flat=True))}")
else:
    print(f"✗ STUDENT LOGIN FAILED!")

# Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print(f"""
To login as the tutor you just created in the admin form:
  - Username: {tutor.tutor_id}
  - Password: {admin_entered_passport}

To login as the student you just created:
  - Username: {student.student_id}
  - Password: {admin_entered_student_passport}

FLOW EXPLANATION:
1. Admin creates a tutor/student via the manage form
2. Form saves the tutor/student with hashed passport_data
3. Form automatically creates Django User with username = tutor_id/student_id
4. Form automatically assigns user to Tutors/Students group
5. User can now login using: username (ID) + password (passport_data)

If you are having issues logging in, check:
- The username field should be the Tutor ID or Student ID (e.g., T001, ST001)
- The password field should be the Passport Data you entered when creating the account
- The passport data is case-sensitive!
""")
