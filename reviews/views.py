from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache

from core.enums import CacheKeys
from reviews.forms import ReviewForm
from reviews.models import Review


class ReviewCreate(LoginRequiredMixin, CreateView):
    form_class = ReviewForm
    template_name = 'reviews/create.html'
    success_url = reverse_lazy('reviews:list')
    login_url = reverse_lazy('profiles:login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ReviewList(ListView):
    model = Review
    template_name = 'reviews/list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        queryset = cache.get(CacheKeys.REVIEWS_ALL)
        if not queryset:
            print('caching')
            queryset = Review.objects.all()
            cache.set(CacheKeys.REVIEWS_ALL, queryset)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering, )
            queryset = queryset.order_by(ordering)
        return queryset
