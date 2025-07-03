from fastapi import FastAPI
import time
import datetime
import ManufacturerList
from ImageURL import ImageURL
from SpecSheetURL import SpecSheetURL
from schemas import EquipmentRequest, EquipmentRequest1, EquipmentRequest2
from apscheduler.schedulers.background import BackgroundScheduler
from equipmentListUpdater import equipmentDBlistUpdater

apps = FastAPI()
starttime = time.perf_counter()

def scheduled_task():

    print(f"Task executed at {datetime.datetime.now()}")

scheduler = BackgroundScheduler()
# Run every Sunday at 00:00
scheduler.add_job(scheduled_task, 'cron', day_of_week='sun', hour=0, minute=0)
scheduler.start()

@apps.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@apps.post("/get-Manufacturers", tags=["Get Manufacturers And Models"])
async def get_Manufacturers(data: EquipmentRequest1):
    _manufacturerList = ManufacturerList.get_all_manufacturers(data.equipmentType)
    return {
        "equipmentType": data.equipmentType,
        "manufacturers": _manufacturerList,
    }

@apps.post("/get-Models-By-Manufacturer", tags=["Get Manufacturers And Models"])
async def get_Models_By_Manufacturer(data: EquipmentRequest2):
    _modelList = ManufacturerList.get_models_by_manufacturer(data.equipmentType, data.manufacturer, data.types)
    return {
        "equipmentType": data.equipmentType,
        "models": _modelList,
    }

@apps.post("/get-imageurl-and-specsheeturl", tags=["Get ImageURL And SpecSheetURL"])
async def get_imageurl_and_specsheeturl(data: EquipmentRequest):
    _ImageURL = ImageURL(data.dict())
    _SpecSheetURL = SpecSheetURL(data.dict())
    best_url = _ImageURL.imageURLFinder()
    spec_url = _SpecSheetURL.specSheet(max_pages=3, delay=2)
    return {
        "equipmentType": data.equipmentType,
        "modelNo": data.modelNo,
        "specSheetUrl": spec_url or "Not found",
        "frontImageUrl": best_url or "Not found",
        "time taken": time.perf_counter() - starttime,
    }

