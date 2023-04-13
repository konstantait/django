from django.views.generic import TemplateView, RedirectView

from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from .forms import LoginForm, SignupForm


class LoginView(TemplateView):
    template_name = 'accounts/login.html'
    form = LoginForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form': self.form})
        return context

    def post(self, request, *args, **kwargs):
        self.form = LoginForm(request, request.POST)
        if self.form.is_valid():
            auth_login(request, self.form.get_user())
            next_page = request.POST.get('next', None)
            if next_page is None and not url_has_allowed_host_and_scheme(
                    url=next_page,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure()):
                return redirect('home')
            else:
                return redirect(next_page)
        return self.get(request, *args, ** kwargs)


class SignupView(TemplateView):
    template_name = 'accounts/signup.html'
    form = SignupForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form': self.form})
        return context

    def post(self, request, *args, **kwargs):
        self.form = SignupForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            auth_logout(request)
            return redirect('login')
        return self.get(request, *args, **kwargs)


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super().get(request, *args, **kwargs)

# from django.shortcuts import render, redirect
# from django.utils.http import url_has_allowed_host_and_scheme
# from django.contrib.auth import login as auth_login
# from django.contrib.auth import logout as auth_logout
#
# from .forms import LoginForm, SignupForm
#
#
# def login(request):
#     template_name = 'accounts/login.html'
#     form = LoginForm()
#     if request.method == 'POST':
#         form = LoginForm(request, request.POST)
#         if form.is_valid():
#             auth_login(request, form.get_user())
#             next_page = request.POST.get('next', None)
#             if next_page is None and not url_has_allowed_host_and_scheme(
#                     url=next_page,
#                     allowed_hosts={request.get_host()},
#                     require_https=request.is_secure()):
#                 return redirect('home')
#             else:
#                 return redirect(next_page)
#     context = {'form': form, }
#     return render(request, template_name, context=context)
#
#
# def signup(request):
#     template_name = 'accounts/signup.html'
#     user = request.user
#     form = SignupForm(user=user)
#     if request.method == "POST":
#         form = SignupForm(user=user, data=request.POST)
#         if form.is_valid():
#             form.save()
#             auth_logout(request)
#             return redirect('login')
#     context = {'form': form, }
#     return render(request, template_name, context=context)
#
#
# def logout(request):
#     auth_logout(request)
#     return redirect('home')
