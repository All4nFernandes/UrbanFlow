from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Case(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "received", "Recebido"
        IN_PROGRESS = "in_progress", "Em andamento"
        RESOLVED = "resolved", "Resolvido"

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="cases",
    )
    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(max_length=60)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.RECEIVED,
    )
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title