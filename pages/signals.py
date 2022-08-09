from django.db.models.signals import *
from django.conf import Settings, settings
from .models import *
from django.core.mail import *
from django.contrib.auth.models import User
from account.models import *
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import  force_bytes, force_str, force_text
from django.template.loader import render_to_string
#from django.contrib.sites.shortcuts import get_current_site


def CreateEpisode(sender, instance, created, **kwargs):
    
    if created :
        episode = instance
        users = UsersBack.objects.filter(animes_now=episode.name, is_active=True, notification=True)
        name = episode.name.name.title()
        subject = f'حلقة جديدة من أنمك المفضل {name}'
        eps_url = urlsafe_base64_encode(force_bytes(episode.pk))
        domain = Domain.objects.all()[0].domain
        for user in users:
            context = {
                'username': user.user.username,
                'episode': episode.episode, 
                'name': name,
                'domain': domain,
                'url': eps_url
            }
            body = render_to_string('messages/new_episode.html', context)
            try:
                mes = EmailMessage(
                    subject,
                    body,
                    settings.EMAIL_HOST_USER,
                    [user.user.email]
                )
                mes.content_subtype = 'html' # this is required because there is no plain text email message
                mes.send()
            except:
                print("Failed")
            

post_save.connect(CreateEpisode, sender=Episodes)