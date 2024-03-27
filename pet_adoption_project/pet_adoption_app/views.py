from django.http import Http404
from django.shortcuts import render

from .database_creation import initialize_data
from .models import Pet


def home(request):
    pets = Pet.objects.all()
    # initialize_data()
    return render(request, 'home.html', {
        'pets': pets,
    })


def pets(request):
    all_pets = Pet.objects.all()
    # initialize_data()
    return render(request, 'pets.html', {
        'pets': all_pets,
    })


def pet_detail(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
    except Pet.DoesNotExist:
        raise Http404("Pet not found")
    return render(request, 'pet_detail.html', {'pet': pet})
