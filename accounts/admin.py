from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import UserProfile

CustomUser = get_user_model()

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]
    inlines = [UserProfileInline,]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)