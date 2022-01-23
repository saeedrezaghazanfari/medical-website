import re
from kavenegar import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from .models import User
from .forms import SignUpForm_Email, SignUpForm_Phone, SignInForm, ResetPassWord
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
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
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

	if user and account_activation_token.check_token(user, token):
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
def forget_pw_email_phone(request):
    if request.POST:
        user_text = request.POST.get('phone-or-email')
        if user_text:
            is_email = bool(re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)').match(user_text))
            is_phone = bool(re.compile(r'09([0-1][0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}').match(user_text))

            if is_email and not is_phone:
                user = User.objects.filter(email=user_text).first()
                if user:
                    # send email
                    current_site = get_current_site(request)    # get domain site
                    domain = current_site.domain
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = account_activation_token.make_token(user)
                    # sending mail
                    subject = _('بازیابی رمزعبور | MW')
                    message = f'<h3>سلام و عرض خسته نباشید خدمت {user.first_name} عزیز</h3><p>صفحه ی بازیابی رمزعبور:</p><a href="http://{domain}/account/reset-password/{uid}/{token}">برای ورود به صفحه ی بازیابی رمزعبور کلیک کنید</a>'
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [user.email]
                    msg_EMAIL = EmailMessage(subject, message, from_email, to_list)
                    msg_EMAIL.content_subtype = "html" 
                    msg_EMAIL.send()
                    
                    messages.success(request, _('ایمیل تغییر رمزعبور برای شما ارسال شد. ایمیل خود را چک کنید'))
                    return redirect('/forget-pw/enter-phone-email')
            elif not is_email and is_phone:
                user = User.objects.filter(phone=user_text).first()
                if user:

                    current_site = get_current_site(request)    # get domain site
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = account_activation_token.make_token(user)
                    message = f'سلام و عرض خسته نباشید خدمت {user.first_name} عزیز \n صفحه ی بازیابی رمزعبور \n http://{current_site.domain}/account/reset-password/{uid}/{token}'

                    try:
                        api = KavenegarAPI(settings.KAVENEGAR_API)
                        params = { 'sender' : '10008663', 'receptor': user_text, 'message': message }
                        response = api.sms_send(params)
                        print(response)
                    
                        messages.success(request, _('پیامک تغییر رمزعبور برای شما ارسال شد. منتظر بمانید'))
                        return redirect('/')

                    except APIException as e: 
                        print('err 1')
                        print(e)
                    except HTTPException as e:
                        print('err 2')
                        print(e)

            elif not is_email and not is_phone:
                messages.warning(request, _('فرمت ایمیل یا تلفن شما اشتباه است'))
                return redirect('/forget-pw/enter-phone-email')
            elif is_email and is_phone:
                messages.error(request, _('مشکلی بوجود آمده است'))
                return redirect('/')

    return render(request, 'mw_auth/enter_email_phone.html', {})


# url: account/reset-password/<uidb64>/<token>
def account_reset_password(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user and account_activation_token.check_token(user, token):
		form = ResetPassWord(request.POST or None)
		if form.is_valid():
			pw = form.cleaned_data.get('password2')
			user.set_password(str(pw))
			user.save()
			messages.success(request, _('رمز شما با موفقیت تغییر کرد. اطلاعات خود را وارد کنید'))
			return redirect('auth:signin')

		return render(request, 'mw_auth/reset_password.html', {'form': form})
	else:
		messages.error(request, _('لینک شما نامعتبر و یا منقضی شده است'))
		return redirect('auth:signin')


# url: /sign-out
def sign_out_page(request):
    logout(request)
    messages.info(request, _('شما با موفقیت خارج شدید'))
    return redirect('/sign-in')