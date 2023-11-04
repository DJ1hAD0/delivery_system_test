from datetime import datetime
from typing import List
from pydantic import BaseModel


class Courier(BaseModel):
    id: int | None = None
    courier_name: str

    class Config:
        allow_population_by_field_name = True


class CourierRegistration(BaseModel):
    courier_name: str
    districts: list[str]

    class Config:
        allow_population_by_field_name = True


class PostOrder(BaseModel):
    name: str
    district: str


class CourierRegion(BaseModel):
    courier_id: int
    region_id: int


class OrderRegion(BaseModel):
    order_id: int
    region_id: int
