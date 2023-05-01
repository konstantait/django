from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from orders.tasks import order_created

from django.views.generic.edit import UpdateView

from cart.cart import Cart
from orders.models import Order


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'])
            order.save()
            cart.clear()
            task = order_created.delay(order.id) # noqa
            return redirect('orders:payment', pk=order.id)

    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/create.html',
                  {'cart': cart, 'form': form})


class PaymentView(UpdateView):
    model = Order
    fields = ["is_paid"]
    template_name = 'orders/payment.html'
    success_url = "/"
