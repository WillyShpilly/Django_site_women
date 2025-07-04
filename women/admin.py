from django.contrib import admin, messages
from .models import Women, Category
from django.db.models.functions import Length
from django.utils.safestring import mark_safe

# Register your models here.

class MarriedFileter(admin.SimpleListFilter):
    title = "Статус женщин"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ("married", "Замужем"),
            ("single", "Не замужем"), 
        ]

    def queryset(self, request, queryset):
        if self.value() == "married":
            return queryset.filter(husband__isnull=False)
        elif self.value() == "single":
            return queryset.filter(husband__isnull=True)



@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ("title", "content", "slug", "photo", "post_photo", "cat", "husband", "tags")
    readonly_fields = ("slug", "post_photo")
    list_display = ("id", "post_photo", "title", "time_create", "is_published", "cat")
    list_display_links = ("id", "title")
    ordering = ("-time_create", 'title')
    list_editable = ("is_published",)
    list_per_page = 5
    actions = ("set_published", "set_draft")
    search_fields = ("title", "cat__name")
    list_filter = (MarriedFileter, "cat__name", "is_published")
    filter_horizontal = ("tags", )
    save_on_top = True

    @admin.display(description="Изоображение", ordering="content")
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return "Без фото"
    
    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published = Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Опубликовать выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published = Women.Status.DRAFT)
        self.message_user(request, f"{count} записей сняты с публикации.", messages.WARNING)    


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")