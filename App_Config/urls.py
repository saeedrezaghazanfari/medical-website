from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from . import views


urlpatterns = [
    path('', views.select_lang_redirect),
    path('captcha/', include('captcha.urls')),
]

urlpatterns += i18n_patterns(
    path('', include('MW_Website.urls', namespace='website')),
    path('', include('MW_Auth.urls', namespace='auth')),
    path('', include('MW_Setting.urls', namespace='setting')),
    path('change/language/', views.activate_language, name='activate_lang'),
    path('admin/', admin.site.urls),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
