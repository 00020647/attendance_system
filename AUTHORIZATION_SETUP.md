# Attendance System - Authorization & Test Accounts Setup

## What Was Added

### 1. Authorization (Role-Based Access Control)
- **TutorAdminRequiredMixin**: Restricts create/update views to tutors and admins only
- **AdminRequiredMixin**: Restricts delete views to admins only
- All views now require login

### 2. URL Changes
- Added `login/` route → Django's LoginView with custom template
- Added `logout/` route → Django's LogoutView that redirects to home

### 3. Test User Creation Command
Created management command: `python manage.py create_test_users`

**Test Accounts Created:**
- **Student**: username: `student`, password: `password123` (blue box)
- **Tutor**: username: `tutor`, password: `password123` (red box)
- **Admin**: username: `admin`, password: `password123` (purple box)

### 4. Login Template
- Created login.html with Bootstrap styling
- Shows test account credentials on login page
- Form styling with error handling

### 5. Updated Views & Templates
- All views now enforce login + role-based authorization
- Index page shows login button for unauthenticated users
- Shows user role and colored box when authenticated

## Setup Instructions

Run these commands from `/Users/sukhrob_1/Downloads/attendance_system/attendance_system/`:

### 1. Create/Apply Migrations
```bash
python3 manage.py makemigrations attendance_records
python3 manage.py migrate
```

### 2. Create Test Users & Groups
```bash
python3 manage.py create_test_users
```

### 3. Create Superuser (Optional - for Django admin)
```bash
python3 manage.py createsuperuser
```

### 4. Run Dev Server
```bash
python3 manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Access Control Summary

| Action | Student | Tutor | Admin | Anonymous |
|--------|---------|-------|-------|-----------|
| View Students List | ✓ | ✓ | ✓ | ✗ Login Required |
| Add Student | ✗ | ✓ | ✓ | ✗ Login Required |
| Edit Student | ✗ | ✓ | ✓ | ✗ Login Required |
| Delete Student | ✗ | ✗ | ✓ | ✗ Login Required |
| View Attendance | ✓ | ✓ | ✓ | ✗ Login Required |
| Add Attendance | ✗ | ✓ | ✓ | ✗ Login Required |
| Edit Attendance | ✗ | ✓ | ✓ | ✗ Login Required |
| Delete Attendance | ✗ | ✗ | ✓ | ✗ Login Required |

## File Structure

```
attendance_records/
  management/
    commands/
      create_test_users.py
  templates/
    login.html (NEW)
    index.html (UPDATED)
    ...
  middleware.py (EXISTING)
  urls.py (UPDATED - added login/logout)
  views.py (UPDATED - added mixins & decorators)
```

## URL Patterns
- `/ ` → Home (index)
- `/login/` → Login page
- `/logout/` → Logout
- `/students/` → Student list
- `/students/add/` → Add student
- `/students/<id>/edit/` → Edit student
- `/students/<id>/delete/` → Delete student
- `/attendance/` → Attendance list
- `/attendance/add/` → Add attendance
- `/attendance/<id>/edit/` → Edit attendance
- `/attendance/<id>/delete/` → Delete attendance
