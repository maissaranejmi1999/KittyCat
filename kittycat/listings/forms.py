from django import forms
from .models import Cat, UserProfile, AdoptionRequest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

# Form for creating and updating a Cat model instance
class CatForm(forms.ModelForm):
    class Meta:
        model = Cat  #  Specify the model to use
        fields = ['name', 'age', 'breed', 'castrated', 'image1', 'image2']
        widgets = {
            'image1': forms.ClearableFileInput(attrs={'multiple': False}),
            'image2': forms.ClearableFileInput(attrs={'multiple': False})
        }

# Form for registering a new user
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Form for updating user profile information
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile  #  Specify the model to use
        fields = ['profile_picture', 'contact_info']

# Form submitting an adoption request
class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest  #  Specify the model to use
        fields = ['cat']

# Form for searching cats
class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search by name or breed')
    castrated = forms.BooleanField(required=False, label='Castrated only')
    min_age = forms.IntegerField(required=False, label='Minimum Age')
    max_age = forms.IntegerField(required=False, label='Maximum Age')

