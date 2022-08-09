from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import *

from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage


def createProfile(sender, instance, created, **kwargs):
    if created == True:
        domain = Domain.objects.all()[0]
        user = instance
        profile = UsersBack(
            user=user
        )
        profile.save()

        subject = f'Welcome to {domain.domain}'
        message = 'We are glad you are here!'
        message = render_to_string("messages/welcome.html", {'username': user.username })
       
        try:
            mes = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
            )
            mes.content_subtype = 'html' # this is required because there is no plain text email message
            mes.send()
        except:
            pass
        
def UpdateProfile(sender, instance, created, **kwargs):
    if created == False:

        profile = instance
        print(profile.username)
        user = User.objects.get(username=profile.user.username)
        print(user.username)
        user.username = profile.username
        user.email = profile.email
        user.save()

post_save.connect(createProfile, sender=User)
#post_save.connect(UpdateProfile, sender=UsersBack)