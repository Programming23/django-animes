from django import forms
from .models import *
from account.models import *

class ProfileForm(forms.ModelForm):

    #bio = forms.CharField(label='معلومات عنك', required=False)
    profile_image = forms.ImageField(label='صورة الغلاف', required=False)
    social_github = forms.URLField(label='حساب github الخاص بك ', required=False)
    social_instagram = forms.URLField(label='حساب instagram الخاص بك ', required=False)
    social_twitter = forms.URLField(label='حساب twitter الخاص بك ', required=False)
    social_website = forms.URLField(label='موقعك  ', required=False)
    notification = forms.BooleanField(label='الإشعارات ', required=False)
    information_public = forms.BooleanField(label='المعلومات  ', required=False,
            help_text="رؤية الأخرين للملف الشخصي (Profile)")

    class Meta:
        model = UsersBack
        fields = ['bio',  'profile_image',
                  'social_github', 'social_instagram', 'social_twitter',
                   'social_website', 'notification', 'information_public']

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="اسم المستخدم ", max_length=30, help_text="اسم المستخدم يجب ألا يحتوي على مسافات")
    email = forms.EmailField(label="البريد الالكتروني ")
    password1 = forms.CharField(label="كلمة المرور ", widget=forms.PasswordInput(), min_length=8)
    password2 = forms.CharField(label="تأكيد كلمة المرور ", widget=forms.PasswordInput(), min_length=8)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.ModelForm):
    username = forms.CharField(label="إسم المستخدم أو البريد الإلكتروني" , max_length=30)
    password = forms.CharField(label="كلمة المرور ", widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')
#username = forms.CharField(label="اسم المستخدم ", max_length=30, help_text="اسم المستخدم يجب ألا يحتوي على مسافات")