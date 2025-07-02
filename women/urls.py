from django.urls import path
from women.views import WomenHome, about, ShowPost, contact, login, WomenCategory, WomenTagView, AddPage, UpdatePage, DeletePage

urlpatterns = [
    path('', WomenHome.as_view(), name="home"),
    path('about/', about, name="about"),
    path('addpage/', AddPage.as_view(), name="add_page"),
    path('contact/', contact, name="contact"),
    path('login/', login, name="login"),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name="post"),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name="category"),
    path('tag/<slug:tag_slug>/', WomenTagView.as_view(), name="tag"),
    path("edit/<slug:slug>/", UpdatePage.as_view(), name="edit_page"),
    path('delete/<slug:slug>/', DeletePage.as_view(), name='delete_page'),
]
