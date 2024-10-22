from django import forms
from .models import user_profile

class profile_form(forms.ModelForm):
    class Meta:
        model = user_profile
        fields = ["image", "school", "year", "major1", "major2"]
        #widgets = {
        ##    'school': forms.Select(attrs={'class': 'form-control'}),
         #   'year': forms.Select(attrs={'class': 'form-control'}),
        #    'major1': forms.Select(attrs={'class': 'form-control'}),
        #    'major2': forms.Select(attrs={'class': 'form-control'})
        #}


