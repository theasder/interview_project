# -*- coding: utf-8 -*-
from django import forms
from .models import Problem, Comment, Reply
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
        error_messages = {
            'text': {
                'required': 'Напишите что-то содержательное, а потом нажимайте кнопку.'
            }
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('text', )
        error_messages = {
            'text': {
                'required': 'Напишите что-то содержательное, а потом нажимайте кнопку.'
            }
        }

# class LoginForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

#     class Meta:
#         model = User
#         fields = ('username', 'password')
#         labels = {
#             'username': ('Имя пользователя')
#         }

# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')
#         labels = {
#             'username': ('Имя пользователя'),
#             'email': ('Электронная почта')
#         }

class ProblemForm(forms.ModelForm):

    class Meta:
        model = Problem
        fields = ('title', 'problem_text', 'wiki_answer', 'topic', 'position')
        labels = {
            'title': ('Название'),
            'problem_text': ('Описание'),
            'wiki_answer': ("Ответ на задачу (опционально)"),
            'topic': ("Тема"),
            'position': ('Название позиции')
        }

        error_messages = {
            'title': {
                'max_length': ("Название слишком длинное."),
                'required': ("Это поле обязательно для заполнения.")
            },
            'problem_text': {
                'max_length': ("Описание слишком длинное."),
                'required': ("Это поле обязательно для заполнения.")
            },
            'wiki_answer': {
                'max_length': ("Ответ на задание слишком длинный."),
            },
            'topic': {
                'required': ("Это поле обязательно для заполнения.")
            },
            'position': {
                'required': ("Это поле обязательно для заполнения.")
            },
        }
    # title = forms.CharField(label='Название', max_length=80)
    # problem_text = forms.Textarea()
    # wiki_answer = forms.Textarea()
    # topic = forms.CharField(label='Тема', max_length=50)

