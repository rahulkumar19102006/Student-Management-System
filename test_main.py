import unittest
from unittest.mock import patch
import os
import io
import main

class TestHelpersAndPersistence(unittest.TestCase):
    def setUp(self):
        self.original_filename = main.filename
        main.filename = "test_students_data.json"
        main.students_db = {}

    def tearDown(self):
        if os.path.exists("test_students_data.json"):
            os.remove("test_students_data.json")
        main.filename = self.original_filename

    def test_get_grade(self):
        self.assertEqual(main.get_grade(95), "A+")
        self.assertEqual(main.get_grade(90), "A+")
        self.assertEqual(main.get_grade(85), "A")
        self.assertEqual(main.get_grade(80), "A")
        self.assertEqual(main.get_grade(75), "B+")
        self.assertEqual(main.get_grade(70), "B+")
        self.assertEqual(main.get_grade(65), "B")
        self.assertEqual(main.get_grade(60), "B")
        self.assertEqual(main.get_grade(55), "C")
        self.assertEqual(main.get_grade(50), "C")
        self.assertEqual(main.get_grade(45), "D")
        self.assertEqual(main.get_grade(40), "D")
        self.assertEqual(main.get_grade(35), "F")

    def test_recalculate_student_stats(self):
        student = {
            "marks": {"Math": 80.0, "Science": 90.0},
            "average": 0.0,
            "grade": "N/A"
        }
        main.recalculate_student_stats(student)
        self.assertAlmostEqual(student["average"], 85.0)
        self.assertEqual(student["grade"], "A")

        empty_student = {
            "marks": {},
            "average": 100.0,
            "grade": "A+"
        }
        main.recalculate_student_stats(empty_student)
        self.assertEqual(empty_student["average"], 0.0)
        self.assertEqual(empty_student["grade"], "N/A")

    def test_save_and_load_data(self):
        main.students_db = {
            "101": {
                "name": "Alice",
                "branch": "CSE",
                "semester": 1,
                "courses": ["Math"],
                "marks": {"Math": 95.0},
                "average": 95.0,
                "grade": "A+"
            }
        }
        main.save_data()
        self.assertTrue(os.path.exists("test_students_data.json"))

        main.students_db = {}
        main.load_data()
        self.assertIn("101", main.students_db)
        self.assertEqual(main.students_db["101"]["name"], "Alice")


class TestStudentOperations(unittest.TestCase):
    def setUp(self):
        self.original_filename = main.filename
        main.filename = "test_students_data.json"
        main.students_db = {}

    def tearDown(self):
        if os.path.exists("test_students_data.json"):
            os.remove("test_students_data.json")
        main.filename = self.original_filename

    @patch('builtins.input', side_effect=["101", "Bob", "ECE", "2", "Math, Physics"])
    def test_add_student(self, mock_input):
        main.add_student()
        self.assertIn("101", main.students_db)
        self.assertEqual(main.students_db["101"]["name"], "Bob")
        self.assertEqual(main.students_db["101"]["branch"], "ECE")
        self.assertEqual(main.students_db["101"]["semester"], 2)
        self.assertEqual(main.students_db["101"]["courses"], ["Math", "Physics"])

    @patch('builtins.input', side_effect=["101", "85.0", "95.0"])
    def test_record_marks(self, mock_input):
        main.students_db["101"] = {
            "name": "Bob",
            "branch": "ECE",
            "semester": 2,
            "courses": ["Math", "Physics"],
            "marks": {},
            "average": 0.0,
            "grade": "N/A"
        }
        main.record_marks()
        self.assertEqual(main.students_db["101"]["marks"]["Math"], 85.0)
        self.assertEqual(main.students_db["101"]["marks"]["Physics"], 95.0)
        self.assertEqual(main.students_db["101"]["average"], 90.0)
        self.assertEqual(main.students_db["101"]["grade"], "A+")

    @patch('builtins.input', side_effect=["101", "1", "Bob Smith"])
    def test_update_student_name(self, mock_input):
        main.students_db["101"] = {
            "name": "Bob",
            "branch": "ECE",
            "semester": 2,
            "courses": ["Math"],
            "marks": {"Math": 85.0},
            "average": 85.0,
            "grade": "A"
        }
        main.update_student()
        self.assertEqual(main.students_db["101"]["name"], "Bob Smith")

    @patch('builtins.input', side_effect=["101", "6", "Math", "95.0"])
    def test_update_student_marks(self, mock_input):
        main.students_db["101"] = {
            "name": "Bob",
            "branch": "ECE",
            "semester": 2,
            "courses": ["Math"],
            "marks": {"Math": 85.0},
            "average": 85.0,
            "grade": "A"
        }
        main.update_student()
        self.assertEqual(main.students_db["101"]["marks"]["Math"], 95.0)
        self.assertEqual(main.students_db["101"]["average"], 95.0)
        self.assertEqual(main.students_db["101"]["grade"], "A+")

    @patch('builtins.input', side_effect=["101", "yes"])
    def test_delete_student(self, mock_input):
        main.students_db["101"] = {
            "name": "Bob",
            "branch": "ECE",
            "semester": 2,
            "courses": ["Math"],
            "marks": {},
            "average": 0.0,
            "grade": "N/A"
        }
        main.delete_student()
        self.assertNotIn("101", main.students_db)

    @patch('builtins.input', side_effect=["ECE"])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_search_by_branch(self, mock_stdout, mock_input):
        main.students_db["101"] = {
            "name": "Bob",
            "branch": "ECE",
            "semester": 2,
            "courses": [],
            "marks": {},
            "average": 0.0,
            "grade": "N/A"
        }
        main.search_by_branch()
        output = mock_stdout.getvalue()
        self.assertIn("Total students in ECE: 1", output)


if __name__ == "__main__":
    unittest.main()
