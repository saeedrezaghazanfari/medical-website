from django.shortcuts import render

# url: /
def index_page(request):
    return render(request, 'mw_website/index_page.html', {})

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

    