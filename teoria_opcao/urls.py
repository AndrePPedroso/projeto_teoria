from django.urls import path
from .api.views import *

urlpatterns = [
    path('volatilidade-template', volatilidade_template, name='volatilidade_template'),
]
