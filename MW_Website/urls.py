from django.urls import path
from . import views

app_name = 'website'
urlpatterns = [
    path('', views.index_page, name='index'),
    path('about-us', views.aboutus_page, name='aboutus'),
    path('department', views.department_page, name='department'),
    path('doctors', views.doctors_page, name='doctors'),
    path('blogs', views.blogs_page, name='blogs'),
    path('blogs/details', views.blog_detail_page, name='blog_details'),
    path('contact-us', views.contactus_page, name='contactus'),
]