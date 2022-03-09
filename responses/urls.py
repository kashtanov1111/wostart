from django.urls import path

from . import views

app_name = 'responses'
urlpatterns = [
    path('', 
        views.ResponseListView.as_view(), name='response_list'),
]
