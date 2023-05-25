from django.urls import reverse_lazy

from catalog.models import Product


def test_orders(login_client, product_factory, category_factory, coupon_factory): # noqa

    client, user = login_client()
    url = reverse_lazy('orders:order_create')
    response = client.get(url)
    assert response.status_code == 200
    product = product_factory(categories=(category_factory(),))
    kwargs = {'product_id': f'{product.id}'}
    url = reverse_lazy('cart:add', kwargs=kwargs)
    data = {'quantity': 1}

    response = client.post(url, data=data, follow=True)
    session = client.session
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse_lazy('cart:detail')
    assert response.redirect_chain[0][1] == 302
    assert len(session['cart']) == Product.objects.count()

    coupon = coupon_factory()
    url = reverse_lazy('orders:order_create')
    data = {
        'name': user.first_name,
        'email': user.email,
        'phone': user.phone,
        'coupon': coupon.code
    }
    response = client.post(url, data=data)
    assert response.status_code == 302
