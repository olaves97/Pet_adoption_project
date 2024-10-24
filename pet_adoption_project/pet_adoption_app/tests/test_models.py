from django.test import TestCase
from django.utils import timezone
from pet_adoption_app.models import Vaccine, Pet, Question


class PetModelTests(TestCase):

    def setUp(self):
        self.vaccine1 = Vaccine.objects.create(name="Rabies")
        self.vaccine2 = Vaccine.objects.create(name="Parvovirus")

        self.pet = Pet.objects.create(
            name="Buddy",
            species="Dog",
            breed="Golden Retriever",
            age=5,
            sex="Male",
            size="Medium",
            temperament="Calm",
            personality="Cuddly",
            kid_friendly="Yes",
            dog_friendly="Yes",
            cat_friendly="Yes",
            neutered="Yes",
            submitter="John Doe",
            submission_date=timezone.now()
        )
        self.pet.vaccinations.add(self.vaccine1, self.vaccine2)

    def test_pet_creation(self):
        self.assertEqual(self.pet.name, "Buddy")
        self.assertEqual(self.pet.species, "Dog")
        self.assertEqual(self.pet.age, 5)
        self.assertEqual(self.pet.vaccinations.count(), 2)


class VaccineModelTests(TestCase):

    def setUp(self):
        self.vaccine = Vaccine.objects.create(name="Rabies")

    def test_vaccine_creation(self):
        self.assertEqual(self.vaccine.name, "Rabies")

    def test_vaccine_str(self):
        self.assertEqual(str(self.vaccine), "Rabies")


class QuestionModelTests(TestCase):

    def setUp(self):
        self.question = Question.objects.create(
            question_text="What kind of dog are you looking for?",
            first_option="Small",
            second_option="Medium",
            third_option="Big",
            fourth_option="Doesn't matter"
        )

    def test_question_creation(self):
        self.assertEqual(self.question.question_text, "What kind of dog are you looking for?")
        self.assertEqual(self.question.first_option, "Small")
        self.assertEqual(self.question.second_option, "Medium")

    def test_question_str(self):
        self.assertEqual(str(self.question), "What kind of dog are you looking for?")