from django.urls import reverse_lazy
from django.views.generic import FormView

from django.contrib.auth.decorators import login_required, user_passes_test  # noqa
from django.utils.decorators import method_decorator

from reviews.forms import ReviewForm


class ReviewFormView(FormView):
    template_name = 'reviews/form.html'
    form_class = ReviewForm

    @method_decorator(login_required(login_url=reverse_lazy('profiles:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
