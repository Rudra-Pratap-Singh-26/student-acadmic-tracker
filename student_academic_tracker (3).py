import json
import csv
import os
import sys

# File paths for local persistence and reporting
DB_FILE = 'students_data.json'
EXPORT_FILE = 'academic_report.csv'

def load_database():
    """Reads saved student records from JSON. Returns empty dict if file is missing or corrupted."""
    if not os.path.exists(DB_FILE):
        return {}
    
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as err:
        print(f"[!] Note: Could not parse '{DB_FILE}' ({err}). Starting with empty record set.")
        return {}

def save_database(data):
    """Saves the main student dictionary to disk in JSON format."""
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except OSError as err:
        print(f"[!] Error writing data to disk: {err}")

def prompt_str(msg, allow_blank=False):
    """Prompts for text input and strips whitespace. Re-prompts if blank unless allowed."""
    while True:
        val = input(msg).strip()
        if val or allow_blank:
            return val
        print("    -> Value cannot be empty. Give it another try.")

def prompt_int(msg, min_v=None, max_v=None):
    """Gets an integer from the user within an optional min/max range."""
    while True:
        raw = input(msg).strip()
        try:
            val = int(raw)
            if min_v is not None and val < min_v:
                print(f"    -> Please enter a number >= {min_v}.")
                continue
            if max_v is not None and val > max_v:
                print(f"    -> Please enter a number <= {max_v}.")
                continue
            return val
        except ValueError:
            print("    -> That's not a valid integer. Try again.")

def prompt_float(msg, min_v=None, max_v=None):
    """Gets a float value with boundary checks."""
    while True:
        raw = input(msg).strip()
        try:
            val = float(raw)
            if min_v is not None and val < min_v:
                print(f"    -> Value must be at least {min_v}.")
                continue
            if max_v is not None and val > max_v:
                print(f"    -> Value cannot exceed {max_v}.")
                continue
            return val
        except ValueError:
            print("    -> Invalid decimal number. Please re-enter.")

def convert_marks_to_grade(marks):
    """
    Standard grading conversion mapping:
    90-100: S (10), 80-89: A (9), 70-79: B (8), 60-69: C (7),
    50-59: D (6), 40-49: E (5), <40: F (0)
    """
    if marks >= 90:
        return 'S', 10.0
    elif marks >= 80:
        return 'A', 9.0
    elif marks >= 70:
        return 'B', 8.0
    elif marks >= 60:
        return 'C', 7.0
    elif marks >= 50:
        return 'D', 6.0
    elif marks >= 40:
        return 'E', 5.0
    return 'F', 0.0

def compute_student_gpa(courses):
    """Computes weighted GPA = Sum(credits * grade_points) / Sum(credits)"""
    if not courses:
        return 0.0, 0
    
    tot_pts = 0.0
    tot_credits = 0
    
    for c_info in courses.values():
        cr = c_info.get('credits', 0)
        pts = c_info.get('points', 0.0)
        tot_pts += (cr * pts)
        tot_credits += cr
        
    if tot_credits == 0:
        return 0.0, 0
        
    gpa = tot_pts / tot_credits
    return round(gpa, 2), tot_credits

def register_new_student(db):
    """Adds a new student profile to the database."""
    print("\n" + "="*40)
    print("      REGISTER NEW STUDENT")
    print("="*40)
    
    reg_no = prompt_str("Enter Registration No (e.g. REG101): ").upper()
    if reg_no in db:
        print(f"[!] Registration number '{reg_no}' already exists in the system.")
        return
        
    name = prompt_str("Enter Full Name: ")
    branch = prompt_str("Enter Department / Branch: ")
    
    db[reg_no] = {
        'name': name,
        'branch': branch,
        'courses': {}
    }
    
    save_database(db)
    print(f"\n[+] Successfully registered '{name}' ({reg_no}).")

def list_all_students(db):
    """Displays all students in a neatly formatted table."""
    print("\n" + "="*68)
    print(f"| {'Reg Number':<14} | {'Student Name':<26} | {'Department':<18} |")
    print("="*68)
    
    if not db:
        print(f"| {'No student records found in database.':<64} |")
        print("="*68)
        return
        
    for reg_no, info in db.items():
        st_name = info.get('name', 'N/A')
        if len(st_name) > 26:
            st_name = st_name[:23] + "..."
            
        dept = info.get('branch', 'N/A')
        if len(dept) > 18:
            dept = dept[:15] + "..."
            
        print(f"| {reg_no:<14} | {st_name:<26} | {dept:<18} |")
        
    print("="*68)
    print(f" Total Registered: {len(db)}")

