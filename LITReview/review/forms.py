from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

from .models import Ticket, Review

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}),
        }

        
SignupForm.base_fields['password1'].widget.attrs['placeholder'] = 'Mot de passe'
SignupForm.base_fields['password2'].widget.attrs['placeholder'] = 'Mot de passe à nouveau'


class FollowUserForm(forms.Form):

    follow = forms.ChoiceField()

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['follow'].choices = self.get_choices_for_user()
    
    def get_choices_for_user(self):
        User = get_user_model()
        not_followeds = User.objects.exclude(
            id__in=[
                self.user.id,
                *[followed.id for followed in self.user.follows.all()]
            ]
        )
        return [
            (not_followed.id, not_followed.username) for not_followed in not_followeds
        ]
    def save(self):
        User = get_user_model()
        self.user.follows.add(User.objects.get(id=self.data['follow']))


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre du ticket'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description du ticket'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        OPTIONS = [(i, f'- {i}') for i in range(6)]
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'rating': 'Note :'
        }
        widgets = {
            'headline': forms.TextInput(attrs={'placeholder': 'Titre de la critique'}),
            'body': forms.Textarea(attrs={'placeholder': 'Commentaire'}),
            'rating': forms.RadioSelect(choices=OPTIONS)
        }


class CustomAuthenticationForm(AuthenticationForm):
    pass

CustomAuthenticationForm.base_fields['username'].widget.attrs['placeholder'] = 'Nom d\'utilisateur'
CustomAuthenticationForm.base_fields['password'].widget.attrs['placeholder'] = 'Mot de passe'
