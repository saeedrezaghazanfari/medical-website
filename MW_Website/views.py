from django.views import generic
from django.urls import reverse_lazy
from .models import BlogModel
from django.contrib import messages
from MW_Setting.models import SettingModel, ContactUsModel, NewsEmailModel
from django.utils.translation import gettext_lazy as _
from .forms import CommentForm


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
class BlogsPage(generic.ListView):
    template_name = 'mw_website/blogs_page.html'
    model = BlogModel
    queryset = BlogModel.objects.filter(is_published=True).all()
    paginate_by = 3

# url: /blogs/<slug:slug>
class BlogDetailPage(generic.DetailView):
    model = BlogModel
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
    template_name = 'mw_website/blog_detail_page.html'


# url: /blogs/<slug:slug>
class EmailForNewsUrl(generic.View):
    def post(self, request):
        email = request.POST['emailfield']

        if NewsEmailModel.objects.filter(email=email).first() != email: 
            email_created = NewsEmailModel.objects.create(email=email)
            if email_created:
                messages.info(request, _('ایمیل شما با موفقیت ذخیره شد'))
                return reverse_lazy('website:blogs')

            return reverse_lazy('website:blogs')
        messages.error(request, _('این ایمیل قبلا وارد شده است'))
        return reverse_lazy('website:blogs')


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
    