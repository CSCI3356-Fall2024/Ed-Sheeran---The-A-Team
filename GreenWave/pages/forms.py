from django import forms
from .models import user_profile
from .models import campaign
from .models import service
from .models import Place
from .models import reward
from django.utils import timezone

class profile_form(forms.ModelForm):
    YEAR_CHOICES = [('', 'Please choose a year'), (2025, '2025'),(2026, '2026'),(2027, '2027'),(2028, '2028')]
    year = forms.ChoiceField(choices=YEAR_CHOICES)
    SCHOOL_CHOICES = [('', 'Please choose a school'), ('MCAS', 'MCAS'), ('CSOM', 'CSOM'), ('CSON', 'CSON'), ('LSEHD', 'LSEHD'), ('Messina', 'Messina')]
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

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'MM/DD/YYYY'})
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'MM/DD/YYYY'})
    )
    PLACE_CHOICES = [('1', 'Lower Live'), ('2', 'Stuart Dining Hall'), ('3', 'Carney Dining Hall'), ('4', 'Eagles Nest'), ('5', 'Hillside Cafe'), ('6', 'The Rat')]
    places = forms.ModelMultipleChoiceField(queryset=Place.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = campaign
        fields = ["name", "start_date", "end_date", "points", "validation", "description", "places"]

class service_form(forms.ModelForm):
    class Meta:
        model = service
        fields = ["name", "desc", "how_to_use", "why_to_use", "points_per_use"]

class reward_form(forms.ModelForm):
    class Meta:
        model = reward
        fields = ["name", "desc", "cost"]

class points_form(forms.Form):
    today = timezone.now().date()
    campaign_choice = forms.ModelChoiceField(
        queryset=campaign.objects.filter(start_date__lt=today, end_date__gt=today), 
        label='Campaign',
        empty_label='Select a Campaign',
        widget=forms.Select(attrs={'class': 'campaign'})
    )
        