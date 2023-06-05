from datetime import timedelta

from django.utils import timezone
from django.contrib.sessions.backends.base import SessionBase
from django.db.models.query import QuerySet
from django.core.cache import cache

from core.enums import CacheKeys, StatusTypes
from core.settings import CURRENCY_SESSION_ID

from currencies.models import Currency


def get_currencies() -> QuerySet[Currency]:
    currencies = cache.get(CacheKeys.CURRENCIES_ALL)
    if not currencies:
        currencies = Currency.objects.filter(status=StatusTypes.ENABLED)
        cache.set(CacheKeys.CURRENCIES_ALL, currencies)
    return currencies


def get_outdated_currencies(minutes: int) -> QuerySet[Currency]:
    modified_less_than = timezone.now() - timedelta(minutes=minutes)
    return get_currencies().filter(date_modified__lt=modified_less_than)


def get_currencies_codes() -> list:
    return get_currencies().values_list('code', flat=True)


def get_currency(code: str) -> Currency:
    return get_currencies().get(code=code)


def get_default_currency() -> Currency:
    return get_currencies().get(rate=1)


def get_user_currency(session: SessionBase) -> str:
    code = session.get(CURRENCY_SESSION_ID)
    if not code:
        code = get_default_currency().code
    return code


def update_user_currency(session: SessionBase, code: str) -> None:
    session[CURRENCY_SESSION_ID] = code


# {'code': 'UAH', 'rate': '1.00000'}
# {'code': 'EUR', 'rate': '41.50000'}
# {'code': 'USD', 'rate': '37.60000'}
def update_outdated_currencies_rates(rates: list[dict], minutes=2) -> None:
    if rates:
        default = get_default_currency()
        default_rate = list(filter(lambda x: x['code'] == default.code, rates))[0]['rate'] # noqa
        if default_rate:
            currencies = get_outdated_currencies(minutes)
            for currency in currencies:
                if currency.rate != 1:
                    rate = list(filter(lambda x: x['code'] == currency.code, rates))[0]['rate'] # noqa
                    currency.rate = float(default_rate) / float(rate) # noqa
                    currency.save()

# if default_currency_code = 'UAH'
# rate = rate_UAH
# new_rate_UAH = 1
# new_rate_USD = rate / rate_USD
# new_rate_EUR = rate / rate_EUR
#
# if default_currency_code = 'USD'
# rate = rate_USD
# new_rate_UAH = rate / rate_UAH
# new_rate_USD = 1
# new_rate_EUR = rate / rate_EUR
#
# if default_currency_code = 'EUR'
# rate = rate_EUR
# new_rate_UAH = rate / rate_UAH
# new_rate_EUR = 1
# new_rate_USD = rate / rate_USD
