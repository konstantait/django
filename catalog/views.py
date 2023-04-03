from django.shortcuts import render

# from .models import Product


def catalog(request):
    # products = Product.objects.all()
    # context = {'products': products}
    context = {}
    return render(request, 'catalog/index.html', context)
