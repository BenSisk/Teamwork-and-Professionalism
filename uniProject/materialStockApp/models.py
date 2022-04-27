from email.policy import default
from pyexpat import model
from re import T
from django.db import models

# Create your models here.

class Stock(models.Model):
    name = models.CharField(max_length=255, blank=True,null=True)
    materialType = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True,null=True)

    def __str__(self):
      return self.name + ' ' + str(self.materialType) + ' ' + str(self.quantity)