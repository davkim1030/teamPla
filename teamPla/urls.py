"""teamPla URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from teamPla import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('register_team/', views.register_team, name='register_team'),
    path('pending_team/', views.pending_team, name='pending_team'),
    path('team_info/', views.team_info, name='team_info')
]
