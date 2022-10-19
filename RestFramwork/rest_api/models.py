from email.policy import default
from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    email = models.EmailField(default='')

    def __str__(self):
        return f'{self.title},{self.autor},{self.email}'
