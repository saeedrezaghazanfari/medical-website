from django.shortcuts import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from MW_Setting.models import SettingModel, ContactUsModel, NewsEmailModel
from MW_Auth.models import User
from .models import BlogModel, CommentModel
from .forms import CommentForm


# url: /
class IndexPage(generic.TemplateView):
    template_name = 'mw_website/index_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_blogs'] = BlogModel.objects.filter(is_published=True).all()[:3]
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
    context_object_name = 'blog'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thispost = context['object']
        context['form'] = CommentForm()                                                   # send form
        context['comments'] = CommentModel.objects.filter(blog=thispost, is_reply=False)  # send comments
        context['comments_nums'] = context['comments'].count()                            # send comments numbers
        return context
    template_name = 'mw_website/blog_detail_page.html'


# url: /blogs/comment/save 
class CommentSaveURL(generic.View):
    def post(self, request):
        pass

# url: /blogs/<slug:slug>
class EmailForNewsUrl(generic.View):
    def post(self, request):
        email = request.POST['emailfield']
        if email:
            if not NewsEmailModel.objects.filter(email=email).first(): 
                email_created = NewsEmailModel.objects.create(email=email)
                if email_created:
                    messages.success(request, _('ایمیل شما با موفقیت ذخیره شد'))
                    return redirect('/blogs')
                messages.warning(request, _('مشکلی در ثبت ایمیل پیش آمد'))
                return redirect('/blogs')
            messages.error(request, _('این ایمیل قبلا وارد شده است'))
            return redirect('/blogs')
        messages.error(request, _('فرمت ایمیل را درست وارد کنید'))
        return redirect('/blogs')


# url: /blogs/search/
class SearchBoxURL(generic.ListView):
    template_name = 'mw_website/blogs_page.html'
    model = BlogModel
    def get_queryset(self):
        request = self.request
        query = request.GET.get('query')
        lookup = Q(title__icontains=query) | Q(short_desc__icontains=query) | Q(writer__user__first_name__icontains=query)  | Q(writer__user__last_name__icontains=query) 
        return BlogModel.objects.filter(lookup, is_published=True).distinct()
    paginate_by = 3


# url: /blogs/search/tags
class SearchTagURL(generic.ListView):
    template_name = 'mw_website/blogs_page.html'
    model = BlogModel
    def get_queryset(self):
        request = self.request
        query = request.GET.get('query')
        return BlogModel.objects.filter(tags__title__iexact=query, is_published=True).distinct()
    paginate_by = 3


# url: /blogs/search/categories

class SearchCategoryURL(generic.ListView):
    template_name = 'mw_website/blogs_page.html'
    model = BlogModel
    def get_queryset(self):
        request = self.request
        query = request.GET.get('query')
        return BlogModel.objects.filter(categories__title__iexact=query, is_published=True).distinct()
    paginate_by = 3

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
    