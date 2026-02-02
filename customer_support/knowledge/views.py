from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knowledge.singleton import shared_query_service

class QueryAPIView(APIView):
    def post(self, request):
        query = request.data.get('query', '')
        if not query.strip():
            return Response({"error": "Query cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        
        results = shared_query_service.query_with_llm(query)

        return Response({"results": results})
