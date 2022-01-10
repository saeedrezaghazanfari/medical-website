import datetime
from django.db import models
from django.db.models.base import Model, ModelState
from MW_Auth.models import User
from django.utils.translation import gettext_lazy as _
from Extentions.utils import doctor_image_path, patient_image_path, get_doctor_code, get_patient_code


class DoctorModel(models.Model):
    code = models.AutoField(primary_key=True, unique=True, editable=False, default=get_doctor_code, verbose_name=_('کد پزشک'))
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    profile = models.ImageField(upload_to=doctor_image_path, null=True, blank=True, verbose_name=_('پروفایل'))
    specialties = models.ManyToManyField(to='SpecialtyModel', verbose_name=_('تخصص ها'))
    bio = models.TextField(max_length=300, blank=True, null=True, verbose_name=_('بیوگرافی'))

    class Meta:
        ordering = ['-user__id']
        verbose_name = _('پزشک')
        verbose_name_plural = _('پزشک ها')

    def __str__(self):
        return str(self.code)

    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    get_full_name.short_description = _('نام پزشک')


class SpecialtyModel(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('عنوان تخصص'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('تخصص')
        verbose_name_plural = _('تخصص ‌ها')
    
    def __str__(self):  
        return self.title


class PatientModel(models.Model):
    code = models.AutoField(primary_key=True, unique=True, editable=False, default=get_patient_code, verbose_name=_('کد بیمار'))
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    profile = models.ImageField(upload_to=patient_image_path, null=True, blank=True, verbose_name=_('پروفایل'))

    class Meta:
        ordering = ['-user__id']
        verbose_name = _('بیمار')
        verbose_name_plural = _('بیماران')

    def __str__(self):
        return str(self.code)

    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    get_full_name.short_description = _('نام بیمار')


class DoctorNotesModel(models.Model):
    doctor = models.ForeignKey(to=DoctorModel, on_delete=models.CASCADE, verbose_name=_('پزشک'))
    short_title = models.CharField(max_length=100, verbose_name=_('عنوان کوتاه'))
    text = models.TextField(max_length=400, verbose_name=_('متن'))
    created = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        ordering = ['-id']
        verbose_name = _('نوت پزشک')
        verbose_name_plural = _('نوت های پرشکان')

    def __str__(self):
        return self.short_title

    def get_full_name(self):
        return f'{self.doctor.user.first_name} {self.doctor.user.last_name}'
    get_full_name.short_description = _('نام پزشک')


class BlogModel(models.Model):
    writer = models.ForeignKey(to=DoctorModel, on_delete=models.CASCADE, verbose_name=_('نویسنده'))
    categories = models.ManyToManyField(to='CategoryModel', verbose_name=_('دسته بندی ها'))
    tags = models.ManyToManyField(to='TagModel', verbose_name=_('تگ ها'))
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))
    desc = models.TextField(verbose_name=_('متن مقاله'))
    short_desc = models.CharField(max_length=500, verbose_name=_('متن کوتاه'))
    is_liked = models.BooleanField(default=False, verbose_name=_('لایک؟'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('بلاگ')
        verbose_name_plural = _('بلاگ‌ها')

    def __str__(self):
        return self.title

    def get_full_name(self):
        return f'{self.writer.user.first_name} {self.writer.user.last_name}'
    get_full_name.short_description = _('نام نویسنده')


class CommentModel(models.Model):
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('پاسخ'))
    message = models.TextField(verbose_name=_('نظر'))
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    blog = models.ForeignKey(to=BlogModel, on_delete=models.CASCADE, verbose_name=_('بلاگ'))
    created = models.DateTimeField(auto_now_add=True)
    is_reply = models.BooleanField(default=False, verbose_name=_('پاسخ؟'))
    is_like = models.BooleanField(default=False, verbose_name=_('لایک؟'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('نظر کاربر')
        verbose_name_plural = _('نظرات کاربران')

    def __str__(self):
        return self.blog.title

class CategoryModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('دسته بندی')
        verbose_name_plural = _('دسته بندی ها')

    def __str__(self):
        return self.title


class TagModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('تگ')
        verbose_name_plural = _('تگ ها')

    def __str__(self):
        return self.title