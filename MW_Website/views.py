from django.views import generic
from django.shortcuts import render
from .models import (
    BlogModel
)


# url: /
class IndexPage(generic.TemplateView):
    template_name = 'mw_website/index_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_blogs'] = BlogModel.objects.all()[:3]
        return context

# url: /about-us
def aboutus_page(request):
    return render(request, 'mw_website/aboutus_page.html', {})

# url: /department
def department_page(request):
    return render(request, 'mw_website/department_page.html', {})

# url: /doctors
def doctors_page(request):
    return render(request, 'mw_website/doctors_page.html', {})

# url: /blogs
def blogs_page(request):
    return render(request, 'mw_website/blogs_page.html', {})


# url: /blog-detail////////////
def blog_detail_page(request):
    return render(request, 'mw_website/blog_detail_page.html', {})


# url: /contact-us
def contactus_page(request):
    return render(request, 'mw_website/contactus_page.html', {})

    