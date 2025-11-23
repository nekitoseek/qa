
from helpers.data_gen import random_name, random_price
from config import SELLER_ID
from helpers.data_gen import random_seller_id


# ---------------------------
#     П O З И Т И В Н Ы Е
# ---------------------------

def test_create_item_valid(api):
    """POST-01: Создание объявления с валидными данными"""
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

    item_id = api.extract_id(resp)
    assert item_id is not None


def test_create_items_same_name_different_sellers(api):
    """POST-02: Два объявления с одинаковым name, но разным sellerID"""
    name = random_name()

    payload1 = {
        "sellerID": random_seller_id(),
        "name": name,
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }
    payload2 = {
        "sellerID": random_seller_id(),
        "name": name,
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

    id1 = api.extract_id(r1)
    id2 = api.extract_id(r2)

    assert id1 != id2


def test_create_item_max_name_length(api):
    """POST-03: Максимально длинный name (255 символов)"""
    payload = {
        "sellerID": SELLER_ID,
        "name": "a" * 255,
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }

    resp = api.post_item(payload)
    assert resp.status_code == 200

    item_id = api.extract_id(resp)
    assert item_id is not None


def test_create_same_items_get_different_ids(api):
    """POST-04: Полностью одинаковые данные → разные id"""
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

    r1 = api.post_item(payload)
    r2 = api.post_item(payload)

    assert r1.status_code == 200
    assert r2.status_code == 200

    id1 = api.extract_id(r1)
    id2 = api.extract_id(r2)

    assert id1 != id2


# ---------------------------
#      Н Е Г А Т И В Н Ы Е
# ---------------------------

def test_create_item_empty_body(api):
    """POST-05: Пустой JSON"""
    resp = api.post_item({})
    assert resp.status_code == 400


def test_create_item_no_seller(api):
    """POST-06: Отсутствует sellerID"""
    payload = {
        "name": random_name(),
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }
    resp = api.post_item(payload)
    assert resp.status_code == 400


def test_create_item_no_name(api):
    """POST-07: Отсутствует name"""
    payload = {
        "sellerID": SELLER_ID,
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }
    resp = api.post_item(payload)
    assert resp.status_code == 400


def test_create_item_sellerID_too_small(api):
    """POST-08: sellerID < 111111"""
    payload = {
        "sellerID": 100,
        "name": random_name(),
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }
    resp = api.post_item(payload)
    assert resp.status_code == 400


def test_create_item_sellerID_too_big(api):
    """POST-09: sellerID > 999999"""
    payload = {
        "sellerID": 10000000,
        "name": random_name(),
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }
    resp = api.post_item(payload)
    assert resp.status_code == 400


def test_create_item_sellerID_string(api):
    """POST-10: sellerID строка"""
    payload = {
        "sellerID": "abc",
        "name": random_name(),
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }
    resp = api.post_item(payload)
    assert resp.status_code == 400


def test_create_item_name_number(api):
    """POST-11: name = число"""
    payload = {
        "sellerID": SELLER_ID,
        "name": 123,
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }
    resp = api.post_item(payload)
    assert resp.status_code == 400


def test_create_item_empty_name(api):
    """POST-12: name пустой"""
    payload = {
        "sellerID": SELLER_ID,
        "name": "",
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }
    resp = api.post_item(payload)
    assert resp.status_code == 400


def test_create_item_name_too_long(api):
    """POST-13: name > 255"""
    payload = {
        "sellerID": SELLER_ID,
        "name": "a" * 1000,
        "price": random_price(),
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }
    resp = api.post_item(payload)
    assert resp.status_code in (400, 413)