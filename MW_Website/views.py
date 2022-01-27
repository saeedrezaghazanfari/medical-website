import redis
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from MW_Setting.models import SettingModel, ContactUsModel, NewsEmailModel
from django.http import JsonResponse
from MW_Auth.models import User
from .models import BlogModel, CommentModel, BlogLikesModel
from .forms import CommentForm


# redis connection
rd = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB,  charset="utf-8", decode_responses=True)

# url: /
class IndexPage(generic.TemplateView):
    template_name = 'mw_website/index_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = BlogModel.objects.filter(is_published=True).all()[:3]
        list_blogs = []
        for blog in blogs:
            list_blogs.append({
                'blog':blog, 
                'likes': rd.hget('blog_like_nums', blog.slug),   # read from redis
                'comments': rd.hget('blog_comment_nums', blog.slug) # read from redis
            })
        context['last_blogs'] = list_blogs
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
    def get_queryset(self):
        blogs = BlogModel.objects.filter(is_published=True).all()
        blogs_comments = []
        for blog in blogs:
            blogs_comments.append({
                'blog': blog, 
                'num_comments': rd.hget('blog_comment_nums', blog.slug)
            })
        return blogs_comments
    paginate_by = 3


# url: /blogs/like/<slug:slug>
class BlogLikePage(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            exist = BlogLikesModel.objects.filter(user=request.user, blog=BlogModel.objects.get(slug=kwargs['slug'])).first()
            if not exist:
                like = BlogLikesModel.objects.create(user=request.user, blog=BlogModel.objects.get(slug=kwargs['slug']))
                if like:
                    likes = BlogLikesModel.objects.filter(blog=BlogModel.objects.get(slug=kwargs['slug'])).count()
                    return JsonResponse({'counter': likes, 'status': 200}, safe=False)
            
            elif exist:
                dislike = BlogLikesModel.objects.get(user=request.user, blog=BlogModel.objects.get(slug=kwargs['slug'])).delete()
                if dislike:
                    likes = BlogLikesModel.objects.filter(blog=BlogModel.objects.get(slug=kwargs['slug'])).count()
                    return JsonResponse({'counter': likes, 'status': 203}, safe=False)

        return JsonResponse({'status': 404}, safe=False)


# url: /blogs/<slug:slug>
class BlogDetailPage(LoginRequiredMixin, generic.DetailView):
    model = BlogModel
    context_object_name = 'blog'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thispost = context['object']
        context['form'] = CommentForm()                                                                      # send form
        context['comments'] = CommentModel.objects.filter(blog=thispost, is_reply=False, is_show=True)    # send comments
        context['replies'] = CommentModel.objects.filter(blog=thispost, is_reply=True, is_show=True)    # send replyes
        context['is_like'] = bool(BlogLikesModel.objects.filter(blog=thispost, user=self.request.user).first())   # like it?     
        context['comments_nums'] = context['comments'].count() + context['replies'].count()     # send comments numbers
        context['likes'] = BlogLikesModel.objects.filter(blog=thispost).count()                # send likes numbers

        # save or update - redis
        rd_exitst = rd.hget('blog_comment_nums', thispost.slug)
        if rd_exitst:
            rd.hdel('blog_comment_nums', thispost.slug)
            rd.hdel('blog_like_nums', thispost.slug)
            rd.hsetnx('blog_comment_nums', thispost.slug, context['comments_nums'])
            rd.hsetnx('blog_like_nums', thispost.slug, BlogLikesModel.objects.filter(blog=thispost).count())
        else:
            rd.hsetnx('blog_comment_nums', thispost.slug, context['comments_nums'])
            rd.hsetnx('blog_like_nums', thispost.slug, BlogLikesModel.objects.filter(blog=thispost).count())

        return context
    template_name = 'mw_website/blog_detail_page.html'


# url: /blogs/comment/save 
class CommentSaveURL(LoginRequiredMixin, generic.View):
    def post(self, request):
        msg = request.POST['message']
        blog_slug = request.POST['at_blog']
        reply = request.POST['isreply']
        comment_id = request.POST['commentid']

        if msg and blog_slug and reply == 'False' and comment_id == '':
            blog = BlogModel.objects.filter(slug=blog_slug).first()
            comment = CommentModel.objects.create(message=msg, user=request.user, blog=blog)
            if comment and blog:
                messages.success(request, _('نظر شما ثبت شد. بعد از تایید در سایت نمایش خواهد شد'))
                return redirect(f'/blogs/{blog_slug}')
            
            messages.success(request, _('مشکلی به وجود آمده است'))
            return redirect('/')

        elif msg and blog_slug and reply == 'True' and comment_id:
            blog = BlogModel.objects.filter(slug=blog_slug).first()
            comment = CommentModel.objects.get(id=comment_id)
            reply = CommentModel.objects.create(reply=comment, message=msg, user=request.user, blog=blog, is_reply=True)
            if reply and blog:
                messages.success(request, _('پاسخ شما ثبت شد. بعد از تایید در سایت نمایش خواهد شد'))
                return redirect(f'/blogs/{blog_slug}')

            messages.success(request, _('مشکلی به وجود آمده است'))
            return redirect('/')


# url: /blogs/<slug:slug>
class EmailForNewsUrl(LoginRequiredMixin, generic.View):
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
    paginate_by = 3
    def get_queryset(self):
        request = self.request
        query = request.GET.get('query')
        lookup = Q(title__icontains=query) | Q(short_desc__icontains=query) | Q(writer__user__first_name__icontains=query)  | Q(writer__user__last_name__icontains=query) 
        blogs = BlogModel.objects.filter(lookup, is_published=True).distinct()

        blogs_comments = []
        for blog in blogs:
            counter = blog.commentmodel_set.filter(is_show=True).count()
            blogs_comments.append({'blog': blog, 'num_comments': counter})
        return blogs_comments

# url: /blogs/search/tags
class SearchTagURL(generic.ListView):
    template_name = 'mw_website/blogs_page.html'
    model = BlogModel
    paginate_by = 3
    def get_queryset(self):
        request = self.request
        query = request.GET.get('query')
        blogs = BlogModel.objects.filter(tags__title__iexact=query, is_published=True).distinct()
        blogs_comments = []
        for blog in blogs:
            counter = blog.commentmodel_set.filter(is_show=True).count()
            blogs_comments.append({'blog': blog, 'num_comments': counter})
        return blogs_comments


# url: /blogs/search/categories

class SearchCategoryURL(generic.ListView):
    template_name = 'mw_website/blogs_page.html'
    model = BlogModel
    def get_queryset(self):
        request = self.request
        query = request.GET.get('query')
        blogs = BlogModel.objects.filter(categories__title__iexact=query, is_published=True).distinct()
        blogs_comments = []
        for blog in blogs:
            counter = blog.commentmodel_set.filter(is_show=True).count()
            blogs_comments.append({'blog': blog, 'num_comments': counter})
        return blogs_comments
    paginate_by = 3

# url: /contact-us
class ContactUsPage(generic.CreateView):
    template_name = 'mw_website/contactus_page.html'
    model = ContactUsModel
    success_url = reverse_lazy('website:index')
    fields = ['message', 'name', 'email', 'title']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sets'] = SettingModel.objects.first()
        return context
    