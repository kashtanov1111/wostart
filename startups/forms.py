import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import Startup, StartupImage

class TitleCleanMixin:

    def clean_title(self):
        new_title = self.cleaned_data['title'].lower()
        if new_title == 'my' or new_title == 'add':
            raise ValidationError(
                'Title may not be "my"'
            )
        return new_title

class FoundedCleanMixin:

    def clean_founded(self):
        new_founded = self.cleaned_data['founded']
        if new_founded > datetime.date.today():
            raise ValidationError(
                'The date cannot be in the future!'
            )
        return new_founded

class WebsiteCleanMixin:

    def clean_web_site(self):
        new_website = self.cleaned_data['web_site']
        if new_website is not None:
            if '://' not in new_website:
                new_website = 'http://' + new_website
        return new_website

class StartupForm(
    TitleCleanMixin, FoundedCleanMixin, 
    WebsiteCleanMixin, forms.ModelForm):

    class Meta:
        model = Startup
        fields = ('title', 'description', 'founded', 'web_site')
        widgets = {
            'founded': forms.DateInput(attrs={'type': 'date'}),
        }

class StartupCreateForm(StartupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['images'].label = 'Images (5 max.)'

    images = forms.FileField(required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True, 'class': 'form-control'}))

    class Meta(StartupForm.Meta):
        fields = StartupForm.Meta.fields + ('images',)