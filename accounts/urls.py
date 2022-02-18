from django.urls import path

from . import views

app_name = 'profile'
urlpatterns = [
    path('edit/', views.UpdateUserProfileView.as_view(), 
            name='update_profile'),
]
