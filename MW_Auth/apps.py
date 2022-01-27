from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MwAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MW_Auth'
    verbose_name = _('احراز هویت')