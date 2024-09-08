from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author'] 
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
