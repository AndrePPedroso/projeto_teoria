from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from estocasticos.use_cases.mbg_ito_use_case import GeneralizedBrownianMotionUseCase
from estocasticos.use_cases.modelo_reversao_media_use_case import ReversaoMediaUseCase
from estocasticos.use_cases.monte_carlos_use_case import MonteCarloUseCase
from estocasticos.use_cases.random_walk_normal_use_case import RandomWalkNormalUseCase
from estocasticos.use_cases.cadeia_markov_use_case import CadeiaMarkovUseCase
from estocasticos.use_cases.random_walk_use_case import RandomWalkUseCase


def pagina_inicial(request):
    return render(request, "admin/login.html")


def custom_admin_login(request):
    error_message = None
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.is_superuser:
                return redirect("/admin/")
            else:
                return redirect("/home")
        else:
            error_message = "Incorrect username or password."

    else:
        form = AuthenticationForm()

    return render(
        request, "admin/login.html", {"form": form, "error_message": error_message}
    )


@login_required(login_url='/admin/login/')
def home_view(request):
    return render(request, "site/home/home.html")


@csrf_exempt
def set_language(request):
    if request.method == "POST":
        language = request.POST.get("language")
        if language in ["en", "pt"]:
            request.session["language"] = language
            return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)
