from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView
from .forms import SignUpForm


class LoginCustomView(LoginView):
    template_name = 'accounts/login.html'


class ChangePassword(PasswordChangeView):
    template_name = 'accounts/login.html'
    success_url = '/store/'


class SignUp(CreateView):
    template_name = 'form.html'
    success_url = '/store/'
    form_class = SignUpForm
