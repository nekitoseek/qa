import pytest
from helpers.data_gen import random_name, random_price
from config import SELLER_ID
import re

def extract_id(resp):
    """
    Извлекает UUID объявления из ответа вида:
    {"status": "Сохранили объявление - d1978119-0906-4be1-bf1d-ea2e8fdca856"}
    """
    text = resp.json()["status"]  # получаем строку
    match = re.search(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", text)
    if match:
        return match.group(0)
    return None


# -----------------------------------------------------
#                  П О З И Т И В Н Ы Е
# -----------------------------------------------------

def test_get_item_valid(api):
    """GET-01: Получение существующего объявления"""

    # Создаём объявление
    payload = {
        "sellerID": SELLER_ID,
        "name": random_name(),
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }
    create_resp = api.post_item(payload)
    assert create_resp.status_code == 200

    item_id = extract_id(create_resp)
    assert item_id is not None

    # Получаем объявление
    resp = api.get_item(item_id)
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1

    item = data[0]
    assert item["id"] == item_id
    assert item["sellerID"] == payload["sellerID"]
    assert item["name"] == payload["name"]
    assert item["price"] == payload["price"]

    # statistics тоже должны быть
    assert "statistics" in item
    assert "viewCount" in item["statistics"]
    assert "likes" in item["statistics"]
    assert "contacts" in item["statistics"]


def test_get_two_items_return_correct_items(api):
    """GET-02: Для двух разных объявлений возвращаются корректные данные"""

    payload1 = {
        "sellerID": SELLER_ID,
        "name": random_name(),
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }
    payload2 = {
        "sellerID": SELLER_ID,
        "name": random_name(),
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }

    r1 = api.post_item(payload1)
    r2 = api.post_item(payload2)

    assert r1.status_code == 200
    assert r2.status_code == 200

    id1 = extract_id(r1)
    id2 = extract_id(r2)

    resp1 = api.get_item(id1)
    resp2 = api.get_item(id2)

    assert resp1.status_code == 200
    assert resp2.status_code == 200

    assert resp1.json()[0]["id"] == id1
    assert resp2.json()[0]["id"] == id2


def test_get_item_has_required_fields(api):
    """GET-03: У объявления есть все обязательные поля"""

    payload = {
        "sellerID": SELLER_ID,
        "name": random_name(),
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }
    resp = api.post_item(payload)
    assert resp.status_code == 200

    item_id = extract_id(resp)
    r = api.get_item(item_id)
    assert r.status_code == 200

    item = r.json()[0]

    expected_fields = {"id", "name", "price", "sellerID", "createdAt", "statistics"}
    assert expected_fields.issubset(item.keys())

    stats_fields = {"viewCount", "likes", "contacts"}
    assert stats_fields.issubset(item["statistics"].keys())


# -----------------------------------------------------
#                 Н Е Г А Т И В Н Ы Е
# -----------------------------------------------------

def test_get_item_not_found(api):
    """GET-04: Несуществующий ID → 404"""

    fake_id = "11111111-1111-1111-1111-111111111111"

    resp = api.get_item(fake_id)
    assert resp.status_code == 404


@pytest.mark.parametrize("bad_id", [
    "123",
    "абв",
    "!!!",
    "",
    None
])
def test_get_item_invalid_id(api, bad_id):
    """GET-05: ID неверного формата → 400 или 404"""

    resp = api.get_item(bad_id)
    assert resp.status_code in (400, 404)