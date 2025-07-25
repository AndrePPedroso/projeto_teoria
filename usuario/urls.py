from django.urls import path
from .api.views import *

urlpatterns = [
    path("accounts/signup/", singup_view, name="account_signup"),
    path("accounts/login/", login_template, name="account_login"),
    path("sign_up/", sing_up_template, name="sing-up-template"),
    path('accounts/verify-email/<str:uidb64>/<str:token>/', verify_email_view, name='account_verification_sent'),
    path("update_profile/", update_profile_view, name="update_profile_view"),
]
