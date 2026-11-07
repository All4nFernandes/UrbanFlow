import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

class CitizenRegistrationForm(UserCreationForm):
    cpf = forms.CharField(
        label="CPF",
        max_length=14,
        widget=forms.TextInput(attrs={"placeholder": "000.000.000-00", "autocomplete": "off"}),
    )

    def clean_cpf(self):
        cpf = re.sub(r"\D", "", self.cleaned_data["cpf"])
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            raise forms.ValidationError("Informe um CPF válido com 11 dígitos.")

        first_sum = sum(int(cpf[index]) * (10 - index) for index in range(9))
        first_digit = (first_sum * 10) % 11
        first_digit = 0 if first_digit == 10 else first_digit

        second_sum = sum(int(cpf[index]) * (11 - index) for index in range(10))
        second_digit = (second_sum * 10) % 11
        second_digit = 0 if second_digit == 10 else second_digit

        if int(cpf[9]) != first_digit or int(cpf[10]) != second_digit:
            raise forms.ValidationError("CPF inválido.")
        if User.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return cpf

    def save(self, commit=True):
        user = super().save(commit=False)
        user.cpf = self.cleaned_data["cpf"]
        user.role = User.Role.REQUESTER
        user.username = self.cleaned_data["cpf"]
        user.is_active = True
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ("first_name", "last_name", "cpf", "email")
        labels = {
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "email": "E-mail",
        }

class CPFLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="CPF ou usuário",
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "CPF (com ou sem pontuação) ou usuário",
            "autocomplete": "username",
        }),
    )


