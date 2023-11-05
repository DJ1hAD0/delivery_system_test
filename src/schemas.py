from datetime import datetime
from typing import List
from pydantic import BaseModel


class Courier(BaseModel):
    id: int | None = None
    courier_name: str

    class Config:
        allow_population_by_field_name = True

class Order(BaseModel):
    courier_id: int
    region_id: int
    order_name: str


class CourierRegistration(BaseModel):
    courier_name: str
    districts: list[str]

    class Config:
        allow_population_by_field_name = True


class OrderRegistration(BaseModel):
    order_name: str
    order_district: str


class PostOrder(BaseModel):
    name: str
    district: str
