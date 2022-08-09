from django.contrib.auth.models import User
import secrets

user = ipAdress(ip=secrets.token_hex(14).title()).save()

w = open("hamza.txt", "w")

w.write(str(user))
w.close()