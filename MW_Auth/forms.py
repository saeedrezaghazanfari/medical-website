from dataclasses import fields
from django import forms
from .models import User
from django.utils.translation import gettext_lazy as _


class SignUpForm_Email(forms.ModelForm):
    passcode = forms.CharField(
        label=_("گذر واژه"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': _('رمزعبور خود را وارد کنید')}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'national_code', 'passcode']
        widgets = {
            'first_name': forms.TextInput({'placeholder': _('نام خود را وارد کنید')}),
            'last_name': forms.TextInput({'placeholder': _('نام خانوادگی خود را وارد کنید')}),
            'email': forms.EmailInput({'placeholder': _('ایمیل خود را وارد کنید')}),
            'national_code': forms.NumberInput({'placeholder': _('کدملی خود را وارد کنید')}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).first():
            raise forms.ValidationError(_('این ایمیل در سیستم ثبت شده است'))
        return email

    def clean_national_code(self):
        national_code = self.cleaned_data.get('national_code')
        if User.objects.filter(national_code=national_code).first():
            raise forms.ValidationError(_('این کدملی در سیستم ثبت شده است'))
        return national_code


class SignUpForm_Phone(forms.ModelForm):
    passcode = forms.CharField(
        label=_("گذر واژه"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': _('رمزعبور خود را وارد کنید')}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'national_code', 'passcode']
        widgets = {
            'first_name': forms.TextInput({'placeholder': _('نام خود را وارد کنید')}),
            'last_name': forms.TextInput({'placeholder': _('نام خانوادگی خود را وارد کنید')}),
            'phone': forms.NumberInput({'placeholder': _('شماره تلفن خود را وارد کنید')}),
            'national_code': forms.NumberInput({'placeholder': _('کدملی خود را وارد کنید')}),
        }

    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(_('این شماره تلفن در سیستم ثبت شده است'))
        return phone

    def clean_national_code(self):
        national_code = self.cleaned_data.get('national_code')
        if User.objects.filter(national_code=national_code).exists():
            raise forms.ValidationError(_('این کدملی در سیستم ثبت شده است'))
        return national_code

class SignInForm(forms.ModelForm):
    passcode = forms.CharField(
        label=_("گذر واژه"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': _('رمزعبور خود را وارد کنید')}),
    )

    class Meta:
        model = User
        fields = ['national_code', 'passcode']
        widgets = {
            'national_code': forms.NumberInput({'placeholder': _('کدملی خود را وارد کنید')}),
        }