from fastapi import FastAPI
import time
import ManufacturerList
from schemas import EquipmentRequest1
from schemas import EquipmentRequest2
apps = FastAPI()
starttime = time.perf_counter()

@apps.post("/get-Manufacturers", tags=["Get Manufacturers And Models"])
async def get_Manufacturers(data: EquipmentRequest1):
    _manufacturerList =  ManufacturerList.get_all_manufacturers(data.equipmentType)
    return {
        "equipmentType": data.equipmentType,
        "manufacturers": _manufacturerList,
    }

@apps.post("/get-Models-By-Manufacturer", tags=["Get Manufacturers And Models"])
async def get_Models_By_Manufacturer(data: EquipmentRequest2):
    _modelList =  ManufacturerList.get_models_by_manufacturer(data.equipmentType, data.manufacturer, data.types)
    return {
        "equipmentType": data.equipmentType,
        "models": _modelList,
    }
