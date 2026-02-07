from django.contrib import admin
from django.urls import path
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/journey', views.journey_config, name='journey_config'),
    path('', views.home, name='home'),
]
