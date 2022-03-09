from django.urls import path

from . import views

app_name = 'ads'
urlpatterns = [
    path('', views.AdListView.as_view(), name='ad_list'),
    path('my/', 
        views.UserAdsListView.as_view(), name='user_ads'),
    path('add/', 
        views.AdCreateView.as_view(), name='ad_create'),
    path('iresponded/', 
        views.AdsIRespondedListView.as_view(), name='ads_i_responded'),
    path('<slug:slug>/', 
        views.AdDetailView.as_view(), name='ad_detail'),
    path('<slug:slug>/edit/', 
        views.AdUpdateView.as_view(), name='ad_update'),
    path('<slug:slug>/delete/', 
        views.AdDeleteView.as_view(), name='ad_delete'),
]
