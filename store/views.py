from django.shortcuts import render

# from store.models import Product


def store(request):
    # products = Product.objects.all()
    # context = {'products': products}
    context = {}
    return render(request, 'store/index.html', context)
