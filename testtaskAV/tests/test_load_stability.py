
from concurrent.futures import ThreadPoolExecutor, as_completed
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
#                  НАГРУЗОЧНЫЕ ТЕСТЫ
# -----------------------------------------------------

def test_load_multiple_post_items(api):
    """LOAD-01: Одновременно отправить десятки POST-запросов"""

    def create_item():
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
        return resp

    num_requests = 20  # отправляем 20 запросов одновременно
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_item) for _ in range(num_requests)]
        for future in as_completed(futures):
            results.append(future.result())

    # Проверяем, что все запросы успешные и получили id
    ids = []
    for resp in results:
        assert resp.status_code == 200
        item_id = extract_id(resp)
        assert item_id not in ids  # все id уникальные
        ids.append(item_id)

    assert len(ids) == num_requests


def test_load_multiple_get_same_item(api):
    """LOAD-02: Многократный GET одного и того же item"""

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
    item_id = extract_id(create_resp)

    # Многократные GET
    num_requests = 30
    results = []

    def get_item():
        return api.get_item(item_id)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_item) for _ in range(num_requests)]
        for future in as_completed(futures):
            results.append(future.result())

    # Проверяем, что все GET успешные и возвращают корректные данные
    for resp in results:
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == item_id