from django.db import models


class Pet(models.Model):
    SEX_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    SIZE_CHOICES = [('Small', 'Small'), ('Medium', 'Medium'), ('Big', 'Big')]
    DECISION_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    TEMP_CHOICES = [('Calm', 'Calm'), ('Energetic', 'Energetic')]
    PERSONALITY_CHOICES = [('Cuddly', 'Cuddly'), ('Distant', 'Distant')]
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=30)
    breed = models.CharField(max_length=30, blank=True)
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, blank=True)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    temperament = models.CharField(max_length=20, choices=TEMP_CHOICES)
    personality = models.CharField(max_length=30, choices=PERSONALITY_CHOICES, blank=True)
    kid_friendly = models.CharField(max_length=3, choices=DECISION_CHOICES, blank=True)
    dog_friendly = models.CharField(max_length=3, choices=DECISION_CHOICES, blank=True)
    cat_friendly = models.CharField(max_length=3, choices=DECISION_CHOICES, blank=True)
    neutered = models.CharField(max_length=3, choices=DECISION_CHOICES)
    submitter = models.CharField(max_length=100)
    submission_date = models.DateTimeField()
    vaccinations = models.ManyToManyField('Vaccine', blank=True)


class Vaccine(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.CharField(max_length=200, null=True)
    first_option = models.CharField(max_length=200, null=True)
    second_option = models.CharField(max_length=200, null=True)
    third_option = models.CharField(max_length=200, null=True)
    fourth_option = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.question_text


# class Answer(models.Model):
#     answer = models.OneToOneField('Questions', on_delete=models.CASCADE, primary_key=True)
#
#     def __str__(self):
#         return self.answer
