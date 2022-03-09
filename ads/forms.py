from decimal import Decimal as D

from django import forms
from django.core.exceptions import ValidationError

from .models import Ad
from startups.models import Startup
from startups.forms import TitleCleanMixin

class AdForm(TitleCleanMixin, forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['startup'].queryset = (
                Startup.objects.filter(founder=user))
        self.fields['startup'].empty_label = 'Select'
        self.fields['share'].label = 'Share(%)'
        
    class Meta:
        model = Ad
        fields = (
            'title', 'position', 'description', 'share', 'startup')
        widgets = {
            'position': forms.Select(attrs={'class': 'form-select'}),
            'startup': forms.Select(attrs={'class': 'form-select'}),
        }
