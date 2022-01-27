from django import forms
from .models import User
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _


class SignUpForm_Email(forms.ModelForm):
    passcode = forms.CharField(
        label=_("گذر واژه"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': _('رمزعبور خود را وارد کنید')}),
    )
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'national_code', 'passcode']
        widgets = {
            'first_name': forms.TextInput({'placeholder': _('نام خود را وارد کنید')}),
            'last_name': forms.TextInput({'placeholder': _('نام خانوادگی خود را وارد کنید')}),
            'email': forms.EmailInput({'placeholder': _('ایمیل خود را وارد کنید')}),
            'national_code': forms.NumberInput({'placeholder': _('کدملی خود را وارد کنید')}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        for i in first_name:
            if ord(i) < 1000:
                raise forms.ValidationError(_('نام باید شامل کاراکترهای فارسی باشد'))
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        for i in last_name:
            if ord(i) < 1000:
                raise forms.ValidationError(_(' نام‌خانوادگی باید شامل کاراکترهای فارسی باشد'))
        return last_name

    def clean_passcode(self):
        passcode = self.cleaned_data.get('passcode')
        for i in passcode:
            if ord(i) > 1000:
                raise forms.ValidationError(_('رمزعبور باید شامل کاراکترهای انگلیسی باشد'))
        return passcode
    
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
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'national_code', 'passcode']
        widgets = {
            'first_name': forms.TextInput({'placeholder': _('نام خود را وارد کنید')}),
            'last_name': forms.TextInput({'placeholder': _('نام خانوادگی خود را وارد کنید')}),
            'phone': forms.NumberInput({'placeholder': _('شماره تلفن خود را وارد کنید')}),
            'national_code': forms.NumberInput({'placeholder': _('کدملی خود را وارد کنید')}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        for i in first_name:
            if ord(i) < 1000:
                raise forms.ValidationError(_('نام باید شامل کاراکترهای فارسی باشد'))
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        for i in last_name:
            if ord(i) < 1000:
                raise forms.ValidationError(_(' نام‌خانوادگی باید شامل کاراکترهای فارسی باشد'))
        return last_name

    def clean_passcode(self):
        passcode = self.cleaned_data.get('passcode')
        for i in passcode:
            if ord(i) > 1000:
                raise forms.ValidationError(_('رمزعبور باید شامل کاراکترهای انگلیسی باشد'))
        return passcode
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).first():
            raise forms.ValidationError(_('این شماره تلفن در سیستم ثبت شده است'))
        return phone

    def clean_national_code(self):
        national_code = self.cleaned_data.get('national_code')
        if User.objects.filter(national_code=national_code).first():
            raise forms.ValidationError(_('این کدملی در سیستم ثبت شده است'))
        return national_code

class SignInForm(forms.Form):
    passcode = forms.CharField(
        label=_("گذر واژه"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': _('رمزعبور خود را وارد کنید')}),
    )
    national_code = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': _('کدملی خود را وارد کنید') }))

    def clean_national_code(self):
        ntcode = self.cleaned_data.get('national_code')
        if not User.objects.filter(national_code=ntcode).first():
            raise forms.ValidationError(_('این کدملی در سیستم ثبت نشده است'))
        return ntcode


class ResetPassWord(forms.Form):
    password1 = forms.CharField(
        label=_("گذر واژه"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': _('رمزعبور خود را وارد کنید')}),
    )
    password2 = forms.CharField(
        label=_("تکرار گذر واژه"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': _('رمزعبور خود را تکرار کنید')}),
    )
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        for i in password:
            if ord(i) > 1000:
                raise forms.ValidationError(_('رمزعبور باید شامل کاراکترهای انگلیسی باشد'))
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password2 != password1:
            raise forms.ValidationError(_('باید هردو پسورد با هم برابر باشند'))
        return password2
        