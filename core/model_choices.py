from django.db.models import IntegerChoices


class DiscountTypes(IntegerChoices):
    CASH = 0, 'cash'
    PERCENT = 1, "percent"
