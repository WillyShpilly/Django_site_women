from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import Women, Category, TagPost
from .forms import AddPostForm

import uuid
import os
# Create your views here.


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


def index(request):
    posts = Women.published.all().select_related("cat")
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": posts,
        "cat_selected": 0
    }
    return render(request, "women/index.html", context = data)


def handle_uploaded_file(f):
    file_name, file_extension = os.path.splitext(f.name)
    with open(f'uploads/{file_name}_{uuid.uuid4()}{file_extension}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    # if request.method == "POST":
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         handle_uploaded_file(request.cleaned_data['file'])

    # else:
    #     form = UploadFileForm()    
    return render(request, "women/about.html", {"title": "О сайте", "menu": menu})


def addpage(request):
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            # try:
            #     Women.objects.create(**form.changed_data)
            #     return redirect("home")
            # except:
            #     form.add_error(None, "Ошибка добавления поста")
            form.save()    
            return redirect("home")
    else:        
        form = AddPostForm()
    
    data = {
        "menu": menu, 
        "title": "Добавление статьи",
        "form": form
    }
    return render(request, "women/addpage.html", context = data)


def contact(request):
    return HttpResponse("Обратная связь")   


def login(request):
    return HttpResponse("Авторизация")


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        "title": post.title,
        "menu": menu,
        "post": post,
        "cat_selected": 1,
    }
    return render(request, "women/post.html", context=data)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat=category).select_related("cat")
    
    data = {
        "title": f"Рубрика: {category.name}",
        "menu": menu,
        "posts": posts,
        "cat_selected": category.pk,
    }
    return render(request, "women/index.html", context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug = tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related("cat")

    data = {
        "title": f"Тег: {tag:tag}",
        "menu": menu,
        "posts": posts,
        "cat_selected": None,
    }

    return render(request, "women/index.html", context=data)
