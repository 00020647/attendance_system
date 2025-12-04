# Login System Guide

## How the Login System Works

The attendance system has a custom authentication system that uses **Tutor ID / Student ID** and **Passport Data** for login credentials.

### Key Principle
**Username = Tutor ID or Student ID**
**Password = Passport Data**

## For Administrators

### Creating a New Tutor

1. Go to the admin dashboard
2. Click "Manage Tutors"
3. Click "Add Tutor"
4. Fill in the form:
   - **First Name**: The tutor's first name
   - **Last Name**: The tutor's last name
   - **Tutor ID**: Unique identifier (e.g., T001, T002) - **This will be the login username**
   - **Email**: The tutor's email address
   - **Passport Data**: The login password - **This will be the login password**
   - **Confirm Passport Data**: Re-enter the same password
   - **Courses**: Select courses the tutor teaches

5. Click "Save"

**Result**: 
- ✅ Tutor account is created in the system
- ✅ Django User is automatically created with username = Tutor ID
- ✅ User is automatically added to the "Tutors" group
- ✅ Tutor can now login immediately

### Creating a New Student

1. Go to the admin dashboard
2. Click "Manage Students"
3. Click "Add Student"
4. Fill in the form:
   - **First Name**: The student's first name
   - **Last Name**: The student's last name
   - **Student ID**: Unique identifier (e.g., ST001, ST002) - **This will be the login username**
   - **Email**: The student's email address
   - **Passport Data**: The login password - **This will be the login password**
   - **Confirm Passport Data**: Re-enter the same password
   - **Courses**: Select courses the student is enrolled in

5. Click "Save"

**Result**: 
- ✅ Student account is created in the system
- ✅ Django User is automatically created with username = Student ID
- ✅ User is automatically added to the "Students" group
- ✅ Student can now login immediately

## For Users (Tutors and Students)

### How to Login

1. Go to the login page
2. Enter your credentials:
   - **Username**: Your Tutor ID or Student ID (e.g., T001, ST001)
   - **Password**: Your Passport Data (the password you or your admin created)
3. Click the appropriate "Login" button
4. You should be redirected to your dashboard

### Example Login Credentials

**Tutor Account:**
- Username: `T001`
- Password: (the passport data entered by admin)

**Student Account:**
- Username: `ST001`
- Password: (the passport data entered by admin)

### What to Do if You Can't Login

1. **Check the username**: Make sure you're using your Tutor ID or Student ID, not your name
   - For tutors: Should start with "T" (e.g., T001, T002)
   - For students: Should start with "ST" (e.g., ST001, ST002)

2. **Check the password**: Make sure you're using the correct passport data
   - Passwords are case-sensitive
   - Make sure there are no extra spaces
   - If you forgot the password, contact your administrator

3. **Account not created yet?**: Ask your administrator to create your account in the "Manage Tutors" or "Manage Students" section

## Technical Details

### How It Works

1. **Account Creation**:
   - When an admin creates a tutor/student via the manage form, a tutor/student record is saved to the database
   - The passport data is securely hashed using Django's PBKDF2_SHA256 algorithm
   - A Django User account is automatically created with username = tutor_id/student_id
   - The user is automatically added to the appropriate group (Tutors or Students)

2. **Login Process**:
   - User enters their Tutor/Student ID and Passport Data
   - The system looks up the tutor/student record by ID
   - The entered password is verified against the hashed password
   - If correct, the corresponding Django User is retrieved and authenticated
   - If incorrect, login fails

3. **Security**:
   - Passwords are never stored in plain text
   - Password verification uses constant-time comparison to prevent timing attacks
   - Each password has a unique salt
   - Django's built-in password hashing is used

### Database Structure

**Tutor Table** (attendance_records_tutor):
- tutor_id: VARCHAR(30) - Unique identifier, used as login username
- first_name: VARCHAR(100)
- last_name: VARCHAR(100)
- email: VARCHAR(254)
- passport_data: VARCHAR(128) - Hashed password
- created_at: DATETIME

**Student Table** (attendance_records_student):
- student_id: VARCHAR(30) - Unique identifier, used as login username
- first_name: VARCHAR(100)
- last_name: VARCHAR(100)
- email: VARCHAR(254)
- passport_data: VARCHAR(128) - Hashed password
- created_at: DATETIME

**Django User Table** (auto-created):
- username: VARCHAR(150) - Same as tutor_id or student_id
- first_name: VARCHAR(150)
- last_name: VARCHAR(150)
- email: VARCHAR(254)
- groups: Many-to-Many relationship (Tutors or Students group)

### Authentication Backends

The system uses two custom authentication backends:

1. **TutorAuthBackend** (`attendance_records/auth_backends.py`):
   - Authenticates tutors using tutor_id + passport_data
   - Creates/updates Django User with username = tutor_id
   - Adds user to "Tutors" group

2. **StudentAuthBackend** (`attendance_records/auth_backends.py`):
   - Authenticates students using student_id + passport_data
   - Creates/updates Django User with username = student_id
   - Adds user to "Students" group

### Automatic User Creation

When a tutor or student is created/updated, a Django signal automatically:
1. Creates a Django User if it doesn't exist
2. Updates the user's info (first name, last name, email) if changed
3. Adds the user to the appropriate group (Tutors or Students)
4. Ensures the user is not removed from their group

## Troubleshooting

### Problem: "Invalid credentials" when trying to login

**Solution**: 
- Double-check the username - it should be the Tutor ID or Student ID
- Double-check the password - it should be the Passport Data you entered
- Remember that passwords are case-sensitive

### Problem: Login button doesn't work

**Solution**:
- Make sure you're using the correct login form
- Check that your browser's cookies are enabled
- Try clearing your browser cache

### Problem: Account doesn't exist

**Solution**:
- Ask your administrator to create your account in the "Manage Tutors" or "Manage Students" section
- Make sure you're using the correct institution/database

### Problem: Forgot your password

**Solution**:
- Contact your administrator to reset your password
- The administrator can update your passport data in the "Manage Tutors" or "Manage Students" section

## Best Practices

1. **Use Strong Passport Data**: Create complex passwords with letters, numbers, and symbols
2. **Keep Credentials Secure**: Don't share your password with anyone
3. **Report Issues**: If you suspect unauthorized access, inform your administrator immediately
4. **Update Email**: Keep your email address up to date for account recovery

## Admin Responsibilities

1. **Create Accounts Securely**: Use strong passwords when creating accounts
2. **Distribute Credentials Safely**: Don't email passwords - communicate them securely
3. **Monitor Access**: Regularly check who's logging in and when
4. **Reset Forgotten Passwords**: Update the passport data if a user forgets their password
5. **Remove Access**: Delete accounts when users leave the institution

---

**Last Updated**: December 4, 2025
**System Version**: Django 5.2.9
**Security Level**: Medium (uses PBKDF2_SHA256 hashing)
