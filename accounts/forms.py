from allauth.account.forms import (
    SignupForm, LoginForm, ChangePasswordForm 
)
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

class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = False
        self.fields['password'].label = False

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'}))

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']:
            self.fields[key].label = False
        
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()      
        return user

class CustomChangePasswordForm(ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oldpassword'].label = False
        self.fields['password1'].label = False
        self.fields['password2'].label = False

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
            'avatar': forms.ClearableFileInput(
                    attrs={'class': 'form-control'}), 
        }

