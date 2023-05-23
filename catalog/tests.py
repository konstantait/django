from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from catalog.models import Product
from reviews.models import Review

User = get_user_model()


def test_products_list(
        client,
        category_factory,
        product_factory
):
    category = category_factory(name='Sofas')
    # for 100% test coverage
    assert str(category) == 'Sofas'
    for _ in range(3):
        product_factory(categories=(category, ))
    kwargs = {
        'category_slug': f'{category.slug}'
    }
    url = reverse_lazy('catalog:list', kwargs=kwargs)
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['products']) == Product.objects.count()


def test_product_detail(
        client,
        user_factory,
        category_factory,
        product_factory,
        review_factory
):
    category = category_factory(name='Sofas')
    product = product_factory(categories=(category,))
    # for 100% test coverage
    assert product.get_categories() == ['Sofas', ]
    for _ in range(3):
        review_factory(author=user_factory(), product=product)
    kwargs = {
        'category_slug': f'{category.slug}',
        'slug': f'{product.slug}'
    }
    url = reverse_lazy('catalog:detail', kwargs=kwargs)
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['reviews']) == Review.objects.count()
