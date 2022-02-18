from allauth.account.forms import SignupForm

from django import forms
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
        fields = ('email', 'username',)


class CustomSignupForm(SignupForm):

    def save(self, request):
        user = super().save(request)
        user.save()
        UserProfile.objects.create(
            user=user,
        )        
        return user

class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = UserProfile
        fields = ['age', 'avatar']

