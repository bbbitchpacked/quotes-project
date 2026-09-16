from django import forms
from .models import Category, Tag, Quote


class QuoteCreateForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'category']


class QuoteUpdateForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'category']


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class TagUpdateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class QuoteTagsAddForm(forms.Form):
    tag_id = forms.IntegerField()