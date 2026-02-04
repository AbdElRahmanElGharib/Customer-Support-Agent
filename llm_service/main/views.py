from django.views.generic import TemplateView
from django.http import JsonResponse
from main.singleton import shared_llm_service

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def post(self, request, *args, **kwargs):
        user_message = request.POST.get('message', '')

        bot_reply = shared_llm_service.generate_answer(user_message)

        return JsonResponse({'response': bot_reply})
