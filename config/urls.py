"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views
from accounts.views import (
    UpdateUserProfileView, CustomPasswordChangeView)

urlpatterns = [
    path('admin-2281953/', admin.site.urls),
    path('accounts/password/change/',
        CustomPasswordChangeView.as_view(),
        name='account_change_password'),
    path('accounts/', include('allauth.urls')),
    path('users/', include('accounts.urls')),
    path('startups/', include('startups.urls')),
    path('ads/', include('ads.urls')),
    path('profile/edit/', UpdateUserProfileView.as_view(), 
            name='update_profile'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('', views.HomePageView.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns