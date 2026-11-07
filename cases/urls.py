from django.urls import path

from . import views

app_name = "cases"

urlpatterns = [
    path("", views.case_list, name="list"),
    path("novo/", views.case_create, name="create"),
    path("<int:pk>/editar/", views.case_update, name="update"),
    path("<int:pk>/excluir/", views.case_delete, name="delete"),
    path("<int:pk>/", views.case_detail, name="detail"),
]
