from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MwSettingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MW_Setting'
    verbose_name = _('تنظیمات')
