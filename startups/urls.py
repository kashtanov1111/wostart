from django.urls import path

from . import views

app_name = 'startups'
urlpatterns = [
    path('', views.StartupListView.as_view(), name='startup_list'),
]
