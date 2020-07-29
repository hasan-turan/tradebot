from django import forms
from .models import Exchange


class ExchangeForm(forms.ModelForm):
    class Meta:
        model = Exchange
        fields = ['title', 'url', 'api_key', 'secret_key']
