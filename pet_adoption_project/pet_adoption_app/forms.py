from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from pet_adoption_app.models import Pet


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PetInDatabase(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["name", "species", "breed", "age", "sex", "size", "temperament", "personality", "kid_friendly",
                  "dog_friendly", "cat_friendly", "neutered", "submitter", "submission_date", "vaccinations"]
