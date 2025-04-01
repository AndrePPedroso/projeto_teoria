from django.urls import path
from .api.views import *

urlpatterns = [
    path("volatilidade-template", volatilidade_template, name="volatilidade_template"),
    path("volatility/log-cf/", log_cf_volatility, name="log_cf_volatility"),
    path(
        "volatility/copeland-antikarov/",
        copeland_antikarov_volatility,
        name="copeland_antikarov_volatility",
    ),
    path(
        "volatility/herath-park/", herath_park_volatility, name="herath_park_volatility"
    ),
    path(
        "volatility/brandao-dyer-hahn/",
        brandao_dyer_hahn_volatility,
        name="brandao_dyer_hahn_volatility",
    ),
    path(
        "volatility/markowitz-mean-variance/",
        markowitz_mean_variance_volatility,
        name="markowitz_mean_variance_volatility",
    ),
    path("volatility/lewis-irr/", lewis_irr_volatility, name="lewis_irr_volatility"),
    path("volatility/var-based/", var_based_volatility, name="var_based_volatility"),
    path("volatility/comparison/", volatility_comparison, name="volatility_comparison"),
    path("volatility/binomial-model/", binomial_model_view, name="binomial_model"),
]
