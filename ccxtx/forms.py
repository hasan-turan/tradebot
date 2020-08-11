from django import forms
from .models import Ccxtx


class CcxtxForm(forms.ModelForm):
    class Meta:
        model = Ccxtx
        fields = ['exchanges'] 