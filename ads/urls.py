from django.urls import path

from . import views

app_name = 'ads'
urlpatterns = [
    path('', views.AdListView.as_view(), name='ad_list'),
    path('<slug:slug>/', views.AdDetailView.as_view(), name='ad_detail'),
]
