from django import forms

class DocumentUploadForm(forms.Form):
    file = forms.FileField(
        label="Select Document",
        help_text="Upload a PDF or TXT file."
    )

    def validate_file_type(self):
        uploaded_file = self.cleaned_data['file']
        if not uploaded_file.name.lower().endswith(('.pdf', '.txt')):
            raise forms.ValidationError("Unsupported file type. Please upload a PDF or TXT file.")
