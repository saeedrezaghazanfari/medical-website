import redis
from kavenegar import *
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from .models import User
# imports for activate account
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token

# redis connection
rd = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB,  charset="utf-8", decode_responses=True)

@shared_task
def send_mail_signup_email(username, domain):
    user = User.objects.get(username=username)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    subject = 'اکتیویت حساب کاربری | MW'
    message = f'<h3>سلام و عرض خسته نباشید خدمت {user.first_name} عزیز</h3><p>لینک فعالسازی حساب کاربری:</p><a href="http://{domain}/account/activation/{uid}/{token}">برای فعالسازی کلیک کنید</a>'
    from_email = settings.EMAIL_HOST_USER
    to_list = [user.email]
    msg_EMAIL = EmailMessage(subject, message, from_email, to_list)
    msg_EMAIL.content_subtype = "html" 
    msg_EMAIL.send()
    return f'send email to {user.email} / signup'


@shared_task
def send_sms_signup_phone(username, domain):
    user = User.objects.get(username=username)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    message = f'سلام و عرض خسته نباشید خدمت {user.first_name} عزیز\nلینک فعالسازی حساب کاربری:\n\nhttp://{domain}/account/activation/{uid}/{token}'

    api = KavenegarAPI(settings.KAVENEGAR_API)
    params = {
        'sender': settings.KAVENEGAR_SENDER, 
        'receptor': user.phone, 
        'message': message 
    }
    response = api.sms_send(params)
    print(response)

    return f'send SMS to {user.phone} / signup'


@shared_task
def send_mail_forgetpw_email(username, domain):
    user = User.objects.get(username=username)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    # sending mail
    subject = 'بازیابی رمزعبور | MW'
    message = f'<h3>سلام و عرض خسته نباشید خدمت {user.first_name} عزیز</h3><p>صفحه ی بازیابی رمزعبور:</p><a href="http://{domain}/account/reset-password/{uid}/{token}">برای ورود به صفحه ی بازیابی رمزعبور کلیک کنید</a>'
    from_email = settings.EMAIL_HOST_USER
    to_list = [user.email]
    msg_EMAIL = EmailMessage(subject, message, from_email, to_list)
    msg_EMAIL.content_subtype = "html" 
    msg_EMAIL.send()
    return f'send email to {user.email} / fp'


@shared_task
def send_sms_forgetpw_phone(username, domain):
    user = User.objects.get(username=username)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    message = f'سلام و عرض خسته نباشید خدمت {user.first_name} عزیز\nصفحه ی بازیابی رمزعبور\nhttp://{domain}/account/reset-password/{uid}/{token}'

    api = KavenegarAPI(settings.KAVENEGAR_API)
    params = {
        'sender' : settings.KAVENEGAR_SENDER, 
        'receptor': user_text, 
        'message': message 
    }
    response = api.sms_send(params)
    print(response)
    return f'send SMS to {user.phone} / fp'

