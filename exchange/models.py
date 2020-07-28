from django.db import models
import datetime
# Create your models here.

# Create your models here.


class Exchange(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.title
