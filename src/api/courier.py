from src import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from src.database import get_db
from sqlalchemy import func

router = APIRouter()


@router.get('/')
def get_all_couriers(db: Session = Depends(get_db)):
    result = db.query(models.Courier).all()
    return result

@router.post('/')
def registrate_courier(payload: schemas.CourierRegistration, db: Session = Depends(get_db)):
    new_courier = models.Courier(courier_name=payload.courier_name)
    db.add(new_courier)
    db.commit()
    db.refresh(new_courier)
    for district in payload.districts:
        region_id = db.query(models.Region).filter(models.Region.region_name == district).all()
        if region_id is not None:
            courier_region = models.CourierRegion(courier_id=new_courier.id, region_id=region_id[0].id)
            db.add(courier_region)
    db.commit()
    return {"message": f"courier {new_courier.courier_name} successfully registered"}


@router.get('/{id}')
def get_courier_info(id: int, db: Session = Depends(get_db)):
    courier = db.query(models.Courier).filter(models.Courier.id == id).all()
    if len(courier) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Courier not found")
    active_orders = db.query(models.Order.id, models.Order.order_text).filter(models.Order.courier_id == id).filter(
        models.Order.finish_time.is_(None)).all()
    active_order = {'id': active_orders[0][0], 'order_name': active_orders[0][1]} if len(active_orders) > 0 else None
    avg_order_complete_time = db.query(func.avg(models.Order.finish_time - models.Order.start_time)).filter(
        models.Order.courier_id == id).filter(
        models.Order.finish_time.is_not(None)).all()
    orders_by_day = db.query(func.count(models.Order.id)).group_by(func.date(models.Order.start_time)).filter(
        models.Order.courier_id == id).filter(
        models.Order.finish_time.is_not(None)).all()
    return {'id': courier[0].id,
            'name': courier[0].courier_name,
            'active_order': active_order,
            'avg_order_complete_time': str(avg_order_complete_time[0][0] if len(avg_order_complete_time) > 0 else None),
            'avg_day_orders': int(sum(orders_by_day[0]) / len(orders_by_day[0])) if len(orders_by_day) > 0 else None
            }
