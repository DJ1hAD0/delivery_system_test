from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_registrate_courier():
    response = client.post(
        "/courier/", headers={},
        json={
            "courier_name": "Сергей",
            "districts": [
                "Железнодорожный",
                "Октябрьский"
            ]
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "courier Сергей successfully registered"
    }

def test_get_all_couriers():
    response = client.get("/courier/", headers={})
    assert response.status_code == 200
    assert response.json() == [
        {
            "courier_name": "Пётр",
            "id": 1
        },
        {
            "courier_name": "Василий",
            "id": 2
        },
        {
            "courier_name": "Егор",
            "id": 3
        }
    ]


def test_get_courier_info():
    response = client.get("/courier/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Пётр",
        "active_order": {
            "id": 4,
            "order_name": "Заказ Петра в октябрьском не завершенный"
        },
        "avg_order_complete_time": "4:30:00",
        "avg_day_orders": 2
    }



