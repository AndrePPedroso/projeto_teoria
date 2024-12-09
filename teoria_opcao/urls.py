from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api.views import *

router = DefaultRouter()

urlpatterns = [
    path('volatilidade-template/', volatilidade_template, name='volatilidade_template'),
]
