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

def test_statistic_valid(api):
    """STAT-01: Создать объявление → получить статистику"""

    # 1. Создаём объявление
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

    # 2. Получаем статистику
    stat_resp = api.get_item_statistic(item_id)
    assert stat_resp.status_code == 200

    stats = stat_resp.json()
    expected_fields = {"contacts", "likes", "viewCount"}
    assert expected_fields.issubset(stats.keys())


# -----------------------------------------------------
#                 Н Е Г А Т И В Н Ы Е
# -----------------------------------------------------

@pytest.mark.parametrize("bad_id", ["123", "abc", "!!!", "", None])
def test_statistic_invalid_id(api, bad_id):
    """STAT-03: Невалидный id → 400"""
    resp = api.get_item_statistic(bad_id)
    assert resp.status_code == 400


def test_statistic_not_found(api):
    """STAT-04: Статистика несуществующего item → 404"""
    fake_id = "11111111-1111-1111-1111-111111111111"
    resp = api.get_item_statistic(fake_id)
    assert resp.status_code == 404