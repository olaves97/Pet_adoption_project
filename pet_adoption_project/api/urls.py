from django.urls import path
from . import views

urlpatterns = [
    path('pets_data/', views.getData),
]