from django.db.models import IntegerChoices


class DiscountTypes(IntegerChoices):
    FIXED = 0, 'Fixed Amount'
    PERCENTAGE = 1, "Percentage"


class StatusTypes(IntegerChoices):
    ENABLED = 0, 'Enabled'
    DISABLED = 1, 'Disabled'
