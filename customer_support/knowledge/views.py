from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knowledge.query_service import RAGQueryService

class QueryAPIView(APIView):
    def post(self, request):
        query = request.data.get('query', '')
        if not query.strip():
            return Response({"error": "Query cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        service = RAGQueryService(top_k=5)
        results = service.query(query)

        return Response({"results": results})
