from django.db import models

# Create your models here.
class Employee(models.Model):
    name  = models.CharField(max_length=200)
    title = models.CharField(max_length= 200)


    def __str__(self):
        info = f'{self.name} - {self.title}'
        return info
