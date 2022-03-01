from allauth.account.forms import SignupForm

from django import forms
from django.forms import Textarea
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name')


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'}))

    email = forms.CharField(
        max_length=100, required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Last name',
                                    'class': 'form-control'}))
    
        
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        UserProfile.objects.create(
            user=user,
        )        
        return user

class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['about'].label = 'About Me'
        self.fields['instagram'].label = 'Instagram username'
        self.fields['twitter'].label = 'Twitter username'

    class Meta:
        model = UserProfile
        fields = [
            'about', 'instagram', 'twitter', 'mobile_phone','avatar',
            ]
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}), 
        }