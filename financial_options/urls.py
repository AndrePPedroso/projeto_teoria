from django.urls import path
from .api.views import *

urlpatterns = [
    path('save-financial-model/', save_black_schole_model_view, name='save_financial_model'),
    path('black-scholes/api/', black_scholes_view, name='black_scholes_api'),
    path('black-scholes-merton/', black_scholes_merton_template, name='black_scholes_merton'),
    path('black-scholes-merton/api/', black_scholes_merton_view, name='black_scholes_merton_api'),
    path('cox-ross-rubinstein/', cox_ross_rubinstein_template, name='cox_ross_rubinstein'),
    path('api/cox-ross-rubinstein/', cox_ross_rubinstein_view, name='cox_ross_rubinstein_api'),
    path('precificar/', precificar_opcao_view, name='precificar_opcao'),
    path('precificar-americana/', precificar_opcao_americana_view, name='precificar_opcao_americana'),
    path('financial_options/basic_concepts/overview/', basic_concepts_overview_view, name='basic_concepts_overview'),
    path('financial_options/black_scholes/overview/', black_scholes_overview_view, name='black_scholes_overview'),
    path('financial_options/cox_ross/overview/', cox_ross_overview_view, name='cox_ross_overview'),
    path('financial_options/monte_carlo/overview/', monte_carlo_overview_view, name='monte_carlo_overview'),

    path('financial_options/basic_concepts/call_put_options/', call_put_options_view, name='call_put_options'),
    path('financial_options/basic_concepts/asset_put_combination/', asset_put_combination_view, name='asset_put_combination'),
    path('financial_options/basic_concepts/bull_bear_spread/', bull_bear_spread_view, name='bull_bear_spread'),
    path('financial_options/basic_concepts/collar_strategy_simulator/', collar_strategy_simulator_view, name='collar_strategy_simulator'),

]
