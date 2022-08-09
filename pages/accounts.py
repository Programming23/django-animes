

from django.conf.urls import url
from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from account.models import *
from django.contrib.admin.models import *
from django.contrib import auth
from pages.models import *
from django.core.mail import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import  force_bytes, force_str, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
import re
from django.conf import settings
from django.http import *
import secrets
from django.core.mail import EmailMessage
from pages.views import get_client_ip
from datetime import datetime, timedelta
from django.utils import timezone

def send_message(user,request):
    domain = get_current_site(request)
    subject = 'Activate Your Account'
    token = secrets.token_hex(14).title()
    tk = Tokens(user=user, token=token, work='activate_account').save()
    context = {
        'user':user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.email)),
        'token': token,
    }

    body = render_to_string('account/activate.html', context)

    # Please use the link below to verify your account.

    # https://{domain}/account/activate-user/{context["uid"]}/{context["token"]}'''

    try:
        message =  EmailMessage(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        message.content_subtype = 'html' # this is required because there is no plain text email message
        message.send()
    except:
        return 'not'


def register(request):


    if not request.user.is_authenticated:
        ip = get_client_ip(request)

        try:
            aip = ipAdress.objects.get(ip=ip)
        except :
            aip = ipAdress(ip=ip)
            aip.save()

        val_email = ''
        val_user = ''
        val_pass1 = ''
        val_pass2 = ''
        error = None
        if request.method == "POST":
            username = ''
            email = ''
            password1 = ''
            password2 = ''
            terms = ''
            if 'username' in request.POST:
                username = request.POST['username']

            if 'email' in request.POST:
                email = request.POST['email']

            if 'password1' in request.POST:
                password1 = request.POST['password1']

            if 'password2' in request.POST:
                password2 = request.POST['password2']
            if 'terms' in request.POST:
                terms = request.POST['terms']


            val_pass1 = password1
            val_pass2 = password2
            val_user = username
            val_email = email

            if terms != 'on':
                error = 'أنت غير موافق على الشروط'
            elif not (username and email and password1 and password2) :
                error = 'حقل فارغ'
            elif username.find(' ') != -1:
                error = 'سم المستخدم يجب ألا يحتوي على مسافات'
            elif User.objects.filter(username=username).exists():
                    error = 'اسم المستخدم موجود مسبقاً'
            elif User.objects.filter(email=email).exists():
                    error = 'هذا البريد الإلكتروني موجود مسبقا'
            elif email.find('@') < 6 or not re.fullmatch(r'\b[A-Za-z0-9]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
                error = 'هناك خطأ في بريدك الإلكتروني'
            elif len(email) <= 15:
                error = 'البريد الالكتروني يجب أن يكون أكثر من 15 حرف'
            elif password1 != password2:
                error = 'كلمة المرور غير متطابقة'
            elif password1.find(' ') != -1:
                error = 'كلمة المرور يجب ألا يحتوي على مسافات'
            elif len(password1) <= 8:
                    error = 'كلمة المرور يجب أن تكون أكثر من 8 حروف'
            elif password1.isdigit():
                error = 'كلمة المرور لا يجب أن تحتوي على أرقام فقط'
            else:
                cr_user = User.objects.create_user(username=username, email=email,password=password1)
                if send_message(cr_user, request)  == 'not':
                    cr_user.delete()
                    error = 'بريدك الإلكتروني غير صحيح'
                else:

                    x = {
                        'message': 'تم إنشاء حسابك بنجاح. المرجو التحقق من بريدك الإلكتروني'
                    }

                    return render(request, 'account/register.html', x)




        x = {
            'error':error,
            'user_value': val_user,
            'email_value': val_email,
            'pass1_value': val_pass1,
            'pass2_value': val_pass2,
            'register': True,
            'title_tag': 'سجل حسابك لمشاهدة احدث حلقات و أفلام الانمي مترجمة اون لاين',
            'domain': get_current_site(request),
        }

        return render(request, 'account/register.html', x)
    else:
        return redirect('index')



def login(request):
    if not request.user.is_authenticated:
        error = None
        form = LoginForm()
        if request.method == "POST":
            if 'username' in request.POST and 'password' in request.POST:
                username = request.POST['username']
                password = request.POST['password']

                if username and password:

                    try:
                        user = User.objects.get(email=username)
                        username = user.username
                    except:
                        pass
                    user = auth.authenticate(username=username, password=password)



                    if UsersBack.objects.filter(user=user, is_active=False).exists():
                            error = 'المرجو تفعيل حسابك'
                    else:
                        if user is not None:

                            auth.login(request, user)
                            return redirect('index')
                        else:
                            error = 'اسم المستخدم او كلمة المرور غير صحيحة'
                else:
                    error = 'حقل فارغ'
            else:
                error = 'حقل فارغ'
        x = {
            'form': form,
            'error': error,
            'page': 'login',
            'domain': get_current_site(request),
            'title': 'تسجيل الدخول',
            'title_tag': 'سجل حسابك لمشاهدة احدث حلقات و أفلام الانمي مترجمة اون لاين ',
        }

        return render(request, 'account/login.html', x)
    else:
        return redirect('index')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)

    return redirect('index')



def reset_password(request):
    if request.user.is_authenticated:
        return redirect('index')
    messages = []
    error = None
    domain = get_current_site(request)
    if request.method == 'POST':
        if not ('email' in request.POST):
            error = 'بريدك الإلكتروني فارغ'
        else:
            email = request.POST['email']
            user = None
            try:
                user = User.objects.get(email=email)
            except:
                error = 'بريدك الإلكتروني غير صحيح'
                
            if user:
                try:
                    user = UsersBack.objects.get(user=user, is_active=True)
                    user = user.user
                except:
                    error = 'بريدك الإلكتروني غير مفعل'
                    user = None
                    
                if user:

                    try:
                        tk = Tokens.objects.get(user=user, work='reset_password').delete()
                    except:
                        pass
                    token = secrets.token_hex(14).title()
                    token_db = Tokens(user=user, token=token, work='reset_password').save()

                    subject = 'reset password'
                    uid = urlsafe_base64_encode(force_bytes(user.pk))

                    body = render_to_string('messages/reset_password.html', 
                    {'domain': domain, 'uid': uid, 'token': token, 'username': user.username})


                    try:
                        send_mail(
                            subject,
                            body,
                            settings.EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=False
                        )
                        messages.append('المرجو التحقق من بريدك الالكتروني')
                    except:
                        error = 'خطأ'

    x = {
        'page': 'reset_password',
        'error': error,
        'title': 'تغيير كلمة السر',
        'messages': messages,
        'domain': domain
    }
    return render(request, 'account/login.html', x)

def reset_password_confirm(request, uidb64, token):
    if request.user.is_authenticated:
        raise Http404

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e :
        user=None

    try:
        tk = Tokens.objects.get(user=user, work='reset_password')

    except Exception as e :
        tk=None

    messages = []
    error = None
    if user and tk :
        if request.POST:
            if not('password1' in request.POST):
                error = 'الحقل الأول فارغ'
            elif not('password2' in request.POST):
                error = 'الحقل الثاني فارغ'
            else:
                password1 = request.POST['password1']
                password2 = request.POST['password2']

                if password1 != password2:
                    error = 'كلمة المرور غير متطابقة'
                elif password1.find(' ') != -1:
                    error = 'كلمة المرور يجب ألا يحتوي على مسافات'
                elif len(password1) <= 8:
                     error = 'كلمة المرور يجب أن تكون أكثر من 8 حروف'
                elif password1.isdigit():
                    error = 'كلمة المرور لا يجب أن تحتوي على أرقام فقط'
                else:
                    user.set_password(password1)
                    user.save()
                    k = tk.delete()

                    auth.login(request, user)
                    return redirect('index')
        x = {
            'title': 'تغيير كلمة السر',
            'title_tag': 'تغيير كلمة السر',
            'error': error,
            'domain': get_current_site(request),
        }
        return render(request, 'account/reset.html', x)
    raise Http404



def activate(request, uidb64, token):
    if request.user.is_authenticated:
        raise Http404
    tk = Tokens.objects.filter(created__lte=timezone.now()- timedelta(days=1)).delete()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(email=uid)
    except Exception as e :
        user=None

    try:
        tk = Tokens.objects.get(user=user, work='activate_account')
    except:
        tk = None

    if user and tk:
        user_back = UsersBack.objects.get(user=user)

        ip = get_client_ip(request)

        try:
            aip = ipAdress.objects.get(ip=ip)
        except :
            aip = ipAdress(ip=ip)

        aip.user_ip.add(user)
        aip.save()
        user_back.is_active = True
        user_back.save()

        k = tk.delete()
        auth.login(request, user)
        return redirect('index')
    raise Http404