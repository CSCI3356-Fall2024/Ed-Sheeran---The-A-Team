from django import forms
from .models import user_profile
from .models import campaign
from .models import service

class profile_form(forms.ModelForm):
    YEAR_CHOICES = [(2025, '2025'),(2026, '2026'),(2027, '2027'),(2028, '2028')]
    year = forms.ChoiceField(choices=YEAR_CHOICES)
    SCHOOL_CHOICES = [('Boston College', 'Boston College')]
    school = forms.ChoiceField(choices = SCHOOL_CHOICES)

    class Meta:
        model = user_profile
        fields = ["image", "school", "year", "major1", "major2"]
        #widgets = {
        ##    'school': forms.Select(attrs={'class': 'form-control'}),
         #   'year': forms.Select(attrs={'class': 'form-control'}),
        #    'major1': forms.Select(attrs={'class': 'form-control'}),
        #    'major2': forms.Select(attrs={'class': 'form-control'})
        #}
class campaign_form(forms.ModelForm):
    VALIDATION_CHOICES = [('Choice 1', 'Choice 1'), ('Choice 2', 'Choice 2')]
    validation = forms.ChoiceField(choices = VALIDATION_CHOICES)
    class Meta:
        model = campaign
        fields = ["name", "start_date", "end_date", "points", "validation", "description"]

class service_form(forms.ModelForm):
    class Meta:
        model = service
        fields = ["name", "desc", "how_to_use", "why_to_use", "points_per_use"]