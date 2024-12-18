from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView
from allauth.account.views import PasswordResetFromKeyView


def sing_up_template(request):
    return render(request, "site/usuario/cadastro.html")


def singup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if not password1 or not password2:
            messages.error(request, "choose a valid password.")
            return render(
                request,
                "site/usuario/cadastro.html",
                {"error_message": "Choose a valid password."},
            )

        if password1 != password2:
            messages.error(request, "The passwords don't match.")
            return render(
                request,
                "site/usuario/cadastro.html",
                {"error_message": "The passwords don't match."},
            )

        try:
            user = User.objects.create_user(
                username=username, email=email, password=password1
            )
            login(request, user)
            return redirect("/home")
        except Exception as e:
            return render(
                request, "site/usuario/cadastro.html", {"error_message": str(e)}
            )

    return render(request, "site/usuario/cadastro.html")
