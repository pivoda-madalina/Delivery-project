from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from .views import LoginCustomView, ChangePassword, SignUp, EditProfile


urlpatterns = [
    path('login/', LoginCustomView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('password/', ChangePassword.as_view(), name='change_password'),
    path('reset_password/', PasswordResetView.as_view(template_name='accounts/password_reset_form.html'),
         name='reset_password'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset/complete/',
         PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('edit_profile/', EditProfile.as_view(), name='edit_profile'),
]
