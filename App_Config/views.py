from django.utils.translation import activate
from django.shortcuts import redirect


def activate_language(request):
    lang = request.GET.get('lang')
    next_url = request.GET.get('url')
    activate(lang)
    return redirect(f'/{lang}/{next_url}')

def select_lang_redirect(request):
    return redirect('/fa')