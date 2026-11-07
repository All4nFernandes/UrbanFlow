from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from accounts.forms import CPFLoginForm

from cases.views import home

urlpatterns = [
    path("", home, name="home"),
    path("login/", LoginView.as_view(template_name="registration/login.html", authentication_form=CPFLoginForm, redirect_authenticated_user=True), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("accounts/", include("accounts.urls")),
    path("chamados/", include("cases.urls")),
    path("admin/", admin.site.urls),
]
