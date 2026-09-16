# Student Management System

A Python-based Command-Line Interface (CLI) application for managing student records, course enrollments, marks, averages, and letter grades. Data is persisted locally in JSON format.

## Features

- **Add New Student**: Register students with unique roll numbers, name, branch, semester, and course list.
- **Record Marks**: Input course marks (0-100) and automatically calculate average percentage and letter grades.
- **Display Records**: View summary table of all students or detailed view of individual student details and course breakdown.
- **Update Student Info**: Update name, branch, semester, add/remove courses, or update course marks with dynamic recalculation of average and grade.
- **Delete Record**: Remove student records with prompt confirmation.
- **Search by Branch**: Filter and view student list by branch.
- **Data Persistence**: Automatically save and load records from `students_data.json`.

## Grade Scale

| Average Percentage | Grade |
| ------------------ | ----- |
| $\ge 90\%$         | A+    |
| $\ge 80\%$         | A     |
| $\ge 70\%$         | B+    |
| $\ge 60\%$         | B     |
| $\ge 50\%$         | C     |
| $\ge 40\%$         | D     |
| $< 40\%$           | F     |

## Prerequisites

- Python 3.x

## How to Run

To start the interactive command-line interface:

```bash
python3 main.py
```

## Running Tests

To run the automated unit test suite:

```bash
python3 -m unittest discover
```
