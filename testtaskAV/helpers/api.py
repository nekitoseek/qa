import requests
import os

BASE_URL = os.getenv("BASE_URL", "https://qa-internship.avito.com/api/1")

class ApiClient:

    def post_item(self, payload):
        return requests.post(f"{BASE_URL}/item", json=payload)

    def get_item(self, item_id):
        return requests.get(f"{BASE_URL}/item/{item_id}")

    def get_seller_items(self, seller_id):
        return requests.get(f"{BASE_URL}/{seller_id}/item")

    def get_statistics(self, item_id):
        return requests.get(f"{BASE_URL}/statistic/{item_id}")

    def extract_id(self, response):
        """
        Извлекает ID объявления из response.json()["status"]
        """
        status = response.json().get("status", "")
        if " - " in status:
            return status.split(" - ")[-1].strip()
        return None

    def get_item_statistic(self, item_id):
        return requests.get(f"{BASE_URL}/api/1/statistic/{item_id}")