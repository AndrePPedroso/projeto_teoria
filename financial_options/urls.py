from django.urls import path
from .api.views import *

urlpatterns = [
    path('black-scholes/', black_scholes_template, name='black_scholes'),
    path('black-scholes/api/', black_scholes_view, name='black_scholes_api'),
    path('black-scholes-merton/', black_scholes_merton_template, name='black_scholes_merton'),
    path('black-scholes-merton/api/', black_scholes_merton_view, name='black_scholes_merton_api'),
    path('cox-ross-rubinstein/', cox_ross_rubinstein_template, name='cox_ross_rubinstein'),
    path('api/cox-ross-rubinstein/', cox_ross_rubinstein_view, name='cox_ross_rubinstein_api'),
    path('precificar/', precificar_opcao_view, name='precificar_opcao'),
    path('financial_options/basic_concepts/overview/', basic_concepts_overview_view, name='basic_concepts_overview'),
    path('financial_options/basic_concepts/call_put_options/', call_put_options_view, name='call_put_options'),
    path('financial_options/basic_concepts/asset_put_combination/', asset_put_combination_view, name='asset_put_combination'),
    path('financial_options/basic_concepts/bull_bear_spread/', bull_bear_spread_view, name='bull_bear_spread'),

]
