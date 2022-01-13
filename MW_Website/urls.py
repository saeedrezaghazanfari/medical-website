from django.urls import path
from . import views


app_name = 'website'
urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('about-us', views.AboutUsPage.as_view(), name='aboutus'),
    path('department', views.DepartmentPage.as_view(), name='department'),
    path('doctors', views.DoctorsPage.as_view(), name='doctors'),
    path('blogs/', views.BlogsPage.as_view(), name='blogs'),
    path('blogs/<slug:slug>', views.BlogDetailPage.as_view(), name='blog_details'),
    path('contact-us', views.ContactIsPage.as_view(), name='contactus'),
]