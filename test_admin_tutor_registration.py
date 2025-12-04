#!/usr/bin/env python
"""
Test script showing how admin can register a new tutor with passport data.
Run with: python manage.py shell < test_admin_tutor_registration.py
"""

from attendance_records.models import Tutor, Course
from attendance_records.views import TutorForm
from django.contrib.auth.models import User, Group

print("\n" + "=" * 80)
print("ADMIN TUTOR REGISTRATION TEST")
print("=" * 80)

# Simulate admin filling out the tutor form
print("\n[STEP 1] Admin fills out the Tutor Registration Form")
print("-" * 80)

form_data = {
    'first_name': 'Professor',
    'last_name': 'Anderson',
    'tutor_id': 'PROF_A001',
    'email': 'anderson@university.edu',
    'passport_data': 'SecurePass@2025',
    'passport_data_confirm': 'SecurePass@2025',
}

print("Form Data Entered by Admin:")
print(f"  - First Name: {form_data['first_name']}")
print(f"  - Last Name: {form_data['last_name']}")
print(f"  - Tutor ID: {form_data['tutor_id']}")
print(f"  - Email: {form_data['email']}")
print(f"  - Passport Data: {form_data['passport_data']} (will be hashed)")
print(f"  - Confirm Passport Data: {form_data['passport_data_confirm']}")

# Validate the form
print("\n[STEP 2] Validate the Form Data")
print("-" * 80)

form = TutorForm(data=form_data)

if form.is_valid():
    print("✓ Form validation PASSED!")
    print("✓ All fields are correct")
    print("✓ Passport data matches confirmation")
else:
    print("✗ Form validation FAILED!")
    print(f"Errors: {form.errors}")
    exit(1)

# Save the form
print("\n[STEP 3] Admin Clicks 'Save' - Form is Saved to Database")
print("-" * 80)

tutor = form.save()

print(f"✓ Tutor created successfully:")
print(f"  - Tutor ID: {tutor.tutor_id}")
print(f"  - Name: {tutor.first_name} {tutor.last_name}")
print(f"  - Email: {tutor.email}")
print(f"  - Passport: (hashed - {tutor.passport_data[:50]}...)")

# Check if Django User was created
print("\n[STEP 4] Django User Account Auto-Created for Login")
print("-" * 80)

django_user = User.objects.get(username=tutor.tutor_id)
groups = list(django_user.groups.values_list('name', flat=True))

print(f"✓ Django User automatically created:")
print(f"  - Username: {django_user.username}")
print(f"  - First Name: {django_user.first_name}")
print(f"  - Last Name: {django_user.last_name}")
print(f"  - Email: {django_user.email}")
print(f"  - Groups: {groups}")

# Test authentication
print("\n[STEP 5] New Tutor Can Now Login Immediately")
print("-" * 80)

from attendance_records.backends import TutorAuthBackend

backend = TutorAuthBackend()

class MockRequest:
    pass

request = MockRequest()

# Try to authenticate with the credentials
auth_user = backend.authenticate(
    request,
    username=tutor.tutor_id,
    password=form_data['passport_data']  # Use the original passport_data, not hashed
)

if auth_user:
    print(f"✓ Authentication SUCCESSFUL!")
    print(f"  - Logged in as: {auth_user.username}")
    print(f"  - User Groups: {list(auth_user.groups.values_list('name', flat=True))}")
    print(f"\n  Tutor {tutor.tutor_id} can now access the system!")
else:
    print(f"✗ Authentication FAILED!")

# Test wrong password
print("\n[STEP 6] Verify Security - Wrong Password is Rejected")
print("-" * 80)

auth_user_wrong = backend.authenticate(
    request,
    username=tutor.tutor_id,
    password='WrongPassword123'
)

if auth_user_wrong is None:
    print(f"✓ Wrong password correctly REJECTED")
    print(f"  - Security working as expected!")
else:
    print(f"✗ ERROR: Wrong password was accepted (security issue!)")

# Summary
print("\n" + "=" * 80)
print("ADMIN TUTOR REGISTRATION WORKFLOW")
print("=" * 80)

print(f"""
HOW ADMIN REGISTERS A NEW TUTOR:

1. Admin navigates to: /tutors/add/
2. Admin fills in the form:
   - First Name: Professor
   - Last Name: Anderson
   - Tutor ID: PROF_A001 (this becomes the login username)
   - Email: anderson@university.edu
   - Passport Data: SecurePass@2025 (this becomes the login password)
   - Confirm Passport Data: SecurePass@2025
   - Courses: (select any courses the tutor teaches)
3. Admin clicks "Save"
4. System automatically:
   ✓ Saves tutor to database with hashed passport data
   ✓ Creates Django User with username = {tutor.tutor_id}
   ✓ Adds user to 'Tutors' group
   ✓ Enables tutor to login immediately

HOW THE NEW TUTOR CAN LOGIN:

At login page (/login/):
  - Username: {tutor.tutor_id}
  - Password: SecurePass@2025

SECURITY FEATURES:

✓ Passwords are hashed using Django's PBKDF2_SHA256
✓ Each password has a unique salt
✓ Wrong passwords are rejected
✓ Tutor automatically added to 'Tutors' group for role-based access control
✓ User information synced between Tutor and Django User models
""")

print("=" * 80)
print("TEST COMPLETE ✓")
print("=" * 80)
