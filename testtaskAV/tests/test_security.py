import pytest
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

def test_security_xss_in_name(api):
    """SEC-01: Проверка защиты от XSS через поле name"""

    payload = {
        "sellerID": SELLER_ID,
        "name": "<script>alert('xss')</script>",
        "price": 100
    }

    resp = api.post_item(payload)
    assert resp.status_code == 200

    item_id = extract_id(resp)

    # Делаем GET и убеждаемся, что HTML-тэги не выполняются
    get_resp = api.get_item(item_id)
    assert get_resp.status_code == 200

    data = get_resp.json()[0]
    assert data["name"] == payload["name"]  # хранится как обычный текст


def test_security_sql_injection_in_name(api):
    """SEC-02: Проверка защиты от SQL-инъекций"""

    injection = "\" OR 1=1 --"

    payload = {
        "sellerID": SELLER_ID,
        "name": injection,
        "price": 150,
        "statistics": {
            "likes": 5,
            "viewCount": 150,
            "contacts": 9213381839
        }
    }

    resp = api.post_item(payload)

    # API должно безопасно обработать строку
    assert resp.status_code == 200

    item_id = extract_id(resp)

    get_resp = api.get_item(item_id)
    assert get_resp.status_code == 200

    data = get_resp.json()[0]

    # Поле должно сохраниться как есть, без выполнения инъекции
    assert data["name"] == injection
    assert data["id"] == item_id