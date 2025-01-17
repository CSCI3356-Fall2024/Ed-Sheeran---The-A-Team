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

from pages.views import logout_view
from pages.views import cancelled_view
from pages.views import home_view
from pages.views import campaign_view
from pages.views import add_score, leaderboard_view
from pages.views import profile_view, rewards, exchange, input, exchange_detail_view
from pages.views import service_detail_view, service_list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('social_django.urls', namespace='social')),
    # path('login/', TemplateView.as_view(template_name='login.html'), name = 'login'),
    # path('accounts/profile/',login_required(TemplateView.as_view(template_name='profile.html')), name = 'profile'),

    path('logout/', logout_view, name = 'logout'),
    path('', home_view, name= 'home'),
    path('accounts/3rdparty/login/cancelled/', cancelled_view, name='account_login_cancelled'),
    path('accounts/', include('allauth.urls')),
    path("accounts/profile/", profile_view, name="profile"),
    path("service/<int:id>//", service_detail_view, name="service_detail"),
    path("services/", service_list_view, name="service_list"),
    path("rewards/", rewards, name="rewards"),
    path("campaigns/", campaign_view, name="campaigns"),
    path("exchange/", exchange, name="exchange"),
    path("input/", input, name="input"),
    path('add-score/', add_score, name='add_score'),
    # path('leaderboard/', leaderboard, name='leaderboard'),
    path("exchange/<int:id>/", exchange_detail_view, name="exchange_detail"),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
