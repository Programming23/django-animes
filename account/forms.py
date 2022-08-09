from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="اسم المستخدم ", max_length=30, help_text="اسم المستخدم يجب ألا يحتوي على مسافات")
    email = forms.EmailField(label="البريد الالكتروني ")
    password1 = forms.CharField(label="كلمة المرور ", widget=forms.PasswordInput(), min_length=8)
    password2 = forms.CharField(label="تأكيد كلمة المرور ", widget=forms.PasswordInput(), min_length=8)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.ModelForm):
    username = forms.CharField(label="اسم المستخدم ", max_length=30)
    password = forms.CharField(label="كلمة المرور ", widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')



    
