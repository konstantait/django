from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Review
from .forms import ReviewModelForm


def home(request):
    template_name = 'catalog/index.html'
    context = {}
    return render(request, template_name, context=context)


@login_required(login_url='login')
def reviews(request):
    template_name = 'catalog/reviews.html'
    user = request.user
    form = ReviewModelForm(user=user)
    if request.method == 'POST':
        form = ReviewModelForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
    context = {
        'form': form,
        'reviews': Review.objects.all()
    }
    return render(request, template_name, context=context)
