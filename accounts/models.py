from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models


class UrbanFlowUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields["role"] = "superuser"
        return super().create_superuser(
            username,
            email,
            password,
            **extra_fields,
        )


class User(AbstractUser):
    class Role(models.TextChoices):
        REQUESTER = "requester", "Requerente"
        AUDITOR = "auditor", "Fiscal/Auditor"
        SUPERUSER = "superuser", "Superuser"

    cpf = models.CharField(
        max_length=11,
        unique=True,
        null=True,  # temporário até preencher CPFs dos usuários existentes
        blank=False,
        validators=[
            RegexValidator(r"^\d{11}$", "Informe os 11 dígitos do CPF, sem pontuação.")
        ],
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.REQUESTER,
    )
    REQUIRED_FIELDS = ["email", "cpf"]

    objects = UrbanFlowUserManager()
