from pydantic import BaseModel
from typing import Optional

class EquipmentRequest1(BaseModel):
    equipmentType: str = "EV Charger"

class EquipmentRequest2(BaseModel):
    equipmentType: str = "EV Charger"
    manufacturer: str = "ABB"
    types: list[str] = ["Level 2", "Level 3"]

# from pydantic import BaseModel
# from typing import Optional
#
# class EquipmentRequest(BaseModel):
#     equipmentType: str = "EV Charger"
#     modelNo: str = "Terra 54"
#     manufacturer: Optional[str] = "ABB"
#     voltageRating: Optional[str] = "480"