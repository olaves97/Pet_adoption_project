from django.http import Http404
from django.shortcuts import render

from .models import Pet, Question
from .quiz_functions import QuizManager


PARAMETERS = ['size', 'age', 'sex', 'breed', 'temperament', 'personality', 'kid_friendly', 'dog_friendly',
              'cat_friendly', 'neutered']


def home(request):
    return render(request, 'home.html', {})


def pets(request):
    all_pets = Pet.objects.all()
    return render(request, 'pets.html', {
        'pets': all_pets,
    })


def quiz(request):
    question_objs = Question.objects.all()
    return render(request, 'quiz_main_page.html', {
        'questions': question_objs,
    })


class TooFewAnswers(Exception):
    pass


def submit_form(request):
    responses = QuizManager().prepare_a_list_of_responses(request)

    try:
        if len(responses) == len(PARAMETERS):
            top_three_dogs = QuizManager().search_database(responses, PARAMETERS)
            matched_pets = QuizManager().find_three_best_dogs_ids(top_three_dogs)
            return render(request, 'quiz_results.html', {
                'matched_pets': matched_pets,
            })
        else:
            raise TooFewAnswers

    except TooFewAnswers:
        raise Http404("Too few answers were given.")


def pet_detail(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
    except Pet.DoesNotExist:
        raise Http404("Pet not found")
    return render(request, 'pet_detail.html', {'pet': pet})
