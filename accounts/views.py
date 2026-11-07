from django.shortcuts import render, redirect
from .forms import CitizenRegistrationForm


def cadastro(request):
    if request.method == "POST":
        form = CitizenRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CitizenRegistrationForm()

    return render(
        request,
        "accounts/cadastro.html",
        {"form": form}
    )