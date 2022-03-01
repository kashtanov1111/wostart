from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    path('<str:username>/',
        views.UserDetailView.as_view(), name='user_profile'),
]
