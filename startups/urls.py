from django.urls import path

from . import views

app_name = 'startups'
urlpatterns = [
    path('', views.StartupListView.as_view(), name='startup_list'),
    path('my/', 
        views.UserStartupsListView.as_view(), name='user_startups'),
    path('<slug:slug>/', 
        views.StartupDetailView.as_view(), name='startup_detail'),
    path('<slug:slug>/delete/', 
        views.StartupDeleteView.as_view(), name='startup_delete')
]
