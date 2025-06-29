from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
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
    
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.IntegerField(сhoices=Status, default=Status.DRAFT)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, related_query_name="posts")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')
    husband = models.OneToOneField("Husband", on_delete=models.SET_NULL, null=True, blank=True, related_name="woman")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title
    

    class Meta:
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