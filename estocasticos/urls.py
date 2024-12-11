from django.urls import path
from .api.views import *

urlpatterns = [
    path("processos-home", processos_home, name="processos_home"),
    path(
        "teoria-opcoes-financeiras",
        teoria_opcoes_financeiras,
        name="teoria_opcoes_financeiras",
    ),
    path("teoria-opcoes-reais", teoria_opcoes_reais, name="teoria_opcoes_reais"),
    path("cadeia-markov", cadeia_markov, name="cadeia_markov"),
    path("random-walk-normal", random_walk_normal, name="random_walk_normal"),
    path("random-walk_template", random_walk_template, name="random_walk_template"),
    path("monte-carlos", monte_carlos, name="monte_carlos"),
    path("mbg-ito", mbg_ito, name="mbg_ito"),
    path("mbg-teoria", mbg_teoria, name="mbg_teoria"),
    path("modelo-reversao-media", modelo_reversao_media, name="modelo_reversao_media"),
    # #------calculos----------
    path("markov_simulador/", markov_simulator, name="simulate_markov"),
    path(
        "random_walk_normal_simulador/",
        random_walk_normal_view,
        name="simulate_random_walk_normal",
    ),
    path("random_walk_simulador/", random_walk_view, name="simulate_random_walk"),
    path("monte_carlos_simulator/", monte_carlo_view, name="monte_carlos_simulator"),
    path("mbg_simulator/", simulate_gbm_view, name="mbg_simulator"),
    path(
        "simulate-mean-reversion/",
        simulate_mean_reversion_view,
        name="simulate_mean_reversion",
    ),
]
