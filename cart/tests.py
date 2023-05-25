from django.urls import reverse_lazy

from catalog.models import Product


def test_cart(client, faker, product_factory, category_factory):
    url = reverse_lazy('cart:detail')
    response = client.get(url)
    assert response.status_code == 200

    product = product_factory(categories=(category_factory(), ))
    kwargs = {'product_id': f'{product.id}'}
    url = reverse_lazy('cart:add', kwargs=kwargs)
    data = {'quantity': 1}
    response = client.post(url, data=data, follow=True)
    session = client.session
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse_lazy('cart:detail')
    assert response.redirect_chain[0][1] == 302
    assert len(session['cart']) == Product.objects.count()

    url = reverse_lazy('cart:clear')
    response = client.post(url, follow=True)
    session = client.session
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse_lazy('cart:detail')
    assert response.redirect_chain[0][1] == 302
    assert len(session['cart']) == 0

    product = product_factory(categories=(category_factory(),))
    kwargs = {'product_id': f'{product.id}'}
    url = reverse_lazy('cart:add', kwargs=kwargs)
    data = {'quantity': 1, 'override': True}
    response = client.post(url, data=data)
    assert response.status_code == 302
    url = reverse_lazy('cart:remove', kwargs=kwargs)
    response = client.post(url, data=data)
    session = client.session
    assert response.status_code == 302
    assert len(session['cart']) == 0
