from django.urls import path
from .api.views import *

urlpatterns = [
    path("accounts/signup/", singup_view, name="account_signup"),
    path("sing_up_template/", sing_up_template, name="sing-up-template"),
]
