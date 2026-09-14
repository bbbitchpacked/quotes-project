from django.contrib import admin
from .models import Category, Tag, Quote

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Quote)