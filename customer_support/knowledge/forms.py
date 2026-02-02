from django import forms

class DocumentUploadForm(forms.Form):
    file = forms.FileField(
        label="Select Document",
        help_text="Upload a PDF or TXT file."
    )