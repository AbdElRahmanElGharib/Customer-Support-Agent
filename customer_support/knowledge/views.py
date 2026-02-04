from rest_framework.views import APIView
from django.views.generic import TemplateView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from knowledge.singleton import shared_query_service
from django.views.generic.edit import FormView
from django.core.files.storage import FileSystemStorage
from .forms import DocumentUploadForm
from knowledge.management.commands.ingest_documents import Command as IngestCommand
from .tasks import process_document
from .models import DocumentSubmission

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
        
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        
        submission = DocumentSubmission.objects.create(file=filename, status=DocumentSubmission.Status.SUBMITTED)
        process_document.delay(submission.pk)   # type: ignore

        return super().form_valid(form)
