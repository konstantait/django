from datetime import timedelta

from django.utils import timezone
from django.db.models.query import QuerySet
from django.core.cache import cache

from core.enums import CacheKeys, StatusTypes

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


def get_currency(code: str) -> Currency:
    return get_currencies().get(code=code)


def get_default_currency() -> Currency:
    return get_currencies().get(rate=1)


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
