from django.http import Http404
from django.shortcuts import render

from .database_creation import initialize_data, initialize_questions
from .models import Pet, Questions


def home(request):
    # initialize_data()
    # initialize_questions()
    return render(request, 'home.html', {})


def pets(request):
    all_pets = Pet.objects.all()
    return render(request, 'pets.html', {
        'pets': all_pets,
    })


def quiz(request):
    question_objs = Questions.objects.all()
    return render(request, 'quiz_main_page.html', {
        'questions': question_objs,
        })


def pet_detail(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
    except Pet.DoesNotExist:
        raise Http404("Pet not found")
    return render(request, 'pet_detail.html', {'pet': pet})
