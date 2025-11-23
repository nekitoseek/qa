import pytest
from helpers.api import ApiClient

@pytest.fixture()
def api():
    return ApiClient()