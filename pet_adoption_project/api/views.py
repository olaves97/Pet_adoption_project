from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ItemSerializer
from pet_adoption_app.models import Pet


@api_view(['GET'])
def getData(request):
    pets = Pet.objects.all()
    serializer = ItemSerializer(pets, many=True)
    return Response(serializer.data)
