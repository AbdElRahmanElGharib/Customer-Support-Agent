from rest_framework.views import APIView
from django.views.generic import TemplateView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from knowledge.singleton import shared_query_service
from django.views.generic.edit import FormView
from django.core.files.storage import FileSystemStorage
from .forms import DocumentUploadForm
from .tasks import process_document
from .models import DocumentSubmission
from django.core.cache import cache
from django.conf import settings


class QueryAPIView(APIView):
    def post(self, request):
        query = request.data.get('query', '')
        if not query.strip():
            return Response({"error": "Query cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        
        results = shared_query_service.query_with_llm(query)

        return Response({"results": results})

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def post(self, request, *args, **kwargs):
        user_message = request.POST.get('message', '')

        bot_reply = shared_query_service.query_with_llm(user_message)

        return JsonResponse({'response': bot_reply})

class DocumentUploadView(FormView):
    template_name = 'upload.html'
    form_class = DocumentUploadForm
    success_url = '/upload/?success=true'

    def form_valid(self, form):
        uploaded_file = form.cleaned_data['file']
        email = form.cleaned_data['email']
        
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        
        submission = DocumentSubmission.objects.create(file=filename, status=DocumentSubmission.Status.SUBMITTED, user_email=email)
        process_document.delay(submission.pk)   # type: ignore

        return super().form_valid(form)

class SubmissionsView(TemplateView):
    template_name = 'submissions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submissions = cache.get(settings.SUBMISSIONS_CACHE_KEY)
        if submissions is None:
            submissions = list(
                DocumentSubmission.objects.all()
                .order_by("-created_at")
                .values(
                    "id",
                    "file",
                    "user_email",
                    "created_at",
                    "status",
                    "last_updated",
                )
            )

            cache.set(settings.SUBMISSIONS_CACHE_KEY, submissions, settings.SUBMISSIONS_CACHE_TTL_SECONDS)
        
        context['submissions'] = submissions
        return context
