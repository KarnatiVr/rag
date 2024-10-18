from django import forms


class DocumentForm(forms.Form):
    name = forms.CharField(label="Your name", max_length=200)
    document= forms.FileField(label="Upload Document")


class ChatInput(forms.Form):
    input = forms.CharField(label="Your name", max_length=200)