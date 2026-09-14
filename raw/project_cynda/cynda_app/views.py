from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Category, Tag, Quote


class QuoteDetailView(View):
    def get(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        obj = {
            'id': quote.id,
            'text': quote.text,
            'category_id': quote.category_id,
            'tags': list(quote.tags.values('id', 'name')),
        }
        return JsonResponse(obj)


class QuoteRandomView(View):
    def get(self, request):
        quote = Quote.objects.order_by('?').first()
        obj = {
            'id': quote.id,
            'text': quote.text,
            'category_id': quote.category_id,
            'tags': list(quote.tags.values('id', 'name')),
        }
        return JsonResponse(obj)


class QuoteCreateView(View):
    def post(self, request):
        text = request.POST.get('text')
        category_id = request.POST.get('category_id')
        quote = Quote.objects.create(text=text, category_id=category_id)
        obj = {
            'id': quote.id,
            'text': quote.text,
            'category_id': quote.category_id,
        }
        return JsonResponse(obj)


class QuoteUpdateView(View):
    def post(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        quote.text = request.POST.get('text')
        quote.category_id = request.POST.get('category_id')
        quote.save()
        obj = {
            'id': quote.id,
            'text': quote.text,
            'category_id': quote.category_id,
        }
        return JsonResponse(obj)


class QuoteDeleteView(View):
    def post(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        quote.delete()
        obj = {'result': 'deleted'}
        return JsonResponse(obj)


class CategoryQuotesView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        data = []
        for quote in category.quotes.all():
            data.append({
                'id': quote.id,
                'text': quote.text,
                'category_id': quote.category_id,
            })
        obj = {
            'data': data
        }
        return JsonResponse(obj)


class CategoryCreateView(View):
    def post(self, request):
        category = Category.objects.create(name=request.POST.get('name'))
        obj = {
            'id': category.id,
            'name': category.name,
        }
        return JsonResponse(obj)


class CategoryUpdateView(View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.name = request.POST.get('name')
        category.save()
        obj = {
            'id': category.id,
            'name': category.name,
        }
        return JsonResponse(obj)


class CategoryDeleteView(View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        obj = {'result': 'deleted'}
        return JsonResponse(obj)


class TagQuotesView(View):
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        data = []
        for quote in tag.quotes.all():
            data.append({
                'id': quote.id,
                'text': quote.text,
                'category_id': quote.category_id,
            })
        obj = {
            'data': data
        }
        return JsonResponse(obj)


class TagCreateView(View):
    def post(self, request):
        tag = Tag.objects.create(name=request.POST.get('name'))
        obj = {
            'id': tag.id,
            'name': tag.name,
        }
        return JsonResponse(obj)


class TagUpdateView(View):
    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.name = request.POST.get('name')
        tag.save()
        obj = {
            'id': tag.id,
            'name': tag.name,
        }
        return JsonResponse(obj)


class TagDeleteView(View):
    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
        obj = {'result': 'deleted'}
        return JsonResponse(obj)


class QuoteTagsView(View):
    def get(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        obj = {
            'tags': list(quote.tags.values('id', 'name'))
        }
        return JsonResponse(obj)


class QuoteTagsSetView(View):
    def post(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        quote.tags.clear()
        obj = {
            'tags': list(quote.tags.values('id', 'name'))
        }
        return JsonResponse(obj)


class QuoteTagsAddView(View):
    def post(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        tag = get_object_or_404(Tag, pk=request.POST.get('tag_id'))
        quote.tags.add(tag)
        obj = {
            'tags': list(quote.tags.values('id', 'name'))
        }
        return JsonResponse(obj)


class QuoteTagsRemoveView(View):
    def post(self, request, pk, tag_id):
        quote = get_object_or_404(Quote, pk=pk)
        tag = get_object_or_404(Tag, pk=tag_id)
        quote.tags.remove(tag)
        obj = {'result': 'deleted'}
        return JsonResponse(obj)