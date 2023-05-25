from django.urls import reverse_lazy
from reviews.models import Review


def test_reviews_create(
        faker,
        login_client,
        category_factory,
        product_factory,
):
    client, user = login_client()
    client, user = login_client()
    url = reverse_lazy('reviews:list')
    response = client.get(url)
    assert response.status_code == 200

    url = reverse_lazy('reviews:create')
    response = client.get(url)
    assert response.status_code == 200

    category = category_factory(name='Sofas')
    product = product_factory(categories=(category,))
    data = {
        'author': user.id,
        'product': product.id,
        'rating': 0,
        'text': faker.word()
    }
    response = client.post(url, data=data)
    assert response.status_code == 302
    assert Review.objects.count() == 1
