from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "subject", "message")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"class": "form-input", "autocomplete": "email"}),
            "subject": forms.TextInput(attrs={"class": "form-input"}),
            "message": forms.Textarea(attrs={"class": "form-input", "rows": 6}),
        }
