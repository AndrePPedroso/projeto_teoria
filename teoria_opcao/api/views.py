from django.shortcuts import render


def volatilidade_template(request):
    return render(request, "site/teoria/volatilidade.html")


def log_cf_volatility(request):
    """
    Deterministic volatility estimation approach using Logarithm Cash Flow Return.
    This is primarily used as a reference approach.
    """
    context = {
        "title": "Logarithm Cash Flow Return (LOG CF)",
        "description": "A deterministic approach used as a reference for volatility estimation in real options.",
    }
    return render(request, "site/teoria/volatility/log_cf.html", context)


def copeland_antikarov_volatility(request):
    """
    Stochastic approach for volatility estimation using Copeland & Antikarov method.
    This method treats PV₀ as constant during simulation while CF₁ and PV₁ are stochastic.
    """
    return render(request, "site/teoria/copeland-antikarov-template.html")


def herath_park_volatility(request):
    return render(request, "site/teoria/herath_park.html")


def brandao_dyer_hahn_volatility(request):
    """
    Stochastic approach for volatility estimation using Brandão, Dyer & Hahn method.
    This method uses conditional probability where CF₂, CF₃, etc. are dependent on CF₁.
    """
    context = {
        "title": "Brandão, Dyer & Hahn Approach",
        "description": "Method where PV₀ and PV₁ are deterministic while CF₁ is stochastic, using conditional probability.",
    }
    return render(request, "site/teoria/volatility/brandao_dyer_hahn.html", context)


def markowitz_mean_variance_volatility(request):
    """
    Stochastic approach for volatility estimation using Markowitz Mean-Variance method.
    This method calculates volatility as the coefficient of variation of NPV.
    """
    context = {
        "title": "Markowitz Mean-Variance Method",
        "description": "Method that calculates volatility as the coefficient of variation (σ/μ) of NPV.",
        "formula": "σₑ₋ᵥ(NPV) = σNPV/μNPV",
    }
    return render(
        request, "site/teoria/volatility/markowitz_mean_variance.html", context
    )


def lewis_irr_volatility(request):
    """
    Stochastic approach for volatility estimation using Lewis et al. method.
    This method calculates volatility as the coefficient of variation of IRR.
    """
    context = {
        "title": "Lewis et al. IRR Approach",
        "description": "Method that calculates volatility as the coefficient of variation (σ/μ) of IRR.",
        "formula": "σₑ₋ᵥ(IRR) = σIRR/μIRR",
    }
    return render(request, "site/teoria/volatility/lewis_irr.html", context)


def var_based_volatility(request):
    """
    New stochastic approach proposed by the authors for volatility estimation.
    This method is based on Value at Risk (VaR) at 5% level.
    """
    context = {
        "title": "Value at Risk (VaR) Approach",
        "description": "A new method based on management assumption using the Value at Risk (VaR).",
        "formula": "σ = (μNPV - VaR(5%))/(1.6449 × μNPV)",
    }
    return render(request, "site/teoria/volatility/var_based.html", context)


def volatility_comparison(request):
    """
    Comprehensive view for comparing all volatility estimation methods.
    """
    context = {
        "title": "Volatility Methods Comparison",
        "description": "Compare results from different volatility estimation methods for the same investment project.",
    }
    return render(request, "site/teoria/volatility/comparison.html", context)
