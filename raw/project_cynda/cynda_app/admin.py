from django.contrib import admin
from .models import Category, Tag, Quote


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'category')
    list_filter = ('category', 'tags')
    search_fields = ('text',)
    filter_horizontal = ('tags',)