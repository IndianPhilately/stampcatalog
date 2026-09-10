from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),   # temporary homepage
    path('<int:year>/', views.year_detail, name='year_detail'),
    path('stamp/<int:pk>/', views.stamp_detail, name='stamp_detail'),
]
