# Generated by Django 4.0.1 on 2022-01-13 08:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MW_Website', '0004_alter_doctornotesmodel_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctornotesmodel',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 13, 11, 44, 42, 173893)),
        ),
    ]
