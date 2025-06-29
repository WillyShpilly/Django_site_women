from django.urls import path
from women.views import index, about, show_post, addpage, contact, login, show_category, show_tag_postlist

urlpatterns = [
    path('', index, name="home"),
    path('about/', about, name="about"),
    path('addpage/', addpage, name="add_page"),
    path('contact/', contact, name="contact"),
    path('login/', login, name="login"),
    path('post/<slug:post_slug>/', show_post, name="post"),
    path('category/<slug:cat_slug>/', show_category, name="category"),
    path('tag/<slug:tag_slug>/', show_tag_postlist, name="tag"),
]
