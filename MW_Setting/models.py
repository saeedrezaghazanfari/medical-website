from django.db import models
from django.utils.translation import gettext_lazy as _
from Extentions.utils import brands_image_path


class SettingModel(models.Model):
    x_scale = models.FloatField(blank=True, null=True, verbose_name=_('مقیاس ایکس'))
    y_scale = models.FloatField(blank=True, null=True, verbose_name=_('مقیاس ایگرگ'))
    marker_text = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('متن شما روی نقشه'))
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('کشور'))
    state = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('استان'))
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('شهرستان'))
    phone = models.PositiveBigIntegerField(verbose_name=_('تلفن'))
    from_to = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('زمان گشایش'))
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name=_('ایمیل'))
    your_text = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('متن شما درمورد ارتباط'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('‌تنظیمات')
        verbose_name_plural = _('‌تنظیمات')

    def __str__(self):
        return str(_('شما حتما باید یک مقدار در این جدول ذخیره کنید.'))


class BrandsModel(models.Model):
    brand_image = models.ImageField(upload_to=brands_image_path, null=True, blank=True, verbose_name=_('تصویر برند'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('تصویر برند‌')
        verbose_name_plural = _('تصاویر برند‌ها')

    def __str__(self):
        return str(self.id)


class ContactUsModel(models.Model):
    message = models.TextField(verbose_name=_('متن ارتباط'))
    name = models.CharField(max_length=100, verbose_name=_('نام کاربر'))
    email = models.EmailField(max_length=100, verbose_name=_('ایمیل کاربر'))
    title = models.CharField(max_length=100, verbose_name=_('عنوان ارتباط'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('پیام مخاطب')
        verbose_name_plural = _('پیام های مخاطبان')

    def __str__(self):
        return str(self.title)