# Admin Tutor Registration Guide

## Quick Summary

The TutorForm now includes **Passport Data** fields so admins can register new tutors directly with login credentials.

## How Admin Registers a New Tutor

### Step 1: Navigate to Add Tutor Form
Go to: `/tutors/add/`

Or click on:
- Admin Dashboard → "Manage Tutors" → "Add New Tutor" button

### Step 2: Fill Out the Form

The form has the following fields:

| Field | Description | Example |
|-------|-------------|---------|
| **First Name** | Tutor's first name | John |
| **Last Name** | Tutor's last name | Smith |
| **Tutor ID** | Unique identifier (becomes login username) | T001, PROF_J001 |
| **Email** | Tutor's email address | john.smith@university.edu |
| **Passport Data** | Login password (will be hashed/encrypted) | MySecurePass123! |
| **Confirm Passport Data** | Must match Passport Data field | MySecurePass123! |
| **Courses** | Check boxes for courses tutor teaches | Physics, Chemistry |

### Step 3: Validation

The form automatically validates:
- ✓ All required fields are filled
- ✓ Passport Data and Confirm Passport Data match
- ✓ Tutor ID is unique
- ✓ Email format is valid (if provided)

### Step 4: Save

Click **"Save"** button

### Step 5: Automatic Account Creation

When saved, the system automatically:
1. ✓ Saves tutor record with **hashed** passport data (never stored as plain text)
2. ✓ Creates Django User account with username = Tutor ID
3. ✓ Adds user to **'Tutors'** group for role-based access
4. ✓ Enables tutor to login immediately

## How the New Tutor Logs In

The newly registered tutor can now login at `/login/` using:

**Username**: The Tutor ID entered in the form (e.g., T001, PROF_J001)
**Password**: The Passport Data entered in the form

Example:
```
Username: PROF_J001
Password: MySecurePass123!
```

## What Happens After Login?

Once logged in, the tutor can:
- ✓ View their profile and courses
- ✓ Mark attendance for their courses
- ✓ Access tutor-specific dashboards

## Editing an Existing Tutor

If you need to edit a tutor's information:

1. Go to `/tutors/` → Find the tutor → Click **"Edit"**
2. Update the fields you want to change
3. **To change the password**: Fill in **Passport Data** and **Confirm Passport Data**
4. **To keep the same password**: Leave **Passport Data** blank
5. Click **"Save"**

## Deleting a Tutor

To remove a tutor:

1. Go to `/tutors/` → Find the tutor → Click **"Delete"**
2. Confirm the deletion on the confirmation page
3. The tutor record and Django User account are removed

## Security Information

### Password Hashing
- Passwords are **never stored in plain text**
- Uses Django's **PBKDF2_SHA256** hashing algorithm
- Each password gets a unique **salt**
- Verification uses constant-time comparison (prevents timing attacks)

### User Accounts
- Each tutor gets an automatic **Django User** account
- Username = Tutor ID
- User is in the **'Tutors'** group (enables role-based access control)
- User information is synced with tutor record

### Best Practices for Admins

1. **Use Strong Passwords**: 
   - Mix uppercase, lowercase, numbers, and symbols
   - Example: `MyPass@2025!Strong`

2. **Communicate Securely**:
   - Don't email passwords to tutors
   - Share credentials in person or via secure channels

3. **Unique IDs**:
   - Use consistent naming convention (e.g., T001, T002 or PROF_SMITH)
   - Make IDs easy to remember

4. **Update Email**:
   - Keep tutor email addresses current
   - Used for communication and account recovery

## Troubleshooting

### "Tutor ID must be unique" Error
- The Tutor ID you entered already exists
- Choose a different ID

### "Passport data fields must match" Error
- The Passport Data and Confirm fields don't match
- Make sure they're exactly the same (case-sensitive)

### "Passport data is required for new tutors" Error
- You didn't fill in the Passport Data field
- New tutors need a password to login

### Tutor Can't Login
- Check that username = Tutor ID (not the tutor's name)
- Check that password = Passport Data (case-sensitive)
- Verify the account was saved successfully

## Example Workflow

```
ADMIN CREATES NEW TUTOR:
├─ Admin navigates to /tutors/add/
├─ Fills form:
│  ├─ First Name: Dr.
│  ├─ Last Name: Johnson
│  ├─ Tutor ID: DR_JOHNSON
│  ├─ Email: johnson@university.edu
│  ├─ Passport Data: DrJ@2025!Secure
│  ├─ Confirm: DrJ@2025!Secure
│  └─ Courses: Physics 101, Advanced Physics
├─ Clicks Save
└─ System automatically creates Django User

TUTOR LOGS IN:
├─ Navigates to /login/
├─ Enters:
│  ├─ Username: DR_JOHNSON
│  └─ Password: DrJ@2025!Secure
├─ Clicks Login
└─ Tutor Dashboard loads successfully
```

---

**Last Updated**: December 4, 2025
**System**: Django Attendance System
**Database**: MySQL
**Authentication**: Passport Data (Hashed with PBKDF2_SHA256)
