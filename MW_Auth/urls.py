from django.urls import path
from . import views


app_name = 'auth'
urlpatterns = [
    path('sign-up', views.sign_up_page, name='signup'),
    path('sign-up/email', views.signing_up_email, name='signup-email'),
    path('sign-up/phone', views.signing_up_phone, name='signup-phone'),
    path('forget-pw/enter-phone-email', views.forget_pw_p1, name='forget-pw-1'),
    path('forget-pw/reset-password', views.forget_pw_p2, name='forget-pw-2'),
    path('sign-in', views.sign_in_page, name='signin'),
    path('sign-out', views.sign_out_page, name='signout'),
    path('account/activation/<uidb64>/<token>', views.account_activate, name='activate-account'),
]