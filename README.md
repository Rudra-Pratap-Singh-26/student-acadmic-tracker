# Student Academic Tracker & Grade System

A comprehensive, menu-driven Command Line Interface (CLI) application developed in pure Python to manage student profiles, calculate credit-weighted GPAs, generate formatted academic transcripts, export performance reports, and analyze batch cohort performance statistics.

**Author:** Rudra Pratap Singh  
**Language:** Python 3.8+  
**Dependencies:** Pure Python (Standard Library Only)  

---

## Executive Summary

The **Student Academic Tracker & Grade System** provides educational administrators and students with a lightweight, database-free solution for tracking academic performance. It automatically converts raw numerical grades into letter grades, computes exact credit-weighted Cumulative Grade Point Averages (CGPA), renders terminal-based transcripts, and yields cohort analytics. All data is persisted locally in JSON format and can be exported to standard CSV files.

---

## Key Features

* **Student Profile Management**: Register new students with unique registration IDs, search profiles by ID or partial name, list all enrolled students, and safely remove records.
* **Automated Grade Conversion**: Automatically maps numerical marks ($0 - 100$) to corresponding letter grades ($S, A, B, C, D, E, F$) and grade points ($0.0 - 10.0$).
* **Credit-Weighted GPA Engine**: Calculates accurate cumulative GPAs based on individual course credit values ($1 - 6$).
* **ASCII Academic Transcripts**: Renders clean, formatted terminal-based transcripts displaying course details, earned credits, and overall CGPA.
* **Batch Analytics Engine**: Computes cohort metrics, including total enrolled students, overall GPA average, top-performing student, and lowest-performing student.
* **Data Persistence & CSV Export**: Automatically saves and loads state from `students_data.json` and exports tabular summary reports to `academic_report.csv`.

---

## Grading Scale & Formula

### Grade Mapping Scale

| Marks Range | Letter Grade | Grade Points | Performance Description |
| :--- | :---: | :---: | :--- |
| $90 \le \text{Marks} \le 100$ | **S** | $10.0$ | Outstanding |
| $80 \le \text{Marks} < 90$ | **A** | $9.0$ | Excellent |
| $70 \le \text{Marks} < 80$ | **B** | $8.0$ | Very Good |
| $60 \le \text{Marks} < 70$ | **C** | $7.0$ | Good |
| $50 \le \text{Marks} < 60$ | **D** | $6.0$ | Satisfactory |
| $40 \le \text{Marks} < 50$ | **E** | $5.0$ | Pass |
| $\text{Marks} < 40$ | **F** | $0.0$ | Fail |

### Cumulative GPA Formula

The Cumulative Grade Point Average (CGPA) is calculated using the weighted average formula:

$$
\text{GPA} = \frac{\sum_{i=1}^{n} (\text{Credits}_i \times \text{Grade Points}_i)}{\sum_{i=1}^{n} \text{Credits}_i}
$$

*Where $n$ is the total number of courses taken by the student.*

---

## File Structure

```text
student-academic-tracker/
│
├── student_academic_tracker.py   # Main Python source code
├── students_data.json            # Local JSON database (Auto-generated)
├── academic_report.csv           # Exported summary report (Auto-generated)
└── README.md                     # Project documentation
```

---

## Step-by-Step Setup & Execution Guide

Follow these step-by-step instructions to set up, configure, and execute the application.

### Prerequisites

* **Python 3.6 or higher**: Ensure Python is installed on your system. You can verify your Python version by running:

  * **Windows**:
    ```bash
    python --version
    ```
  * **macOS / Linux**:
    ```bash
    python3 --version
    ```

---

### Step 1: Obtain the Project Files

Clone the repository or download the source code into a directory on your machine:

```bash
git clone https://github.com/your-username/student-academic-tracker.git
cd student-academic-tracker
```

*(If downloaded as a ZIP archive, extract the files and navigate into the extracted folder using your terminal.)*

---

### Step 2: Set Up an Isolated Environment (Optional, Recommended)

Although the project uses standard library modules, creating a isolated Python virtual environment ensures clean execution without system-level library conflicts.

* **On Windows (Command Prompt / PowerShell)**:
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

* **On macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

---

### Step 3: Verify Dependencies

This application is built entirely using Python's built-in standard library (`json`, `csv`, `os`, `sys`). **No third-party packages or external `pip` installations are required.**

You can verify that all standard modules are available by running:

```bash
python -c "import json, csv, os, sys; print('[+] All required modules are available.')"
```

---

### Step 4: System Configuration

The application is pre-configured to run out of the box. Default configuration constants are defined at the top of `student_academic_tracker.py`:

```python
# File paths for local persistence and reporting
DB_FILE = 'students_data.json'
EXPORT_FILE = 'academic_report.csv'
```

* **Data File (`DB_FILE`)**: Stores JSON records. If this file does not exist, the system will automatically create it upon first launch or data entry.
* **Export File (`EXPORT_FILE`)**: Defines the default file path when generating CSV reports via Option 8 in the main menu.

*If custom file paths or names are desired, you can edit these two variables directly in `student_academic_tracker.py` using any text editor.*

---

### Step 5: Execute the Program

Launch the application controller loop by running the script:

* **Windows**:
  ```cmd
  python student_academic_tracker.py
  ```

* **macOS / Linux**:
  ```bash
  python3 student_academic_tracker.py
  ```

---

## Using the Application (Menu Walkthrough)

Upon launch, you will be presented with the main CLI navigation menu:

```text
################################################
#  STUDENT ACADEMIC TRACKER & GRADE SYSTEM      #
################################################
 1. Register New Student
 2. View All Registered Students
 3. Search Student Records
 4. Delete Student Record
 5. Add / Update Course Grade
 6. Remove a Course
 7. Print Academic Transcript
 8. Export Data to CSV
 9. View Batch Analytics
10. Save & Exit Program
################################################
```

### Typical Workflow

1. **Register a Student** (`Option 1`): Enter a unique Registration Number (e.g., `REG101`), Full Name, and Department.
2. **Add Course Grades** (`Option 5`): Input the student ID, course code (e.g., `CS101`), title, credit hours ($1 - 6$), and numerical marks ($0 - 100$). The system computes the letter grade and grade points automatically.
3. **Generate Academic Transcript** (`Option 7`): Print a formatted transcript showing completed courses, total credits earned, and CGPA.
4. **View Cohort Performance** (`Option 9`): Inspect aggregate metrics across all students in the system.
5. **Export Metrics** (`Option 8`): Generate `academic_report.csv` for reporting or analysis in Excel.
6. **Save & Exit** (`Option 10`): Safely write all changes to disk and terminate the program.

---

## Troubleshooting & Common Questions

* **`python: command not found`**:
  Ensure Python is installed and added to your system's `PATH` environment variable. On Linux/macOS, try using `python3` instead of `python`.
* **Corrupted Database File (`students_data.json`)**:
  If the JSON file becomes unreadable or manually corrupted, the application will notify you and safely start with an empty record set. You can delete or rename `students_data.json` to start fresh.
* **Permission Denied Errors**:
  Ensure you have write permissions in the directory where the application is stored so it can create `students_data.json` and `academic_report.csv`.

---

## Author & Maintainer

* **Developer**: Rudra Pratap Singh
* **Project**: Student Academic Tracker & Grade System
