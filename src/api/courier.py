from src import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from src.database import get_db

router = APIRouter()


@router.get('/')
def get_all_couriers(db: Session = Depends(get_db)):
    result = db.query(models.Courier).all()
    return result

"""Дописать метод"""

# @router.post('/')
# def registrate_courier(payload: schemas.CourierRegistration, db: Session = Depends(get_db)):
#     new_courier = schemas.Courier(courier_name=payload.courier_name)
#     for district in payload.districts:
#         region_id = db.query(models.Region).filter(models.Region.region_name == district).all()
#         if region_id is not None:
#             print(region_id[0].id)
#             print(new_courier)
#     #         courier_region = schemas.CourierRegion(courier_id=new_courier.id, region_id=region_id)
#     #         db.add(courier_region)
#     # db.add(new_courier)
#     # db.commit()
#     return {"status": "success", "note": new_courier}

@router.get('/{id}')
def get_all_couriers(id: int, db: Session = Depends(get_db)):
    courier = db.query(models.Courier).filter(models.Courier.id == id).all()
    active_orders = db.query(models.Order).filter(models.Order.courier_id == id).filter(models.Order.finish_time is None).all()
    return {courier, active_orders}