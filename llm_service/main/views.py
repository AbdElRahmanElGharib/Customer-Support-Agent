from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.singleton import shared_llm_service

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def post(self, request):
        user_message = request.POST.get('message', '')

        bot_reply = shared_llm_service.generate_answer(user_message)

        return JsonResponse({'response': bot_reply})

class APIMessageView(APIView):
    @csrf_exempt
    def post(self, request):
        user_message = request.data.get('message', '')

        result = shared_llm_service.generate_answer(user_message)

        return Response(
            {
                "status": "success",
                "response": result,
            }
        )
