from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from catalog.models import Category, Product
from currencies.models import Currency
from reviews.models import Review
from core.constants import MAX_DIGITS, DECIMAL_PLACES

User = get_user_model()


def test_products_list(client, faker):
    category_name = faker.word()
    category_slug = category_name.lower()
    category = Category.objects.create(
        name=category_name,
        slug=category_slug,
    )
    Currency.objects.create(code='USD', rate=1)
    Currency.objects.create(code='EUR', rate=0.9)
    Currency.objects.create(code='UAH', rate=37)

    for _ in range(3):
        product_name = faker.word()
        product_slug = product_name.lower()
        product = Product.objects.create(
            name=product_name,
            slug=product_slug,
            sku=faker.word(),
            price=faker.pydecimal(
                min_value=0,
                left_digits=DECIMAL_PLACES,
                right_digits=MAX_DIGITS - DECIMAL_PLACES,
            )
        )
        product.categories.set([category])

    url = reverse_lazy('catalog:list', kwargs={'category_slug': f'{category_slug}'}) # noqa
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['products']) == Product.objects.count()


def test_product_detail(client, faker):
    category_name = faker.word()
    category_slug = category_name.lower()
    category = Category.objects.create(
        name=category_name,
        slug=category_slug,
    )

    Currency.objects.create(code='USD', rate=1)
    Currency.objects.create(code='EUR', rate=0.9)
    Currency.objects.create(code='UAH', rate=37)

    product_name = faker.word()
    product_slug = product_name.lower()
    product = Product.objects.create(
        name=product_name,
        slug=product_slug,
        sku=faker.word(),
        price=faker.pydecimal(
            min_value=0,
            left_digits=DECIMAL_PLACES,
            right_digits=MAX_DIGITS - DECIMAL_PLACES,
        )
    )
    product.categories.set([category])

    user, _ = User.objects.get_or_create(
        email=faker.email(),
    )
    for _ in range(3):
        Review.objects.create(
            author=user,
            product=product,
            text=faker.word(),
            )

    url = reverse_lazy('catalog:detail',
                       kwargs={
                           'category_slug': f'{category_slug}',
                           'slug': f'{product_slug}',
                       }) # noqa
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['reviews']) == Review.objects.count()
