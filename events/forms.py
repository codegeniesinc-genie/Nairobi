from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from .models import Blog, Event


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


#Register User
class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username','email', 'password1', 'password2']

#Authenticate user
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = '__all__'

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'county', 'category_type', 'location', 'price', 'image', 'date', 'time', 'contact_email', 'is_published']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


    