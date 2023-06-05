from core.settings import CURRENCY_SESSION_ID # noqa

from currencies.services import (
    get_user_currency,
    get_currencies
)


def currencies(request):
    return {
        CURRENCY_SESSION_ID: {
            'code': get_user_currency(request.session),
            'all': get_currencies()
        }
    }
