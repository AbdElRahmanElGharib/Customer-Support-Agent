from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from ingestion.singleton import shared_embedder

# Create your views here.
class APIIngestView(APIView):
    @csrf_exempt
    def post(self, request):
        text = request.data.get('text', '')
        
        embedding = shared_embedder.embed_texts([text])
        
        return Response(
            {
                'status': 'success',
                'embedding': embedding.tolist(),
            }
        )