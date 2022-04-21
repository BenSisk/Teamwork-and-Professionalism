from django.db import models

# Create your models here.
NEW_PAGE = (
	('Yes', True),
	('No', False),
)


class crawlerModel(models.Model):
	newPage = models.CharField(max_length=2, choices=NEW_PAGE, default='No')

