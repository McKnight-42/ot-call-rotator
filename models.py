from pydantic import BaseModel
from typing import List

class Employee(BaseModel):
    id: int
    name: str
    shift: str
    rest_days: List[str]
    on_medical_leave: bool
    on_vacation: bool
    worked_ot_yesterday: bool
    exclude_from_ot: bool
    role_type: str
