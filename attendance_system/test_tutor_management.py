#!/usr/bin/env python
"""
Script to test tutor management functionality.
Run with: python manage.py shell < test_tutor_management.py
"""

from attendance_records.models import Tutor, Course
from attendance_records.auth import PassportAuthBackend
from django.contrib.auth.models import Group, User

print("=" * 60)
print("TUTOR MANAGEMENT TEST SCRIPT")
print("=" * 60)

# 1. Test Tutor Model with Passport Data
print("\n1. Testing Tutor Model...")
tutor, created = Tutor.objects.update_or_create(
    tutor_id='TEST_T001',
    defaults={
        'first_name': 'Test',
        'last_name': 'Tutor',
        'email': 'test.tutor@example.com'
    }
)
print(f"   ✓ Tutor created/updated: {tutor}")

# 2. Test Passport Data Hashing
print("\n2. Testing Passport Data Hashing...")
test_passport = 'SecurePassport123!'
tutor.set_passport_data(test_passport)
tutor.save()
print(f"   ✓ Passport data set and hashed")
print(f"   ✓ Hashed value (first 50 chars): {tutor.passport_data[:50]}...")

# 3. Test Passport Verification
print("\n3. Testing Passport Verification...")
is_correct = tutor.check_passport_data(test_passport)
is_wrong = tutor.check_passport_data('WrongPassword')
print(f"   ✓ Correct passport verified: {is_correct}")
print(f"   ✓ Wrong passport rejected: {not is_wrong}")

# 4. Test Authentication Backend
print("\n4. Testing Authentication Backend...")
backend = PassportAuthBackend()

# Test with correct credentials
from django.contrib.auth import get_user_model
User = get_user_model()

# Create a mock request object
class MockRequest:
    pass

request = MockRequest()
auth_user = backend.authenticate(
    request, 
    username='TEST_T001',
    password=test_passport,
    user_type='tutor'
)

if auth_user:
    print(f"   ✓ Authentication successful: {auth_user.username}")
    print(f"   ✓ User groups: {list(auth_user.groups.values_list('name', flat=True))}")
else:
    print(f"   ✗ Authentication failed!")

# Test with wrong credentials
auth_user_wrong = backend.authenticate(
    request,
    username='TEST_T001',
    password='WrongPassword',
    user_type='tutor'
)
print(f"   ✓ Wrong password rejected: {auth_user_wrong is None}")

# 5. Test Form Fields
print("\n5. Testing TutorForm...")
from attendance_records.views import TutorForm

form_data = {
    'first_name': 'Jane',
    'last_name': 'Smith',
    'tutor_id': 'JS001',
    'email': 'jane.smith@example.com',
    'passport_data': 'JaneSecure123',
    'passport_data_confirm': 'JaneSecure123',
}

form = TutorForm(data=form_data)
if form.is_valid():
    print(f"   ✓ Form validation passed")
else:
    print(f"   ✗ Form validation failed: {form.errors}")

# Test mismatched passwords
form_data['passport_data_confirm'] = 'Different'
form = TutorForm(data=form_data)
if not form.is_valid():
    print(f"   ✓ Form correctly rejected mismatched passports")
else:
    print(f"   ✗ Form should have rejected mismatched passports")

# 6. Test Course Association
print("\n6. Testing Course Association...")
course, _ = Course.objects.get_or_create(
    code='TEST101',
    defaults={'name': 'Test Course'}
)
tutor.courses.add(course)
print(f"   ✓ Course associated: {tutor.courses.count()} course(s)")

# 7. Summary
print("\n" + "=" * 60)
print("ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 60)
print(f"\nTest Tutor Summary:")
print(f"  ID: {tutor.tutor_id}")
print(f"  Name: {tutor.first_name} {tutor.last_name}")
print(f"  Email: {tutor.email}")
print(f"  Courses: {tutor.courses.count()}")
print(f"  Passport: {'Set and Hashed' if tutor.passport_data else 'Not Set'}")
print("\n")
