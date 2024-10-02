from rest_framework import serializers
from pet_adoption_app.models import Pet


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'
