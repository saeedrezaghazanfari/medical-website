# Generated by Django 4.0.1 on 2022-01-10 08:57

import Extentions.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialtyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField()),
            ],
            options={
                'verbose_name': 'تخصص',
                'verbose_name_plural': 'تخصص \u200cها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DoctorModel',
            fields=[
                ('code', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='کد دکتر')),
                ('profile', models.ImageField(blank=True, null=True, upload_to=Extentions.utils.doctor_image_path, verbose_name='پروفایل')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'دکتر',
                'verbose_name_plural': 'دکترها',
                'ordering': ['-user__id'],
            },
        ),
    ]
