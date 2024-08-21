from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, PetInDatabase
from .models import Pet, Question
from .quiz_functions import QuizManager

from django.contrib.auth import login


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


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html/', {'form': form})


@user_passes_test(lambda u: u.groups.filter(name='Moderators').exists())
def moderator_dashboard(request):
    database_table = Pet.objects.all()
    return render(request, 'moderator_dashboard.html', {'database_table': database_table})


def edit(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    if request.method == "POST":
        formset = PetInDatabase(request.POST, instance=pet)
        if formset.is_valid():
            formset.save()
            return redirect('/moderator')
    else:
        formset = PetInDatabase(instance=pet)

    return render(request, 'database_actions/edit.html', {'formset': formset})


def create_a_record(request):
    if request.method == "POST":
        formset = PetInDatabase(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/moderator')
    else:
        formset = PetInDatabase()
    return render(request, 'database_actions/create.html', {'formset': formset})


def delete(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    pet.delete()
    database_table = Pet.objects.all()
    return render(request, 'moderator_dashboard.html', {'database_table': database_table})

