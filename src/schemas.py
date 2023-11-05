from pydantic import BaseModel

class CourierRegistration(BaseModel):
    courier_name: str
    districts: list[str]

    class Config:
        allow_population_by_field_name = True


class OrderRegistration(BaseModel):
    order_name: str
    order_district: str

