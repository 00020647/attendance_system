# Attendance System - REST API Documentation

## Overview

The Attendance System includes a simple REST API for programmatic access to student, course, and attendance data. All API endpoints require authentication using session or token-based authentication.

## Base URL
```
http://localhost:8000/api/
```

## Authentication

All API endpoints require authentication. You can authenticate in two ways:

### 1. Session Authentication (Browser)
Login via the web interface at `/login/` and use the same session for API calls.

### 2. API Endpoints with Authentication

```bash
# Example with session cookie
curl -b "sessionid=your_session_id" http://localhost:8000/api/students/
```

---

## API Endpoints

### 1. Students API

#### List all students
```
GET /api/students/
```

**Query Parameters:**
- `search` - Search by student_id, first_name, last_name, or email

**Example:**
```bash
curl -H "Authorization: Session" http://localhost:8000/api/students/?search=john
```

**Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "student_id": "0001",
      "full_name": "John Doe",
      "email": "john@example.com",
      "course_count": 3,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Get specific student
```
GET /api/students/{id}/
```

**Response:**
```json
{
  "id": 1,
  "student_id": "0001",
  "full_name": "John Doe",
  "email": "john@example.com",
  "course_count": 3,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get student's attendance records
```
GET /api/students/{id}/attendance/
```

**Query Parameters:**
- `course` - Filter by course_id

**Example:**
```bash
curl http://localhost:8000/api/students/1/attendance/?course=2
```

**Response:**
```json
[
  {
    "id": 5,
    "student_id": "0001",
    "student_name": "John Doe",
    "course_code": "CS101",
    "semester": 1,
    "week": 1,
    "status": "P",
    "status_display": "Present",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 2. Courses API

#### List all courses
```
GET /api/courses/
```

**Query Parameters:**
- `search` - Search by code or name

**Example:**
```bash
curl http://localhost:8000/api/courses/?search=CS
```

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "code": "CS101",
      "name": "Introduction to Computer Science",
      "student_count": 15,
      "tutor_count": 2
    }
  ]
}
```

#### Get specific course
```
GET /api/courses/{id}/
```

#### Get course's attendance records
```
GET /api/courses/{id}/attendance/
```

**Query Parameters:**
- `date` - Filter by specific date (YYYY-MM-DD)

**Example:**
```bash
curl http://localhost:8000/api/courses/1/attendance/?date=2024-01-15
```

#### Get students in a course
```
GET /api/courses/{id}/students/
```

#### Get tutors teaching a course
```
GET /api/courses/{id}/tutors/
```

---

### 3. Attendance Records API

#### List attendance records
```
GET /api/attendance/
```

**Query Parameters:**
- `student` - Filter by student_id
- `course` - Filter by course_id
- `date` - Filter by date (YYYY-MM-DD)
- `status` - Filter by status (P=Present, A=Absent, E=Excused)

**Example:**
```bash
curl http://localhost:8000/api/attendance/?student=1&status=P
```

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 5,
      "student_id": "0001",
      "student_name": "John Doe",
      "course_code": "CS101",
      "semester": 1,
      "week": 1,
      "status": "P",
      "status_display": "Present",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Get specific attendance record
```
GET /api/attendance/{id}/
```

#### Create attendance record (Tutor/Admin only)
```
POST /api/attendance/
```

**Request Body:**
```json
{
  "student": 1,
  "course": 1,
  "semester": 1,
  "week": 1,
  "status": "P"
}
```

#### Update attendance record (Tutor/Admin only)
```
PUT /api/attendance/{id}/
```

**Request Body:**
```json
{
  "status": "A"
}
```

#### Delete attendance record (Tutor/Admin only)
```
DELETE /api/attendance/{id}/
```

---

### 4. Student's Own Attendance

#### Get current student's attendance records
```
GET /api/my-attendance/
```

**Query Parameters:**
- `course` - Filter by course_id

**Response:**
```json
{
  "student": {
    "id": 1,
    "student_id": "0001",
    "full_name": "John Doe",
    "email": "john@example.com",
    "course_count": 3,
    "created_at": "2024-01-15T10:30:00Z"
  },
  "attendance_records": [
    {
      "id": 5,
      "student_id": "0001",
      "student_name": "John Doe",
      "course_code": "CS101",
      "semester": 1,
      "week": 1,
      "status": "P",
      "status_display": "Present",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

### 5. Statistics API

#### Get overall attendance statistics
```
GET /api/stats/
```

**Response:**
```json
{
  "total_students": 25,
  "total_courses": 5,
  "total_attendance_records": 450,
  "overall_attendance_rate": "87.5%",
  "status_breakdown": {
    "present": 394,
    "absent": 56,
    "late": 0
  }
}
```

---

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Resource deleted successfully
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Pagination

List endpoints support pagination with a default page size of 20 items.

**Query Parameters:**
- `page` - Page number (default: 1)

**Example:**
```bash
curl http://localhost:8000/api/students/?page=2
```

**Response includes:**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/students/?page=3",
  "previous": "http://localhost:8000/api/students/?page=1",
  "results": [...]
}
```

---

## Access Control

### Read Permissions
- **Students**: Can view all students, courses, and their own attendance
- **Tutors**: Can view all students, courses, and attendance records
- **Admins**: Can view all data

### Write Permissions
- **Students**: No write access
- **Tutors**: Can create, update, and delete attendance records
- **Admins**: Can perform all operations

---

## Example Usage

### Python with requests
```python
import requests
from requests.auth import HTTPBasicAuth

# Login and get session
session = requests.Session()
response = session.post(
    'http://localhost:8000/login/',
    data={'username': '0001', 'password': 'password123'}
)

# Get students
response = session.get('http://localhost:8000/api/students/')
print(response.json())

# Create attendance record
data = {
    'student': 1,
    'course': 1,
    'semester': 1,
    'week': 1,
    'status': 'P'
}
response = session.post('http://localhost:8000/api/attendance/', json=data)
print(response.json())
```

### JavaScript/Fetch
```javascript
// Fetch students
fetch('http://localhost:8000/api/students/')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

// Create attendance record
fetch('http://localhost:8000/api/attendance/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    student: 1,
    course: 1,
    semester: 1,
    week: 1,
    status: 'P'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Notes

- All timestamps are in ISO 8601 format (UTC)
- Status codes: `P` = Present, `A` = Absent, `E` = Excused
- Semester values: `1` or `2`
- Week values: `1` to `18`
- The API uses pagination by default (20 items per page)
- Use `?format=json` to force JSON response in browser
