from django import forms
from .models import Article, Comment, Contact, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': 'التعليق',
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        labels = {
            'name': 'اسمكِ',
            'email': 'بريدكِ الإلكتروني',
            'message': 'اكتبي رسالتكِ هنا 💌',
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']

        labels = {
            'image': 'صورة الملف الشخصي',
            'bio': 'نبذة عنكِ',  
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

