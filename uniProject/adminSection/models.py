from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.core.validators import validate_image_file_extension

# Create your models here.

class AppUser(AbstractUser):
    is_admin = models.BooleanField(default=False)

class Document(models.Model):
    title = models.CharField(max_length=30)
    desc = models.CharField(max_length=200)
    docfile = models.FileField('Image', upload_to='static/%Y/%m/%d',
                               validators=[validate_image_file_extension])
