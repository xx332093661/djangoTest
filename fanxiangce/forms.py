# coding: utf-8

from django import forms


class CommentForm(forms.Form):
    body = forms.CharField(label='留言')


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=64, widget=forms.TextInput(attrs={'class': 'form-control form-input'}))
    password = forms.CharField(label='密 码', widget=forms.PasswordInput(attrs={'class': 'form-control form-input'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=64, widget=forms.TextInput(attrs={'class': 'form-control form-input'}))
    email = forms.EmailField(label='邮箱', max_length=64, widget=forms.TextInput(attrs={'class': 'form-control form-input'}))
    name = forms.CharField(label='昵称', max_length=64, widget=forms.TextInput(attrs={'class': 'form-control form-input'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control form-input'}))
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={'class': 'form-control form-input'}))