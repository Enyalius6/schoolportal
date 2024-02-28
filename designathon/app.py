from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)


def write_students(filename, students):
    fieldnames = ['name', 'address', 'age', 'roll_number', 'username', 'password', 'class', 'section', 
                  'timetable_id', 'attendance', 'pending_fee', 'subject_Math_grade', 
                  'subject_English_grade', 'subject_Science_Grade']
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)
# Function to check if username and password match in a CSV file
def check_credentials(filename, username, password):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False
def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data
# Route for login page
@app.route('/')
def index():
    return render_template('login.html')

# Login logic
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if username and password match in admins.csv
    if check_credentials('admins.csv', username, password):
        return redirect(url_for('admin_dashboard'))

    # Check if username and password match in teachers.csv
    elif check_credentials('teachers.csv', username, password):
        return redirect(url_for('teacher_dashboard'))

    # Check if username and password match in students.csv
    elif check_credentials('students.csv', username, password):
        return redirect(url_for('student_dashboard'))

    else:
        return 'Login failed. Invalid username or password.'

# Admin dashboard route
@app.route('/admin')
def admin_dashboard():
    teachers_data = read_csv('teachers.csv')
    students_data = read_csv('students.csv')
    return render_template('admin.html', teachers=teachers_data, students=students_data)
    

# Route for adding a new teacher
@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    username = request.form['teacher_username']
    password = request.form['teacher_password']
    with open('teachers.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
    return redirect(url_for('admin_dashboard'))

# Route for adding a new student
@app.route('/add_student', methods=['POST'])
def add_student():
    # Retrieve all form fields from the request
    name = request.form['name']
    address = request.form['address']
    age = request.form['age']
    roll_number = request.form['roll_number']
    username = request.form['username']
    password = request.form['password']
    class_ = request.form['class']  # Using class_ instead of class to avoid conflict with Python keyword
    section = request.form['section']
    timetable_id = request.form['timetable_id']
    attendance = request.form['attendance']
    pending_fee = request.form['pending_fee']
    math_grade = request.form['subject_Math_grade']
    english_grade = request.form['subject_English_grade']
    science_grade = request.form['subject_Science_Grade']
    parent_key = request.form['parent_key']


    # Write the student data to the CSV file
    with open('students.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, address, age, roll_number, username, password, class_, section, timetable_id,
                         attendance, pending_fee, math_grade, english_grade, science_grade,0,parent_key])

    return redirect(url_for('admin_dashboard'))

@app.route('/remove_teacher', methods=['POST'])
def remove_teacher():
    teacher_username = request.form['teacher_username_remove']
    teachers = []

    # Read existing teachers from the CSV file
    with open('teachers.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != teacher_username:  # Skip the teacher to be removed
                teachers.append(row)

    # Write updated teachers to the CSV file
    with open('teachers.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(teachers)

    return redirect(url_for('admin_dashboard'))

@app.route('/remove_student', methods=['POST'])
def remove_student():
    student_username = request.form['student_username_remove']
    students = []

    # Read existing students from the CSV file
    with open('students.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] != student_username:  # Skip the student to be removed
                students.append(row)

    # Write updated students to the CSV file
    write_students('students.csv', students)

    return redirect(url_for('admin_dashboard'))
# Teacher dashboard route
@app.route('/teacher')
def teacher_dashboard():
    return 'Welcome Teacher!'

# Student dashboard route
@app.route('/student')
def student_dashboard():
    return 'Welcome Student!'

if __name__ == '__main__':
    app.run(debug=True)
