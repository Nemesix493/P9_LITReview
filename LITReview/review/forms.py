from django import forms

class SigninForm(forms.forms):
    username = forms.CharField(max_length=63, label='Nom d\'utilisateur', widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}))
    password = forms.CharField(max_length=63, label='Nom d\'utilisateur', widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))
    re_password = forms.CharField(max_length=63, label='Nom d\'utilisateur', widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe à nouveau'}))