from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_get_order_info():
    response = client.get("/order/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "status": 2
    }


def test_registrate_order():
    response = client.post(
        "/order/", headers={},
        json={
            "order_name": "Привезти пиццу",
            "order_district": "Железнодорожный"
        }
    )
    assert response.status_code == 200
    assert response.json()["courier_id"] == 2


def test_finish_order():
    response = client.post(
        "/order/4", headers={}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Order with id 4 has been closed"
    }
    response = client.post(
        "/order/4", headers={}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Order is already closed"
    }
    response = client.post(
        "/order/444", headers={}
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Order not found"
    }
