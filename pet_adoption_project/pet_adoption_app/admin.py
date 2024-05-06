from django.contrib import admin

from pet_adoption_app.models import Pet, Vaccine, Question

admin.site.register(Pet)
admin.site.register(Vaccine)
admin.site.register(Question)
