from src import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from src.database import get_db
from sqlalchemy import func
from sqlalchemy import update

router = APIRouter()


@router.post('/')
def registrate_order(payload: schemas.OrderRegistration, db: Session = Depends(get_db)):
    region_id = db.query(models.Region).filter(models.Region.region_name == payload.order_district).all()
    buzy_couriers = db.query(models.Order.courier_id).filter(models.Order.finish_time.is_(None))
    if len(region_id) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Region not found")
    print(buzy_couriers)
    result = db.query(models.Courier.id).join(models.CourierRegion).filter(
        models.Region.region_name == payload.order_district).all()
    return {"status": "success", "note": result}


@router.get('/{id}')
def get_order(id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order.id, models.Order.finish_time).filter(models.Order.id == id).all()
    if len(order) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {'id': order[0].id, 'status': 1 if order[0].finish_time is None else 2}

@router.post('/{id}')
def finish_order(id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order.id, models.Order.finish_time).filter(models.Order.id == id).all()
    if len(order) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if order[0][1] is not None:
        return {"message": "Order is already closed"}
    update_statement = update(models.Order).where(models.Order.id == id).values({'finish_time': func.now()})

