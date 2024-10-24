from django import forms
from .models import User


class DocumentForm(forms.Form):
    name = forms.CharField(label="Your name", max_length=200)
    document= forms.FileField(label="Upload Document")


class ChatInput(forms.Form):
    input = forms.CharField(label="Your name", max_length=200)
    choices = forms.ModelChoiceField(queryset=User.objects.values_list('document', flat=True), empty_label="None", label='Document',to_field_name="document", required=False)