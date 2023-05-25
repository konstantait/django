from django.urls import reverse_lazy

from catalog.models import Product


def test_favorites(client, faker, login_client, product_factory, category_factory): # noqa
    url = reverse_lazy('favorites:list')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse_lazy('profiles:login') + f'?next={url}' # noqa
    assert response.redirect_chain[0][1] == 302

    url = reverse_lazy('favorites:list')
    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200

    product = product_factory(categories=(category_factory(),))
    kwargs = {'product_id': f'{product.id}'}
    url = reverse_lazy('favorites:add', kwargs=kwargs)
    response = client.post(url, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse_lazy('favorites:list')
    assert response.redirect_chain[0][1] == 302
    assert len(response.context['products']) == Product.objects.filter(bookmarked_by=user).count() # noqa
    url = reverse_lazy('favorites:clear')
    response = client.post(url)
    assert response.status_code == 302
    assert response.context is None

    product = product_factory(categories=(category_factory(),))
    kwargs = {'product_id': f'{product.id}'}
    url = reverse_lazy('favorites:add', kwargs=kwargs)
    response = client.post(url, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse_lazy('favorites:list')
    assert response.redirect_chain[0][1] == 302
    assert len(response.context['products']) == Product.objects.filter(bookmarked_by=user).count() # noqa
    url = reverse_lazy('favorites:remove', kwargs=kwargs)
    response = client.post(url)
    assert response.status_code == 302
    assert response.context is None
