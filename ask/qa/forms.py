# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from qa.models import Question, Answer


class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(u'Не верное имя пользователя')
        try:
            User.objects.get(username=username)
            raise forms.ValidationError(u'Такой пользователь уже есть!')
        except User.DoesNotExist:
            pass
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(u'Не верный адрес почты')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError(u'Пустой пароль')
        self.raw_passeord = password
        return make_password(password)

    def save(self):
        user = User(**self.cleaned_data)
        user.save()
        return user


class AskForm(forms.Form):
    """docstring for AskForm"""
    title = forms.CharField(max_length=80, label=u"Заголовок")
    text = forms.CharField(widget=forms.Textarea, label=u"Текст")

    def clean(self):
        pass
    
    def save(self):
        question = Question(**self.cleaned_data)
        question.author_id = self._user.id
        question.save()
        return question

class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label=u"Текст ответа")
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_question(self):
        question_id = self.cleaned_data['question']
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            question = None
        return question

    def clean(self):
        pass

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author_id = self._user.id
        answer.save()
        return answer


class LoginForm(forms.Form):
    """docstring for LoginForm"""
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(u'Не верное имя пользователя')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError(u'Пустой пароль')
        self.raw_passeord = password
        return make_password(password)