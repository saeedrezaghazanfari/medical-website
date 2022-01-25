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
    path('blogs/like/<slug:slug>', views.BlogLikePage.as_view(), name='blog_like'),
    path('blogs/comment/save', views.CommentSaveURL.as_view(), name='comment_save'),
    # path('blogs/comment/like', views.CommentLikeURL.as_view(), name='comment_like'),
    path('blogs/search/', views.SearchBoxURL.as_view(), name='blog_search'),
    path('blogs/search/tags/', views.SearchTagURL.as_view(), name='blog_search_tag'),
    path('blogs/search/categories/', views.SearchCategoryURL.as_view(), name='blog_search_category'),
    path('save/email', views.EmailForNewsUrl.as_view(), name='savemail'),
    path('contact-us', views.ContactUsPage.as_view(), name='contactus'),
]