from celery import shared_task

from currencies.services import update_outdated_currencies_rates
from currencies.clients.monobank import monobank_client
from currencies.clients.privatbank import privatbank_client


@shared_task
def get_currencies_privat():
    update_outdated_currencies_rates(privatbank_client.parse())


@shared_task
def get_currencies_mono():
    update_outdated_currencies_rates(monobank_client.parse())
