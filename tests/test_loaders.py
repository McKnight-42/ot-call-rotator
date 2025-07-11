import unittest
import tempfile
import os
from main import load_employees
from models import Employee

class TestLoaders(unittest.TestCase):

    def test_load_employees_valid_data(self):
        data = """id,name,shift,rest_days,on_medical_leave,on_vacation,worked_ot_yesterday,exclude_from_ot,role_type
1,Jane Doe,1st,"Tue,Wed",False,False,False,False,signal
2,Sam Green,2nd,"Sat,Sun",True,False,False,False,signal
"""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            tmpfile.write(data)
            tmpfile.flush()
            employees = load_employees(tmpfile.name)
            self.assertEqual(len(employees), 2)
            self.assertIsInstance(employees[0], Employee)
            self.assertIsInstance(employees[0].rest_days, list)
            self.assertFalse(employees[0].on_medical_leave)
            self.assertTrue(employees[1].on_medical_leave)
        os.unlink(tmpfile.name)

    def test_load_employees_handles_boolean_strings(self):
        data = """id,name,shift,rest_days,on_medical_leave,on_vacation,worked_ot_yesterday,exclude_from_ot,role_type
1,Test,1st,"Mon",True,False,True,False,signal
"""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            tmpfile.write(data)
            tmpfile.flush()
            employees = load_employees(tmpfile.name)
            self.assertTrue(employees[0].on_medical_leave)
            self.assertFalse(employees[0].on_vacation)
            self.assertTrue(employees[0].worked_ot_yesterday)
        os.unlink(tmpfile.name)

if __name__ == "__main__":
    unittest.main()
