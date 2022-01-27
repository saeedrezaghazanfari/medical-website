from pathlib import Path
from decouple import config
from django.utils.translation import gettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG')
ALLOWED_HOSTS = []
SECURE_SSL_REDIRECT = False

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # APPs
    'MW_Website.apps.MwWebsiteConfig',  # website actions
    'MW_Auth.apps.MwAuthConfig',        # authentication actions
    'MW_Setting.apps.MwSettingConfig',        # authentication actions

    # PACKs
    'widget_tweaks',
    'captcha',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # add for translating
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'MW_Website.middleware.first', # custom middleware
]
ROOT_URLCONF = config('ROOT_URLCONF')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = config('WSGI_APPLICATION')

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
#TODO postgresql database - decouple

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGES = [
    ('fa', _('Persian')),
    ('en', _('English')),
]
LANGUAGE_CODE = config('LANGUAGE_CODE')
TIME_ZONE = config('TIME_ZONE')
USE_I18N = config('USE_I18N')
USE_TZ = config('USE_TZ')

STATIC_URL = '/site_static/'
STATIC_ROOT = Path("static_cdn", "static_root")
MEDIA_URL = '/media/'
MEDIA_ROOT = Path("static_cdn", "media_root")
STATICFILES_DIRS = [ Path("assets") ]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ### More Config ### #

# custom user
AUTH_USER_MODEL = config('AUTH_USER_MODEL')

# email configs
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# kavenegar API
KAVENEGAR_API = config('KAVENEGAR_API')
LOGIN_URL = '/fa/sign-in'

# captcha
CAPTCHA_FONT_SIZE = 30
CAPTCHA_BACKGROUND_COLOR = '#fff'
CAPTCHA_FOREGROUND_COLOR = '#4f98dc'
CAPTCHA_LENGTH = 3
CAPTCHA_IMAGE_SIZE = (100, 50) 

# Redis
REDIS_DB = config('REDIS_DB')
REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')