from django.views import generic
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import BlogModel
from MW_Setting.models import SettingModel, ContactUsModel


# url: /
class IndexPage(generic.TemplateView):
    template_name = 'mw_website/index_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_blogs'] = BlogModel.objects.all()[:3]
        return context

# url: /about-us
class AboutUsPage(generic.TemplateView):
    template_name = 'mw_website/aboutus_page.html'

# url: /department
class DepartmentPage(generic.TemplateView):
    template_name = 'mw_website/department_page.html'

# url: /doctors
class DoctorsPage(generic.TemplateView):
    template_name = 'mw_website/doctors_page.html'

# url: /blogs
class BlogsPage(generic.TemplateView):
    template_name = 'mw_website/blogs_page.html'


# url: /blog-detail////////////
class BlogDetailPage(generic.TemplateView):
    template_name = 'mw_website/blog_detail_page.html'


# url: /contact-us
class ContactIsPage(generic.CreateView):
    template_name = 'mw_website/contactus_page.html'
    model = ContactUsModel
    success_url = reverse_lazy('website:index')
    fields = ['message', 'name', 'email', 'title']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sets'] = SettingModel.objects.first()
        return context
    