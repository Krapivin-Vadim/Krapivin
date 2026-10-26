"""Тесты запросов к сервису заказов."""

import pytest


def test_create_order_returns_201(client, order_payload):
    response = client.post("/orders", json=order_payload)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["account_id"] == order_payload["account_id"]
    assert body["item"] == order_payload["item"]
    assert body["quantity"] == order_payload["quantity"]
    assert body["created_at"]


@pytest.mark.parametrize(
    "broken_field",
    [
        {"quantity": 0},
        {"quantity": -1},
        {"item": ""},
        {"account_id": "не-число"},
    ],
)
def test_invalid_payload_returns_422(client, order_payload, broken_field):
    payload = order_payload | broken_field

    response = client.post("/orders", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize("missing", ["account_id", "item", "quantity"])
def test_missing_field_returns_422(client, order_payload, missing):
    payload = {k: v for k, v in order_payload.items() if k != missing}

    response = client.post("/orders", json=payload)

    assert response.status_code == 422

def test_get_orders_returns_200(client):
    created = client.post("/orders", json=order_payload).json()

    response = client.get(f"/orders/{created['id']}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == created["id"]
    assert body["account_id"] == order_payload["account_id"]
    assert body["item"] == order_payload["item"]
    assert body["quantity"] == order_payload["quantity"]


def test_read_missing_order_returns_404(client):
    response = client.get("/orders/99999")

    assert response.status_code == 404
    assert "99999" in response.json()["detail"]
