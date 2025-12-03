ALTER TABLE attendance_records_student 
ADD COLUMN passport_data VARCHAR(128) NOT NULL DEFAULT '';

-- Or if creating from scratch:
DROP TABLE IF EXISTS attendance_records_attendancerecord;
DROP TABLE IF EXISTS attendance_records_student_courses;
DROP TABLE IF EXISTS attendance_records_student;
DROP TABLE IF EXISTS attendance_records_course;

CREATE TABLE attendance_records_course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE attendance_records_student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    student_id VARCHAR(30) UNIQUE NOT NULL,
    passport_data VARCHAR(128) NOT NULL,
    email VARCHAR(254),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE attendance_records_student_courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES attendance_records_student(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES attendance_records_course(id) ON DELETE CASCADE,
    UNIQUE (student_id, course_id)
);

CREATE TABLE attendance_records_attendancerecord (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    semester INT NOT NULL,
    week INT NOT NULL,
    date DATE,
    status VARCHAR(1) NOT NULL,
    notes LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES attendance_records_student(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES attendance_records_course(id) ON DELETE CASCADE,
    UNIQUE (student_id, course_id, semester, week)
);

CREATE TABLE attendance_records_tutor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    tutor_id VARCHAR(30) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    email VARCHAR(254),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE attendance_records_tutor_courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tutor_id INT NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY (tutor_id) REFERENCES attendance_records_tutor(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES attendance_records_course(id) ON DELETE CASCADE,
    UNIQUE (tutor_id, course_id)
);