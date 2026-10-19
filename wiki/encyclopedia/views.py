from django.shortcuts import render
from django import forms
import random

from . import util

class PageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput)
    content = forms.CharField(label="Content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def view_page(request, title):
    page = util.get_entry(title)
    if page:
        return render(request, "encyclopedia/wiki_page.html", {
            "page": page,
            "title": title
        })
    return render(request, "encyclopedia/error_page.html", {
            "title": title
    })

def search(request):
    q = request.GET.get('q', '')
    page = util.get_entry(q)
    if page:
        return render(request, "encyclopedia/wiki_page.html", {
            "page": page
        })
    pages = util.list_entries()
    page = [item for item in pages if q in item]
    return render(request, "encyclopedia/search.html", {
        "pages": page
    })

def create_page(request):
    form = PageForm()
    if request.method != "POST":
        return render(request, "encyclopedia/create_page.html", {
        "form": form
    })

    title = request.POST.get('title', '')
    content = request.POST.get('content', '')
    if title.strip() and content.strip():
        path = request.path
        if "edit" not in path:
            if util.get_entry(title):
                return render(request, "encyclopedia/create_page.html", {
                    "error": 'Page already exists',
                    "form": form
                })
        util.save_entry(title, content)
    return view_page(request, title)

def edit_page(request, title):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        if title.strip() and content.strip():
            util.save_entry(title, content)
            return view_page(request, title)
    form = PageForm()
    form.fields['title'].initial = title
    form.fields['content'].initial = util.get_entry(title)

    return render(request, "encyclopedia/edit_page.html", {
        "form": form,
        "title": title
    })

def random_page(request):
    generator = random.Random()
    titles = util.list_entries()
    return view_page(request, generator.choice(titles))
