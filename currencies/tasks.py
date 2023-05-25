from datetime import timedelta
from celery import shared_task
from django.utils import timezone


from currencies.clients.privatbank import privat
from currencies.clients.monobank import mono
from currencies.models import Currency


def update_currency_rate(rates):
    if not rates:
        return
    rates.append({'code': 'UAH', 'rate': '1.00000'})
    default_currency = Currency.objects.filter(rate=1).first()
    rate = list(filter(lambda x: x['code'] == default_currency.code, rates))[0]['rate'] # noqa
    currencies = Currency.objects.filter(date_modified__lt=timezone.now() - timedelta(minutes=2)) # noqa
    for currency in currencies:
        if currency.rate != 1:
            currency.rate = float(rate) / float(list(filter(lambda x: x['code'] == currency.code, rates))[0]['rate']) # noqa
            currency.save()


@shared_task
def get_currencies_privat():
    rates = privat.exchange()
    update_currency_rate(rates)


@shared_task
def get_currencies_mono():
    rates = mono.exchange()
    update_currency_rate(rates)

# {'code': 'UAH', 'rate': '1.00000'}
#
# {'code': 'EUR', 'rate': '41.50000'}
# {'code': 'USD', 'rate': '37.60000'}

# if default_currency_code = 'UAH'
# rate = rate_UAH
#
# new_rate_UAH = 1
# new_rate_USD = rate / rate_USD
# new_rate_EUR = rate / rate_EUR
#
# if default_currency_code = 'USD'
# rate = rate_USD
#
# new_rate_UAH = rate / rate_UAH
# new_rate_USD = 1
# new_rate_EUR = rate / rate_EUR
#
# if default_currency_code = 'EUR'
# rate = rate_EUR
#
# new_rate_UAH = rate / rate_UAH
# new_rate_EUR = 1
# new_rate_USD = rate / rate_USD
