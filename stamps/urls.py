from django.urls import path
from . import views

urlpatterns = [
    path('', views.year_list, name='year_list'),          # main page
    path('<int:year>/', views.year_detail, name='year_detail'),  # stamps for a year
    path('stamp/<int:pk>/', views.stamp_detail, name='stamp_detail'),  # stamp detail
]
