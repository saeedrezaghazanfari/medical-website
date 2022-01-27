from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from django.db import models
from django.utils.translation import gettext_lazy as _
from Extentions.utils import get_user_code, user_image_path


class User(AbstractUser):
    username = models.CharField(max_length=12, unique=True, default=get_user_code, verbose_name=_('کد کاربری'))
    ip = models.GenericIPAddressField(blank=True, null=True, verbose_name=_('آیپی'))
    phone = models.BigIntegerField(blank=True, null=True, verbose_name=_('شماره تلفن'))
    national_code = models.BigIntegerField(blank=True, null=True, unique=True, verbose_name=_('کدملی'))
    profile = models.ImageField(upload_to=user_image_path, null=True, blank=True, verbose_name=_('پروفایل'))

    def get_profile(self):
        if self.profile:
            return format_html(f'<img style="height: 100px; width: 110px; border-radius: 5px;" src="{self.profile.url}" />')
        else:
            return None
    get_profile.short_description = _('پروفایل')

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    get_full_name.short_description = _('نام و نام خانوادگی')

    class Meta:
        ordering = ['-id']
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')
