import random

from src import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from src.database import get_db
from sqlalchemy import func
from sqlalchemy import update, distinct

router = APIRouter()


@router.post('/')
def registrate_order(payload: schemas.OrderRegistration, db: Session = Depends(get_db)) -> dict:
    """
    Регистрация заказа в системе
    :param payload: словарь, содержащий поля order_name: str - наименование (текст) заказа, order_district: str - наименование района
    :param db: сессия для соединения с БД
    :return: словарь, содержащий:
    id - идентификатор созданного заказа
    courier_id - идентификатор курьера, которому назначен заказ
    если регион отсутствует в БД, возвращается 404
    если нет свободных курьеров в данном районе, возвращается соответствующее сообщение
    """
    region_id = db.query(models.Region.id).filter(models.Region.region_name == payload.order_district).all()
    if len(region_id) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Region not found")
    buzy_couriers = [courier_id[0] for courier_id in
                     db.query(models.Order.courier_id).filter(models.Order.finish_time.is_(None)).all()]
    all_couriers_has_region = [courier_id[0] for courier_id in db.query(models.Courier.id).join(models.CourierRegion).join(models.Region).filter(
        models.Region.region_name == payload.order_district).all()]
    free_couriers_in_region = list(filter(lambda item: item not in buzy_couriers, all_couriers_has_region))
    if len(free_couriers_in_region) == 0:
        return {"message": "There are no free couriers in this region"}
    random_free_courier_id = random.choice(free_couriers_in_region)
    new_order = models.Order(order_text=payload.order_name, region_id=region_id[0][0], courier_id=random_free_courier_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    db.add(models.OrderRegion(order_id=new_order.id, region_id=region_id[0][0]))
    db.commit()
    return {"order_id": new_order.id, "courier_id": random_free_courier_id}


@router.get('/{id}')
def get_order_info(id: int, db: Session = Depends(get_db)) -> dict:
    """
    Вывод информации о конкретном заказе
    :param id: идентификатор заказа
    :param db: сессия для подключения к БД
    :return: словарь, содержащий:
    id - идентификатор заказа
    status - статус заказа. 1 - в работе, 2 - завершен
    если заказ отсутствует в системе, возвращается 404 ошибка
    """
    order = db.query(models.Order.id, models.Order.finish_time).filter(models.Order.id == id).all()
    if len(order) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {'id': order[0].id, 'status': 1 if order[0].finish_time is None else 2}

@router.post('/{id}')
def finish_order(id: int, db: Session = Depends(get_db)) -> dict:
    """
    Завершение заказа
    :param id: идентификатор заказа, который требуется завершить
    :param db: сессия для подключения к БД
    :return: сообщение об успешном завершении заказа
    если заказ отсутствует в системе, возвращается 404 ошибка
    если заказ уже закрыт, отображается соответствующее сообщение
    """
    order = db.query(models.Order.id, models.Order.finish_time).filter(models.Order.id == id).all()
    if len(order) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if order[0][1] is not None:
        return {"message": "Order is already closed"}
    update_statement = update(models.Order).where(models.Order.id == id).values({'finish_time': func.now()})
    db.execute(update_statement)
    db.commit()
    return {'message': f"Order with id {id} has been closed"}

