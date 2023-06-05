from django.shortcuts import render

from currencies.services import update_user_currency


def currency_detail(request, code):
    update_user_currency(request.session, code)
    return render(request, 'catalog/index.html')
