from django.db import models
import datetime
from django.urls import reverse
from django import forms
import ccxt

# Create your models here.

# Create your models here.
ccxtExchabges=ccxt.exchanges
EXCHANGES=[]
for ex in ccxtExchabges:
    EXCHANGES.append((ex,ex))
 

print("----EXCHANGES:".format(EXCHANGES))
class Ccxtx(models.Model):
    exchanges= models.CharField(max_length=25, choices=EXCHANGES, default='binance') 
     

    def __str__(self):
        return self.title

     