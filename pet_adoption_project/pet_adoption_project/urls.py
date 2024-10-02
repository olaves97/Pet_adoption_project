"""
URL configuration for pet_adoption_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from pet_adoption_app import views
from pet_adoption_app.views import PetDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('pets/', views.pets, name='pets'),
    path('quiz/', views.quiz, name='quiz_main_page'),
    path('pets/<int:pet_id>', views.pet_detail, name='pet_detail'),
    path('quiz/results/', views.submit_form, name='quiz_results'),
    path('', include('django.contrib.auth.urls')),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('moderator/', views.moderator_dashboard, name='moderator_dashboard'),
    path('create/', views.create_a_record, name='create'),
    path('pet/edit/<int:pet_id>', views.edit, name='edit'),
    path('pet/delete/<int:pk>', PetDeleteView.as_view(), name='pet_delete'),
]
