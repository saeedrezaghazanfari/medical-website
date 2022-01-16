# Generated by Django 4.0.1 on 2022-01-15 14:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MW_Website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentmodel',
            name='is_show',
            field=models.BooleanField(default=False, verbose_name='نمایش؟'),
        ),
        migrations.AlterField(
            model_name='doctormodel',
            name='specialties',
            field=models.ManyToManyField(to='MW_Website.SpecialtyModel', verbose_name='تخصص\u200cها'),
        ),
        migrations.AlterField(
            model_name='doctornotesmodel',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 15, 18, 8, 50, 703433)),
        ),
    ]