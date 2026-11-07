from django import forms

from .models import Case


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ("title", "category", "description", "latitude", "longitude")
        labels = {
            "title": "Título do chamado",
            "category": "Categoria",
            "description": "Descreva o problema",
            "latitude": "Latitude",
            "longitude": "Longitude",
        }
        help_texts = {
            "category": "Ex.: iluminação pública, buraco, limpeza urbana.",
            "latitude": "Clique no mapa para preencher as coordenadas.",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "field", "placeholder": "Ex.: Poste sem iluminação"}),
            "category": forms.TextInput(attrs={"class": "field", "placeholder": "Ex.: Iluminação pública"}),
            "description": forms.Textarea(attrs={"class": "field", "rows": 4, "placeholder": "Conte o que aconteceu e algum detalhe útil."}),
            "latitude": forms.NumberInput(attrs={"class": "field", "step": "0.000001", "id": "id_latitude"}),
            "longitude": forms.NumberInput(attrs={"class": "field", "step": "0.000001", "id": "id_longitude"}),
        }
