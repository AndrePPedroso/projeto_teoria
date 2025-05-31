from django.urls import path
from .api.views import *

urlpatterns = [
    path('finantial-basic-concepts/', finantial_options_basic_concepts, name='financial_options_basic_concepts'),    
    path('black-scholes/', black_scholes_template, name='black_scholes'),
    path('black-scholes/api/', black_scholes_view, name='black_scholes_api'),
    path('black-scholes-merton/', black_scholes_merton_template, name='black_scholes_merton'),
    path('black-scholes-merton/api/', black_scholes_merton_view, name='black_scholes_merton_api'),
    path('cox-ross-rubinstein/', cox_ross_rubinstein_template, name='cox_ross_rubinstein'),
    path('api/cox-ross-rubinstein/', cox_ross_rubinstein_view, name='cox_ross_rubinstein_api'),
    path('precificar/', precificar_opcao_view, name='precificar_opcao'),
]
