# Generated by Django 3.0.8 on 2020-07-28 07:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0004_auto_20200728_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 28, 10, 7, 16, 840866)),
        ),
    ]