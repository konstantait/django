from django.db.models import IntegerChoices, TextChoices


class DiscountTypes(IntegerChoices):
    FIXED = 0, 'Fixed Amount'
    PERCENTAGE = 1, "Percentage"


class StatusTypes(IntegerChoices):
    ENABLED = 0, 'Enabled'
    DISABLED = 1, 'Disabled'


class RatingTypes(IntegerChoices):
    POOR = 0, 'Poor'
    FAIR = 1, 'Fair'
    GOOD = 2, 'Good'
    VERY_GOOD = 3, 'Very good'
    EXCELLENT = 4, 'Excellent'


class CacheKeys(TextChoices):
    REVIEWS_ALL = 'reviews:all', 'Reviews all'
    CURRENCIES_ALL = 'currencies:all', 'Currencies all'
