# from django.contrib.auth import get_user_model
# from django.urls import reverse_lazy

# from catalog.models import Product
from currencies.tasks import get_currencies_privat, get_currencies_mono, update_currency_rate # noqa
# from currencies.api_client import APIBaseClient


def test_currency(mocker):
    get_currencies_privat()
    get_currencies_mono()
    monobank = mocker.patch('currencies.clients.monobank.mono.exchange')
    assert monobank.call_count == 0
    monobank.return_value = [
        {'code': 'USD', 'rate': '37.4406'},
        {'code': 'EUR', 'rate': '41.8008'},
    ]
    get_currencies_mono()
    assert monobank.call_count == 1
    assert update_currency_rate(None) is None
