from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from catalog.models import Review
from catalog.forms import ReviewModelForm


def home(request):
    context = {}
    return render(request, 'catalog/index.html', context)


@login_required
def reviews(request):
    author = request.user
    form = ReviewModelForm(author=author)
    if request.method == 'POST':
        form = ReviewModelForm(author=author, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for review!')
            return redirect('home')
        else:
            messages.error(request, 'Check input')
    else:
        messages.info(request, f'Welcome {author}, leave your review')
    context = {
        'form': form,
        'reviews': Review.objects.all()
    }
    return render(request, 'catalog/reviews.html', context=context)
