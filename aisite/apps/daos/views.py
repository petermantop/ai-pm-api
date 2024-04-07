from rest_framework.decorators import api_view
from .models import Dao
from django.http import JsonResponse

# Create your views here.
@api_view(['GET'])
def get_daos(request):
    daos = Dao.objects.all()
    # Serialize documents to JSON
    serialized_documents = [doc.to_json() for doc in daos]

    # Return JSON response
    return JsonResponse(serialized_documents, safe=False)