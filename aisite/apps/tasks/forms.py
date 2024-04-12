from django import forms


class ChatForm(forms.Form):
    message = forms.CharField(required=True)
    history = forms.JSONField(required=True)
