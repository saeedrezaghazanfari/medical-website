from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from Extentions.utils import get_user_code
from .models import User
from .forms import SignUpForm_Email, SignUpForm_Phone, SignInForm
# imports for activate account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token


# url: /sign-up
def sign_up_page(request):
    form_email = SignUpForm_Email(request.POST or None)
    form_phone = SignUpForm_Phone(request.POST or None)
    return render(request, 'mw_auth/signup.html', {
        'form_email': form_email,
        'form_phone': form_phone,
    })


# url: /sign-up-email
def signing_up_email(request):
    if request.POST:
        form = SignUpForm_Email(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data.get('passcode'))
            user.save()

            if user:
                current_site = get_current_site(request)    # get domain site
                domain = current_site.domain
                uid =urlsafe_base64_encode(force_bytes(user.pk))
                token =account_activation_token.make_token(user)
                # sending mail
                subject = _('اکتیویت حساب کاربری | MW')
                message = f'<h3>سلام و عرض خسته نباشید خدمت {user.first_name} عزیز</h3><p>لینک فعالسازی حساب کاربری:</p><a href="http://{domain}/account/activation/{uid}/{token}">برای فعالسازی کلیک کنید</a>'
                from_email = settings.EMAIL_HOST_USER
                to_list = [user.email]
                msg_EMAIL = EmailMessage(subject, message, from_email, to_list)
                msg_EMAIL.content_subtype = "html" 
                msg_EMAIL.send()

                messages.success(request, _('حساب شما با موفقیت ساخته شد. برای فعالسازی حساب، ایمیل خود را چک کنید'))
                return redirect('/sign-in')
        messages.error(request, _('ایمیل و یا کدملی شما در سیستم موجود میباشد'))
        return redirect('/sign-up')


# url: /sign-up-phone
def signing_up_phone(request):
    if request.POST:
        form = SignUpForm_Phone(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data.get('passcode'))
            user.save()
            if user:

                messages.success(request, _('حساب شما با موفقیت ساخته شد. برای فعالسازی حساب، کد پیامک شده را وارد کنید'))
                return redirect('/sign-in')


# url: /sign-in
def sign_in_page(request): 
    form = SignInForm(request.POST or None)         # TODO cache with REDIS

    if request.POST:
        if form.is_valid():
            ntcode = form.cleaned_data.get('national_code')
            passcode = form.cleaned_data.get('passcode')
            
            find_user = User.objects.filter(national_code=ntcode).first()

            if find_user:
                user = authenticate(request, username=find_user.username, password=passcode)
                if user:
                    login(request, user)
                    messages.success(request, _('شما با موفقیت وارد شدید'))
                    return redirect('/')

                messages.error(request, _('کدملی و یا رمزعبور شما اشتباه است'))
                return redirect('/sign-in')

            messages.error(request, _('کدملی شما اشتباه است و یا در سیستم موجود نیست'))
            return redirect('/sign-in')
    
    return render(request, 'mw_auth/signin.html', {
        'form': form,
    })


# url: account/activation/<uidb64>/<token>
def account_activate(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		# actiavate account
		user.is_active = True
		user.save()
		messages.info(request, _('حساب کاربری شما فعال گردید.') )
		messages.info(request, _('حساب کاربری شما فعال گردید. برای ورود به حساب، اطلاعات خود را وارد کنید') )
		return redirect('auth:signin')
	else:
		messages.info(request, _('لینک فعالسازی شما نامعتبر است.') )
		return redirect('auth:signin')


# url: forget-pw/enter-phone-email
def forget_pw_p1(request):
    return render(request, 'mw_auth/enter_email_phone.html', {})


# url: forget-pw/reset-password
def forget_pw_p2(request):
    return render(request, 'mw_auth/reset_password.html', {})


# url: /sign-out
def sign_out_page(request):
    logout(request)
    messages.info(request, _('شما با موفقیت خارج شدید'))
    return redirect('/sign-in')