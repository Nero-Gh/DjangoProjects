from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserPreference(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    currence = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return f'{self.user.username} '+ f'{self.currence}'