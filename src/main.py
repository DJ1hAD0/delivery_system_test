from fastapi import FastAPI
from src.database import engine
import src.models
import uvicorn
from src.services import courier, order

src.models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(courier.router, tags=['API курьера'], prefix='/courier')
app.include_router(order.router, tags=['API заказа'], prefix='/order')


@app.get("/")
def root():
    return {"message": "Welcome"}

#
# if __name__ == '__main__':
#     uvicorn.run(app, host="127.0.0.1", port=8000)