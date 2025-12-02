# Attendance System - Student & Tutor Dashboard Setup

## New Features Added

### 1. **Student Dashboard** (Student View)
- Route: `/my-attendance/`
- Students can:
  - Select a course from dropdown
  - View their attendance records for that course
  - See attendance status (Present/Absent/Late) with color badges
  - View any notes from the tutor

### 2. **Tutor Mark Attendance** (Tutor & Admin View)
- Route: `/mark-attendance/`
- Tutors/Admins can:
  - Select a course and date
  - See all students in the system
  - Mark attendance for each student (Present/Absent/Late)
  - Add notes for specific students
  - Submit all attendance records at once

### 3. **Enhanced Home Page**
- Role-based dashboards shown on home page
- Students see "My Attendance" card
- Tutors see "Mark Attendance" card
- Admins see all three options: "Manage Students", "View Attendance", "Mark Attendance"

### 4. **Authorization Controls**
- Only students can access their own dashboard (via user.username matching)
- Only tutors and admins can mark attendance
- Only students see student dashboard
- Only tutors/admins see marking page

## File Changes

### New Files Created:
- `templates/attendance_records/student_dashboard.html` - Student view for their attendance
- `templates/attendance_records/tutor_mark_attendance.html` - Tutor interface to mark attendance
- `templatetags/custom_filters.py` - Custom Django template filter
- `management/commands/create_test_users.py` - Command to create test users

### Modified Files:
- `views.py` - Added `StudentDashboardView` and `TutorMarkAttendanceView`
- `urls.py` - Added routes for student_dashboard and tutor_mark
- `templates/index.html` - Updated with role-based navigation cards

## How to Use

### 1. Run Migrations (if not done yet)
```bash
python3 manage.py makemigrations attendance_records
python3 manage.py migrate
```

### 2. Create Test Users
```bash
python3 manage.py create_test_users
```

### 3. Create Sample Courses (via Django admin or code)
You need at least one Course to test. Access Django admin at `/admin/`:
- Username: `admin`
- Password: `password123`
- Add a few courses (e.g., "Python 101", "Web Dev 301")

### 4. Run Server
```bash
python3 manage.py runserver
```

### 5. Test the System

**As Student (username: `student`):**
1. Login with `student` / `password123`
2. Click "My Attendance"
3. Select a course
4. View attendance records (will show empty if tutor hasn't marked yet)

**As Tutor (username: `tutor`):**
1. Login with `tutor` / `password123`
2. Click "Mark Attendance"
3. Select a course and date
4. Mark each student's attendance
5. Submit

**As Admin (username: `admin`):**
1. Login with `admin` / `password123`
2. See all three options on home
3. Can manage students, view all attendance, and mark attendance

## Database Notes

- Students are matched by their `student_id` field, which should match the username (or you can modify the view)
- Course selection is dropdown-based
- Attendance records are stored with date, status, and optional notes
- Only one attendance record per student/course/date (enforced by unique_together constraint)

## Common Issues

**Q: Student dashboard shows no records?**
A: Tutor needs to mark attendance first for that student/course/date combination.

**Q: Students appear as "Anonymous"?**
A: Make sure Groups "Students" and "Tutors" exist (created by create_test_users command).

**Q: Can't create courses?**
A: Use Django admin (`/admin/`) or add a CourseCRUD page if needed.
