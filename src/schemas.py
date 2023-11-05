from pydantic import BaseModel


class CourierRegistration(BaseModel):
    courier_name: str
    districts: list[str]


class OrderRegistration(BaseModel):
    order_name: str
    order_district: str
