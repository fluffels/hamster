from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True)#pattern="u[0-9]{8}"
    password = forms.CharField(widget=forms.PasswordInput, required=True)