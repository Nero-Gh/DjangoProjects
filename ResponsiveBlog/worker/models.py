from distutils.command.upload import upload
from email.policy import default
from django.db import models

# Create your models here.

class Workers(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} and {self.title}'


class BlogPost(models.Model):
    title = models.CharField(max_length=255, null=False , blank = False)
    description = models.TextField(null=False , blank = False)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images', null=True , blank =True)

    def __str__(self):
        return f'{self.title} , {self.description}, {self.featured}'