def search_students(db):
    """Searches by ID or partial match on student name."""
    print("\n--- Search Student Database ---")
    if not db:
        print("Database is empty.")
        return
        
    term = prompt_str("Enter Reg No or Name to search: ").lower()
    matches = {}
    
    for r_no, info in db.items():
        if term == r_no.lower() or term in info.get('name', '').lower():
            matches[r_no] = info
            
    if not matches:
        print(f"No records matched query: '{term}'")
        return
        
    print(f"\nFound {len(matches)} match(es):")
    print("-" * 68)
    print(f"| {'Reg Number':<14} | {'Student Name':<26} | {'Department':<18} |")
    print("-" * 68)
    for r_no, info in matches.items():
        s_name = info.get('name', 'N/A')
        if len(s_name) > 26: s_name = s_name[:23] + "..."
        dept = info.get('branch', 'N/A')
        if len(dept) > 18: dept = dept[:15] + "..."
        print(f"| {r_no:<14} | {s_name:<26} | {dept:<18} |")
    print("-" * 68)

def remove_student_record(db):
    """Permanently deletes a student record after user confirmation."""
    print("\n--- Delete Student Record ---")
    reg_no = prompt_str("Enter Reg No to delete: ").upper()
    
    if reg_no not in db:
        print(f"[!] No record found for ID: {reg_no}")
        return
        
    s_name = db[reg_no].get('name', 'Unknown')
    confirm = prompt_str(f"Are you sure you want to delete '{s_name}' ({reg_no})? (y/n): ").lower()
    
    if confirm in ['y', 'yes']:
        del db[reg_no]
        save_database(db)
        print(f"[+] Record {reg_no} deleted.")
    else:
        print("Deletion canceled.")

def add_or_update_course(db):
    """Adds a new course or updates marks for an existing course."""
    print("\n--- Add / Update Course Grade ---")
    reg_no = prompt_str("Enter Student Reg No: ").upper()
    
    if reg_no not in db:
        print(f"[!] Student '{reg_no}' not registered.")
        return
        
    c_code = prompt_str("Course Code (e.g. CS101): ").upper()
    c_title = prompt_str("Course Title: ")
    credits = prompt_int("Credits (1 to 6): ", min_v=1, max_v=6)
    marks = prompt_float("Marks obtained (0 to 100): ", min_v=0.0, max_v=100.0)
    
    l_grade, g_pts = convert_marks_to_grade(marks)
    
    course_obj = {
        'title': c_title,
        'credits': credits,
        'marks': marks,
        'grade': l_grade,
        'points': g_pts
    }
    
    if 'courses' not in db[reg_no]:
        db[reg_no]['courses'] = {}
        
    db[reg_no]['courses'][c_code] = course_obj
    save_database(db)
    
    print(f"\n[+] Grade saved for {db[reg_no]['name']}: {c_code} -> Grade {l_grade} ({g_pts} pts)")

def delete_course_from_student(db):
    """Removes a specific course from a student's course list."""
    print("\n--- Remove Course from Student ---")
    reg_no = prompt_str("Enter Student Reg No: ").upper()
    
    if reg_no not in db:
        print(f"[!] Student ID '{reg_no}' not found.")
        return
        
    courses = db[reg_no].get('courses', {})
    if not courses:
        print(f"No courses recorded for {reg_no} yet.")
        return
        
    print("\nEnrolled Courses:")
    for code, cdata in courses.items():
        print(f"  - {code}: {cdata.get('title', '')}")
        
    c_code = prompt_str("\nEnter Course Code to remove: ").upper()
    if c_code not in courses:
        print(f"[!] Course '{c_code}' is not in student's record.")
        return
        
    sure = prompt_str(f"Remove '{c_code}' from {reg_no}? (y/n): ").lower()
    if sure in ['y', 'yes']:
        del db[reg_no]['courses'][c_code]
        save_database(db)
        print(f"[+] Course '{c_code}' removed.")
    else:
        print("Removal aborted.")

def render_transcript(db):
    """Generates an ASCII transcript with GPA for a given student."""
    print("\n--- Generate Transcript ---")
    reg_no = prompt_str("Enter Student Reg No: ").upper()
    
    if reg_no not in db:
        print(f"[!] Reg No '{reg_no}' not found.")
        return
        
    st = db[reg_no]
    courses = st.get('courses', {})
    gpa, total_cr = compute_student_gpa(courses)
    
    print("\n" + "="*72)
    print(f"{'ACADEMIC TRANSCRIPT':^72}")
    print("="*72)
    print(f" Student ID : {reg_no}")
    print(f" Name       : {st.get('name', 'N/A')}")
    print(f" Branch     : {st.get('branch', 'N/A')}")
    print("-" * 72)
    
    if not courses:
        print(" No course records found for this student.")
    else:
        print(f"| {'Code':<10} | {'Course Title':<28} | {'Credits':<7} | {'Grade':<5} | {'Points':<6} |")
        print("-" * 72)
        for code, details in courses.items():
            t = details.get('title', 'N/A')
            if len(t) > 28: t = t[:25] + "..."
            cr = details.get('credits', 0)
            gr = details.get('grade', '-')
            pt = details.get('points', 0.0)
            print(f"| {code:<10} | {t:<28} | {cr:<7} | {gr:<5} | {pt:<6.1f} |")
            
        print("-" * 72)
        print(f" Total Credits Earned : {total_cr}")
        print(f" Cumulative GPA (CGPA) : {gpa:.2f}")
    print("="*72)

