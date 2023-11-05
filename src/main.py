from fastapi import FastAPI
from database import engine
import models
import uvicorn
from src.api import courier, order

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(courier.router, tags=['API курьер'], prefix='/courier')
app.include_router(order.router, tags=['API заказ'], prefix='/order')


@app.get("/")
def root():
    return {"message": "Welcome"}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)