from django.db import models
from MW_Auth.models import User
from django.utils.translation import gettext_lazy as _
from Extentions.utils import doctor_image_path


class DoctorModel(models.Model):
    code = models.AutoField(primary_key=True, unique=True, editable=False, verbose_name=_('کد دکتر'))
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    profile = models.ImageField(upload_to=doctor_image_path, null=True, blank=True, verbose_name=_('پروفایل'))
    # specialties = models.ManyToManyField(to='SpecialtyModel', blank=True, null=True, verbose_name=_('تخصص ها'))

    class Meta:
        ordering = ['-user__id']
        verbose_name = _('دکتر')
        verbose_name_plural = _('دکترها')


class SpecialtyModel(models.Model):
    name = models.IntegerField()

    class Meta:
        ordering = ['-id']
        verbose_name = _('تخصص')
        verbose_name_plural = _('تخصص ‌ها')