from django.db import models
from account.models import UsersBack
from pages.models import Episodes
from django.utils import timezone
# Create your models here.
# class Comment(models.Model):
#     user = models.ForeignKey(UsersBack, on_delete=models.CASCADE)
#     episode = models.CharField(max_length=50)
#     reply = models.ForeignKey('Comment', null=True, related_name='replies', blank=True, on_delete=models.CASCADE)
#     content = models.TextField(max_length=1000)
#     publish_date = models.DateTimeField( default=timezone.now )
#     parent = models.ForeignKey('Comment', null=True, related_name='parent_of_comment', blank=True, on_delete=models.CASCADE)


#     @property
#     def children(self):
#         return Comment.objects.filter(parent=self)

   
    
