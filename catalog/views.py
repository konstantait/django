from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from .models import Review
from .forms import ReviewForm


def home(request):
    template_name = 'catalog/index.html'
    context = {}
    return render(request, template_name, context=context)


@login_required(login_url='login')
def reviews(request):
    template_name = 'catalog/reviews.html'
    user = request.user
    form = ReviewForm(user=user)
    if request.method == 'POST':
        form = ReviewForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
    context = {
        'form': form,
        'reviews': Review.objects.all()
    }
    return render(request, template_name, context=context)


class ReviewView(FormView):
    form_class = ReviewForm
    template_name = 'catalog/reviews.html'

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

# class SignupView(TemplateView):
#     template_name = 'accounts/signup.html'
#     form = SignupForm()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({'form': self.form})
#         return context
#
#     def post(self, request, *args, **kwargs):
#         self.form = SignupForm(request.POST)
#         if self.form.is_valid():
#             self.form.save()
#             auth_logout(request)
#             return redirect('login')
#         return self.get(request, *args, **kwargs)