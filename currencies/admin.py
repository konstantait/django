from django.contrib import admin

from currencies.models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'rate', 'date_modified', 'symbol_left', "symbol_right", 'decimal_place', ) # noqa
