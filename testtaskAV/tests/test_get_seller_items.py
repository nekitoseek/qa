import pytest
from helpers.data_gen import random_name, random_price, random_seller_id


# -----------------------------------------------------
#                  П О З И Т И В Н Ы Е
# -----------------------------------------------------

def test_seller_items_multiple(api):
    """SELL-01: Создать объявления с одним sellerID и получить их"""

    seller = random_seller_id()

    payload1 = {
        "sellerID": seller,
        "name": random_name(),
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }
    payload2 = {
        "sellerID": seller,
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

    resp = api.get_seller_items(seller)
    assert resp.status_code == 200

    items = resp.json()
    assert isinstance(items, list)
    assert len(items) >= 2  # может быть больше, если вручную уже создавали

    # Проверяем, что в списке есть оба созданных name
    returned_names = [item["name"] for item in items]
    assert payload1["name"] in returned_names
    assert payload2["name"] in returned_names


def test_seller_items_empty(api):
    """SELL-02: У продавца нет объявлений — должен вернуться пустой список"""

    seller = random_seller_id()

    resp = api.get_seller_items(seller)
    assert resp.status_code == 200

    assert resp.json() == []


# -----------------------------------------------------
#                 Н Е Г А Т И В Н Ы Е
# -----------------------------------------------------

def test_seller_items_sellerID_too_small(api):
    """SELL-04: sellerID < 111111 → 400"""
    resp = api.get_seller_items(100)  # сильно меньше минимума
    assert resp.status_code == 400


def test_seller_items_sellerID_too_big(api):
    """SELL-05: sellerID > 999999 → 400"""
    resp = api.get_seller_items(10000000)  # сильно больше максимума
    assert resp.status_code == 400


@pytest.mark.parametrize("bad_id", ["abc", "12ab", "!@#", "", None])
def test_seller_items_invalid_format(api, bad_id):
    """SELL-06: Некорректный формат sellerID (строка, символы, пусто) → 400"""
    resp = api.get_seller_items(bad_id)
    assert resp.status_code == 400
