from django.contrib import admin, messages
from .models import Women, Category
from django.db.models.functions import Length

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
    fields = ("title", "content", "slug", "cat", "husband", "tags")
    readonly_fields = ("slug", )
    list_display = ("id", "title", "time_create", "is_published", "cat")
    list_display_links = ("id", "title")
    ordering = ("-time_create", 'title')
    list_editable = ("is_published",)
    list_per_page = 5
    actions = ("set_published", "set_draft")
    search_fields = ("title", "cat__name")
    list_filter = (MarriedFileter, "cat__name", "is_published")
    filter_horizontal = ("tags", )

    @admin.display(description="Краткое описание", ordering=Length("content"))
    def brief_info(self, women: Women):
        return f"Описание: {len(women.content)} символов"
    
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