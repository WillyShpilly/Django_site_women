from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Women, Category, TagPost
from .forms import AddPostForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .utils import DataMixin
from django.core.paginator import Paginator

import uuid
import os
# Create your views here.


class WomenHome(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    title_page = "Главная страница"
    cat_selected = 0



    def get_queryset(self):
        return Women.published.all().select_related("cat")


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
    return render(request, "women/about.html", {"title": "О сайте"})


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "women/addpage.html"
    title_page = "Добавление статьи"


class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ["title", "content", "photo", "is_published", "cat"]
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    title_page = "Редактирование статьи"


class DeletePage(DataMixin, DeleteView):
    model = Women
    context_object_name = 'post'
    success_url = reverse_lazy('home')
    title_page = "Удаление статьи"


def contact(request):
    return HttpResponse("Обратная связь")   


def login(request):
    return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context["post"].title)
  
    
    def get_object(self, queryset = None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class WomenCategory(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False
    

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related("cat")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context["posts"][0].cat
        return self.get_mixin_context(context, title = "Категория - " + cat.name, cat_selected=cat.pk,)
 

class WomenTagView(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        return self.get_mixin_context(context, title=f'Тег - {tag.tag}', )

    


