from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm, PetInDatabase
from .models import Pet, Question
from .quiz_functions import QuizManager

from django.contrib.auth import login



PARAMETERS = ['size', 'age', 'sex', 'breed', 'temperament', 'personality', 'kid_friendly', 'dog_friendly',
              'cat_friendly', 'neutered']


@require_http_methods(["GET"])
def home(request):
    return render(request, 'home.html', {})


@require_http_methods(["GET"])
def pets(request):
    all_pets = Pet.objects.all()
    return render(request, 'pets.html', {
        'pets': all_pets,
    })


@require_http_methods(["GET"])
def quiz(request):
    question_objs = Question.objects.all()
    return render(request, 'quiz_main_page.html', {
        'questions': question_objs,
    })


class TooFewAnswers(Exception):
    pass


@require_http_methods(["GET", "POST"])
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


@require_http_methods(["GET"])
def pet_detail(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
    except Pet.DoesNotExist:
        raise Http404("Pet not found")
    return render(request, 'pet_detail.html', {'pet': pet})


@require_http_methods(["POST", "GET"])
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home/')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html/', {'form': form})


@require_http_methods(["GET"])
@user_passes_test(lambda u: u.groups.filter(name='Moderators').exists(), login_url='/login/')
def moderator_dashboard(request):
    database_table = Pet.objects.all()
    return render(request, 'moderator_dashboard.html', {'database_table': database_table})


@require_http_methods(["POST", "GET"])
@user_passes_test(lambda u: u.groups.filter(name='Moderators').exists(), login_url='/login/')
def edit(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    if request.method == "POST":
        formset = PetInDatabase(request.POST, instance=pet)
        if formset.is_valid():
            formset.save()
            return redirect('/moderator/')
    else:
        formset = PetInDatabase(instance=pet)

    return render(request, 'database_actions/edit.html', {'formset': formset})


@require_http_methods(["POST", "GET"])
@user_passes_test(lambda u: u.groups.filter(name='Moderators').exists(), login_url='/login/')
def create_a_record(request):
    if request.method == "POST":
        formset = PetInDatabase(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/moderator/')
    else:
        formset = PetInDatabase()
    return render(request, 'database_actions/create.html', {'formset': formset})


@user_passes_test(lambda u: u.groups.filter(name='Moderators').exists(), login_url='/login/')
def pet_delete(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)

    if request.method == 'POST':
        pet.delete()
        return redirect('/moderator/')

    return render(request, 'pet_confirm_delete.html', {'pet': pet})