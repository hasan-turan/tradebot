from django.db import models
import datetime
from django.urls import reverse
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

    def get_detail_url(self):
        # return "/exchange/{}".format(self.id)
        # burada belirtilen exchange: urls.py içindeki app_name depişkenini refere eder
        return reverse(viewname='exchange:detail', kwargs={'id': self.id})

    def get_index_url(self):
        # return "/exchange/{}".format(self.id)
        # burada belirtilen exchange: urls.py içindeki app_name depişkenini refere eder
        return reverse(viewname='exchange:index')

    def get_update_url(self):
        # return "/exchange/{}".format(self.id)
        # burada belirtilen exchange: urls.py içindeki app_name depişkenini refere eder
        return reverse(viewname='exchange:update', kwargs={'id': self.id})
