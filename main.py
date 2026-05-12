import json
students_db = {}
filename = "students_data.json"

def load_data():
    global students_db
    try:
        with open(filename, 'r') as f:
            students_db = json.load(f)
    except FileNotFoundError:
        students_db = {}

def save_data():
    with open(filename, 'w') as f:
        json.dump(students_db, f, indent=4,)

def get_grade(average):
    """Assigns grade based on the provided average marks scale."""
    if average >= 90: return "A+"
    elif average >= 80: return "A"
    elif average >= 70: return "B+"
    elif average >= 60: return "B"
    elif average >= 50: return "C"
    elif average >= 40: return "D"
    else: return "F"

def add_student():
    print("\n--- Add New Student ---")
    roll = input("Enter Roll Number: ")
    if roll in students_db:
        print("Error: Roll Number must be unique!")
        return
    
    name = input("Enter Name: ")
    branch = input("Enter Branch: ")
    while True:
       try:
           semester = int(input("Enter Semester: "))
           break
       except ValueError:
           print("Invalid input! Semester must be a number.")
        
    
    courses_input = input("Enter courses (comma-separated): ")
    # Convert comma-separated string to a list of stripped course names
    courses = [c.strip() for c in courses_input.split(",") if c.strip()]
    
    students_db[roll] = {
        "name": name,
        "branch": branch,
        "semester": semester,
        "courses": courses,
        "marks": {},  # Dictionary for course: marks
        "average": 0.0,
        "grade": "N/A"
    }
    save_data()
    print("Student added successfully!")

def record_marks():
    print("\n--- Record Marks ---")
    roll = input("Enter Roll Number: ")
    if roll not in students_db:
        print("Error: Student not found!")
        return
    
    student = students_db[roll]
    print(f"Student: {student['name']}")
    
    total_marks = 0
    for course in student['courses']:
        while True:
            try:
                m = float(input(f"Enter marks for {course}: "))
                if 0 <= m <= 100:
                    student['marks'][course] = m
                    total_marks += m
                    break
                else:
                    print("Marks must be between 0 and 100.")
            except ValueError:
                print("Invalid input! Please enter a numeric value.")
    
    if student['courses']:
        student['average'] = total_marks / len(student['courses'])
        student['grade'] = get_grade(student['average'])
    
    save_data()
    print("Marks recorded successfully!")
    print(f"Average: {student['average']:.2f}% | Grade: {student['grade']}")

def display_all():
    print("\n" + "="*75)
    print(f"{'Roll No.':<12} {'Name':<20} {'Branch':<20} {'Average':<10} {'Grade':<5}")
    print("-" * 75)
    for roll, info in students_db.items():
        print(f"{roll:<12} {info['name']:<20} {info['branch']:<20} {info['average']:<10.2f} {info['grade']:<5}")
    print("="*75)

def display_individual():
    roll = input("\nEnter Roll Number: ")
    if roll not in students_db:
        print("Error: Student not found!")
        return
    
    s = students_db[roll]
    print("\n===== Student Details =====")
    print(f"Roll Number: {roll}")
    print(f"Name: {s['name']}")
    print(f"Branch: {s['branch']}")
    print(f"Semester: {s['semester']}")
    print("Enrolled Courses and Marks:")
    for course in s['courses']:
        mark = s['marks'].get(course, "N/A")
        print(f"  - {course}: {mark}")
    print(f"Average: {s['average']:.2f}%")
    print(f"Grade: {s['grade']}")

def update_student():
    roll = input("\nEnter Roll Number: ")
    if roll not in students_db:
        print("Error: Student not found!")
        return
    
    print("To Update Student Information - Select One Of The Following:")
    print("1. Name\n2. Branch\n3. Semester\n4. Add Course\n5. Remove Course\n6. Update Marks")
    choice = input("Enter choice: ")
    
    s = students_db[roll]
    if choice == '1':
        s['name'] = input("Enter new name: ")
    elif choice == '2':
        s['branch'] = input("Enter new branch: ")
    elif choice == '3':
        try:
            s['semester'] = int(input("Enter new semester: "))
        except ValueError: print("Invalid semester.")
    elif choice == '4':
        new_course = input("Enter new course name: ")
        if new_course not in s['courses']:
            s['courses'].append(new_course)
    elif choice == '5':
        course_rem = input("Enter course to remove: ")
        if course_rem in s['courses']:
            s['courses'].remove(course_rem)
            s['marks'].pop(course_rem, None)
    elif choice == '6':
        course_upd = input("Enter course name to update marks: ")
        if course_upd in s['courses']:
            try:
                m = float(input(f"Enter new marks for {course_upd}: "))
                if 0 <= m <= 100: s['marks'][course_upd] = m
                else: print("Invalid marks.")
            except ValueError: print("Invalid input.")
    
    # Recalculate average/grade after updates
    if s['marks']:
        s['average'] = sum(s['marks'].values()) / len(s['marks'])
        s['grade'] = get_grade(s['average'])
    
    save_data()
    print("Updated successfully!")

def delete_student():
    roll = input("\nEnter Roll Number: ")
    if roll in students_db:
        confirm = input(f"Are you sure you want to delete {students_db[roll]['name']}? (yes/no): ").lower()
        if confirm == 'yes':
            del students_db[roll]
            save_data()
            print("Student deleted successfully!")
    else:
        print("Error: Student not found!")

def search_by_branch():
    branch = input("\nEnter Branch: ")
    count = 0
    print("\n" + "="*60)
    print(f"{'Roll No.':<12} {'Name':<20} {'Average':<10} {'Grade':<5}")
    print("-" * 60)
    for roll, info in students_db.items():
        if info['branch'].lower() == branch.lower():
            print(f"{roll:<12} {info['name']:<20} {info['average']:<10.2f} {info['grade']:<5}")
            count += 1
    print("="*60)
    print(f"Total students in {branch}: {count}")

def main_menu():
    load_data()
    while True:
        print("\n===== Student Management System =====")
        print("1. Add New Student")
        print("2. Record Marks")
        print("3. Display All Students")
        print("4. Display Individual Student")
        print("5. Update Student Information")
        print("6. Delete Student Record")
        print("7. Search by Branch")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1': add_student()
        elif choice == '2': record_marks()
        elif choice == '3': display_all()
        elif choice == '4': display_individual()
        elif choice == '5': update_student()
        elif choice == '6': delete_student()
        elif choice == '7': search_by_branch()
        elif choice == '8': 
            save_data()
            print("Exiting program...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()
