from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView
from .forms import SignUpForm, EditProfileForm


class LoginCustomView(LoginView):
    template_name = 'accounts/login.html'


class ChangePassword(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = '/store/'


class SignUp(CreateView):
    template_name = 'form.html'
    success_url = '/store/'
    form_class = SignUpForm


class EditProfile(UpdateView):
    template_name = 'accounts/edit_profile.html'
    success_url = '/store/'
    form_class = EditProfileForm

    def get_object(self, queryset=None):
        return self.request.user
