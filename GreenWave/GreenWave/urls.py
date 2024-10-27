"""
URL configuration for GreenWave project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LogoutView

from pages.views import home_view
from pages.views import profile_view, rewards
from pages.views import product_detail_view, service_list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name= 'home'),
    path('accounts/', include('allauth.urls')),
    path("accounts/profile/", profile_view, name="profile"),
    path("services/", product_detail_view, name="service"),
    path("service/", service_list_view, name="service_list"),
    path("", LogoutView.as_view(), name="logout"), #do we want a logout page or what? Change where it redirect here and in settings.py "LOGOUT_REDIRECT_URL"
    path("rewards/", rewards, name="rewards"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


