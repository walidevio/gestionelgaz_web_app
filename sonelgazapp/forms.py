from django import forms
from .models import *


class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = ['type','texte', 'address']

    def __init__(self, user, *args, **kwargs):
        super(ReclamationForm, self).__init__(*args, **kwargs)
        self.fields['address'].queryset = Adresse.objects.filter(raccordement__iduser=user)


class ReleveForm(forms.ModelForm):
    class Meta:
        model = Index
        fields = ['matricule', 'releve']
        widgets = {'matricule' : forms.TextInput}

class RaccordementForm(forms.ModelForm):
    class Meta:
        model = Raccordement
        fields = ['type']



