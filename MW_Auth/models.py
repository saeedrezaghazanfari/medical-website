from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ip = models.GenericIPAddressField(blank=True, null=True, verbose_name=_('آیپی'))
    phone = models.BigIntegerField(blank=True, null=True, verbose_name=_('شماره تلفن'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')
