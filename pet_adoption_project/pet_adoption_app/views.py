from django.http import Http404, HttpResponse
from django.shortcuts import render

from .database_creation import initialize_data, initialize_questions
from .models import Pet, Question


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
    question_objs = Question.objects.all()
    return render(request, 'quiz_main_page.html', {
        'questions': question_objs,
        })


def submit_form(request):
    if request.method == 'POST':
        responses = {}
        for key, value in request.POST.items():
            responses[key] = value
            print(value)

        del responses["csrfmiddlewaretoken"]
        print(responses)
        return render(request, 'quiz_results.html', {
            'responses': responses,
        })
    else:
        return HttpResponse("Form submission method is not POST.")


def pet_detail(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
    except Pet.DoesNotExist:
        raise Http404("Pet not found")
    return render(request, 'pet_detail.html', {'pet': pet})
