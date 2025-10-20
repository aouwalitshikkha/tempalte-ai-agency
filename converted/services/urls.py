from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:slug>/', views.service_detail, name='service_detail'),
    path("<slug:service_slug>/<slug:subservice_slug>/", views.subservice_detail, name="subservice_detail"),



]
