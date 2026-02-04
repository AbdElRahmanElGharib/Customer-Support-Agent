from django import forms
from email_validator import validate_email, EmailNotValidError
class DocumentUploadForm(forms.Form):
    file = forms.FileField(
        label="Select Document",
        help_text="Upload a PDF or TXT file."
    )
    email = forms.EmailField(
        label="Your Email",
        help_text="We'll notify you when the processing is complete."
    )

    def validate_file_type(self):
        uploaded_file = self.cleaned_data['file']
        if not uploaded_file.name.lower().endswith(('.pdf', '.txt')):
            raise forms.ValidationError("Unsupported file type. Please upload a PDF or TXT file.")
        
    def validate_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except EmailNotValidError as e:
            raise forms.ValidationError(str(e))
        return email
