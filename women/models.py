from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name = "Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category', kwargs={"cat_slug": self.slug}) 
    

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"
    
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.IntegerField(choices=Status, default=Status.DRAFT, verbose_name="Статус")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="slug")
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, related_query_name="posts", verbose_name="Категории")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="Теги")
    husband = models.OneToOneField("Husband", on_delete=models.SET_NULL, null=True, blank=True, related_name="woman", verbose_name="Муж")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name = "Известные женщины"
        verbose_name_plural = "Известные женщины"
        ordering = ["-time_create"]
        indexes = [
            models.Index(fields=["-time_create"])
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('post', kwargs={"post_slug": self.slug})    
    


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)    
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tag', kwargs={"tag_slug": self.slug})
    

class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name
    
 