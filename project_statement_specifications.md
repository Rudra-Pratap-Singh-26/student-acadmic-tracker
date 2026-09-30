# Project Statement & Specifications

## 1. Problem Statement

Educational institutions, academic advisors, and students frequently face challenges in efficiently tracking academic progress and accurately computing performance metrics. Manual calculations of Cumulative Grade Point Averages (CGPA) across varying course credit weights ($1$ to $6$ credits) are error-prone and time-consuming. Furthermore, while full-scale Enterprise Resource Planning (ERP) software can be overly complex and bulky for quick departmental or individual tracking, basic spreadsheet models often lack input validation and structured data persistence.

There is a need for a lightweight, reliable, and zero-dependency solution that automates grade conversions, enforces credit-weighted calculations, maintains structured local records, and provides quick statistical insight into batch-wide performance without requiring complex database infrastructure.

---

## 2. Scope of the Project

The **Student Academic Tracker & Grade System** is an offline, terminal-based Command-Line Interface (CLI) software built using core Python. 

### In-Scope:
* **Student Record Lifecycle:** Creating, searching, viewing, and deleting student profiles.
* **Course & Marks Management:** Enrolling students in courses, assigning credit hours ($1$–$6$), recording numerical marks ($0$–$100$), and updating existing records.
* **Automated Calculations:** Standardized conversion of percentage marks to letter grades (`S`, `A`, `B`, `C`, `D`, `E`, `F`) and automatic calculation of credit-weighted CGPA.
* **Reporting & Transcripts:** Generating formatted ASCII transcripts and exporting summary records to CSV format (`academic_report.csv`).
* **Batch Analytics:** Computing aggregate metrics including cohort average CGPA, active grade distributions, and identifying top and lowest performers.
* **Local Data Persistence:** Automatic reading and writing to a local JSON storage file (`students_data.json`).

### Out-of-Scope:
* Multi-user online authentication or cloud database synchronization.
* Graphical User Interface (GUI) or web application frontend.
* Direct integration with third-party institutional learning management systems (LMS).

---

## 3. Target Users

1. **Academic Advisors & Department Coordinators:**
   * Need a fast, offline tool to maintain student grade rosters, verify CGPA calculations, and export summary CSV reports for departmental records.

2. **University Students:**
   * Require a personal utility to track course progress, calculate cumulative GPA across semesters, and print formatted academic transcripts.

3. **Instructors & Evaluators:**
   * Seek a simple CLI interface to analyze class cohort performance, check score distributions, and identify top/low performers without overhead.

---

## 4. High-Level Features

* **Interactive CLI Interface:** Menu-driven navigation (options 1–10) with input validation against empty entries, out-of-bounds numbers, and non-existent IDs.
* **Dynamic Grade Conversion & Weighted GPA Engine:** Built-in algorithm converting marks to standardized letter grades and calculating overall CGPA using:
  $$\text{CGPA} = \frac{\sum (\text{Course Credits} \times \text{Grade Points})}{\sum \text{Course Credits}}$$
* **ASCII Transcript Rendering:** Custom formatted output presenting student demographics, course codes, titles, credit values, letter grades, and final CGPA.
* **Batch Performance Analytics:** Statistical aggregator computing total registrations, active student GPAs, cohort average GPA, and highest/lowest achievement markers.
* **Dual-Format Persistence:** JSON serialization for state preservation across program sessions and CSV exporting for spreadsheet integration.