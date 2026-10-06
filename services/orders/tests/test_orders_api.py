"""Заведомо падающий тест

СЕЙЧАС ОН ПРОПУСКАЕТСЯ. Снимите строку со skip ниже, запустите проверки
и убедитесь, что тест падает. Это нормальное и правильное состояние:
сначала появляется тест, который описывает нужное поведение, и только
потом — код, который заставляет его пройти.

"""

import pytest


def test_create_order_returns_201(client):
    payload = {"account_id": 1, "item_id": 1, "quantity": 2}

    response = client.post("/orders", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["account_id"] == payload["account_id"]
    assert body["item"] == payload["item"]
    assert body["quantity"] == payload["quantity"]


@pytest.mark.parametrize(
    "broken_field",
    [
        {"id": 0},
        {"item_id": 0},
        {"account_id": 0},
        {"quantity": 0},
    ],
)
def test_invalid_payload_returns_422(client, order_payload, broken_field):
    payload = order_payload | broken_field

    response = client.post("/orders", json=payload)

    assert response.status_code == 422
