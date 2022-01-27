from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class MwWebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MW_Website'
    verbose_name = _('ماژول های وبسایت')