def export_csv_report(db):
    """Exports all student profiles and overall metrics to CSV format."""
    print("\n--- Exporting Summary to CSV ---")
    if not db:
        print("No student data available to export.")
        return
        
    try:
        with open(EXPORT_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Reg No', 'Name', 'Branch', 'Completed Credits', 'GPA'])
            
            for reg_no, info in db.items():
                courses = info.get('courses', {})
                gpa, tot_cr = compute_student_gpa(courses)
                writer.writerow([
                    reg_no,
                    info.get('name', ''),
                    info.get('branch', ''),
                    tot_cr,
                    f"{gpa:.2f}"
                ])
                
        print(f"[+] Data exported successfully to '{EXPORT_FILE}'.")
        print(f"    Path: {os.path.abspath(EXPORT_FILE)}")
    except OSError as e:
        print(f"[!] Export failed: {e}")

def show_analytics(db):
    """Displays aggregate statistics across the cohort."""
    print("\n" + "="*45)
    print("          BATCH ANALYTICS REPORT")
    print("="*45)
    
    if not db:
        print("No student data to analyze.")
        return
        
    total_count = len(db)
    active_gpas = []
    highest_gpa = -1.0
    lowest_gpa = 11.0
    top_st = None
    low_st = None
    
    for reg_no, info in db.items():
        courses = info.get('courses', {})
        if not courses:
            continue
            
        gpa, _ = compute_student_gpa(courses)
        active_gpas.append(gpa)
        
        if gpa > highest_gpa:
            highest_gpa = gpa
            top_st = (info.get('name'), reg_no, gpa)
            
        if gpa < lowest_gpa:
            lowest_gpa = gpa
            low_st = (info.get('name'), reg_no, gpa)
            
    print(f" Total Registered Students : {total_count}")
    print(f" Students with Grades      : {len(active_gpas)}")
    
    if not active_gpas:
        print(" No grade data entered yet for analytics.")
        print("="*45)
        return
        
    avg_gpa = sum(active_gpas) / len(active_gpas)
    print(f" Cohort Average GPA        : {avg_gpa:.2f}")
    
    if top_st:
        print(f" Highest GPA               : {top_st[2]:.2f} ({top_st[0]} - {top_st[1]})")
    if low_st:
        print(f" Lowest GPA                : {low_st[2]:.2f} ({low_st[0]} - {low_st[1]})")
        
    print("="*45)

def print_main_menu():
    """Prints the CLI application menu."""
    print("\n" + "#"*48)
    print("#  STUDENT ACADEMIC TRACKER & GRADE SYSTEM      #")
    print("#"*48)
    print(" 1. Register New Student")
    print(" 2. View All Registered Students")
    print(" 3. Search Student Records")
    print(" 4. Delete Student Record")
    print(" 5. Add / Update Course Grade")
    print(" 6. Remove a Course")
    print(" 7. Print Academic Transcript")
    print(" 8. Export Data to CSV")
    print(" 9. View Batch Analytics")
    print("10. Save & Exit Program")
    print("#"*48)

def main():
    """Application entry point and core controller loop."""
    print("[*] Initializing system...")
    db = load_database()
    print(f"[*] Loaded {len(db)} student profile(s) from '{DB_FILE}'.")
    
    while True:
        print_main_menu()
        choice = prompt_str("Select an option (1-10): ")
        
        if choice == '1':
            register_new_student(db)
        elif choice == '2':
            list_all_students(db)
        elif choice == '3':
            search_students(db)
        elif choice == '4':
            remove_student_record(db)
        elif choice == '5':
            add_or_update_course(db)
        elif choice == '6':
            delete_course_from_student(db)
        elif choice == '7':
            render_transcript(db)
        elif choice == '8':
            export_csv_report(db)
        elif choice == '9':
            show_analytics(db)
        elif choice == '10':
            print("\nSaving database state...")
            save_database(db)
            print("System closed safely. Goodbye!")
            sys.exit(0)
        else:
            print("[!] Invalid option. Please enter a number between 1 and 10.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Force closed by user interrupt. Exiting...")
        sys.exit(0)