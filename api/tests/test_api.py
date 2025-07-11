import unittest
from fastapi.testclient import TestClient
from api.app import app

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_ping(self):
        response = self.client.get("/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "pong"})

    def test_evaluate_csv_valid(self):
        csv_data = """id,name,shift,rest_days,on_medical_leave,on_vacation,worked_ot_yesterday,exclude_from_ot,role_type
1,Jane Doe,1st,"Tue,Wed",False,False,False,False,signal
2,Sam Green,2nd,"Sat,Sun",True,False,False,False,signal
"""
        files = {"file": ("employees.csv", csv_data, "text/csv")}
        response = self.client.post("/evaluate/csv", files=files, data={"today": "Tue", "is_holiday": "false"})
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("eligible_employees", json_data)
        self.assertTrue(any(e["name"] == "Jane Doe" for e in json_data["eligible_employees"]))
        self.assertTrue(all(e["name"] != "Sam Green" for e in json_data["eligible_employees"]))
