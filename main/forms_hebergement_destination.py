from django import forms
from .models import Hebergement, Destination

class HebergementForm(forms.ModelForm):
    class Meta:
        model = Hebergement
        fields = '__all__'

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = '__all__' 