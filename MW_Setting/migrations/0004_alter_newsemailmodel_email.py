# Generated by Django 4.0.1 on 2022-01-13 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MW_Setting', '0003_alter_newsemailmodel_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsemailmodel',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True, verbose_name='ایمیل'),
        ),
    ]