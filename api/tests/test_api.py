from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

def test_evaluate_csv_valid():
    csv_data = """id,name,shift,rest_days,on_medical_leave,on_vacation,worked_ot_yesterday,exclude_from_ot,role_type
1,Jane Doe,1st,"Tue,Wed",False,False,False,False,signal
2,Sam Green,2nd,"Sat,Sun",True,False,False,False,signal
"""
    files = {"file": ("employees.csv", csv_data, "text/csv")}
    response = client.post("/evaluate/csv", files=files, data={"today": "Tue", "is_holiday": "false"})
    assert response.status_code == 200
    json_data = response.json()
    assert "eligible_employees" in json_data
    assert any(e["name"] == "Jane Doe" for e in json_data["eligible_employees"])
    assert all(e["name"] != "Sam Green" for e in json_data["eligible_employees"])
