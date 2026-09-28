import json

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Category, Tag, Quote
from .forms import (
    QuoteCreateForm, QuoteUpdateForm,
    CategoryCreateForm, CategoryUpdateForm,
    TagCreateForm, TagUpdateForm,
    QuoteTagsAddForm,
)


def parse_body(request):
    if request.content_type == 'application/json':
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            return {}
    return request.POST


@method_decorator(csrf_exempt, name='dispatch')
class CsrfExemptView(View):
    pass


class QuoteRandomView(View):
    def get(self, request):
        quote = Quote.objects.order_by('?').first()
        if quote is None:
            return JsonResponse({'error': 'No quotes found'}, status=404)
        return JsonResponse({
            'id': quote.id,
            'text': quote.text,
            'category_id': quote.category_id,
            'tags': list(quote.tags.values('id', 'name')),
        })


class QuoteListView(CsrfExemptView):
    def get(self, request):
        data = [{
            'id': q.id,
            'text': q.text,
            'category_id': q.category_id,
            'tags': list(q.tags.values('id', 'name')),
        } for q in Quote.objects.all()]
        return JsonResponse({'data': data})

    def post(self, request):
        form = QuoteCreateForm(parse_body(request))
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        quote = form.save()
        return JsonResponse({
            'id': quote.id,
            'text': quote.text,
            'category_id': quote.category_id,
        }, status=201)


class QuoteDetailView(CsrfExemptView):
    def get(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        return JsonResponse({
            'id': quote.id,
            'text': quote.text,
            'category_id': quote.category_id,
            'tags': list(quote.tags.values('id', 'name')),
        })

    def put(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        form = QuoteUpdateForm(parse_body(request), instance=quote)
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        quote = form.save()
        return JsonResponse({
            'id': quote.id,
            'text': quote.text,
            'category_id': quote.category_id,
        })

    def patch(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        data = parse_body(request)
        if 'text' in data:
            quote.text = data['text']
        if 'category_id' in data:
            quote.category_id = data['category_id']
        quote.save()
        return JsonResponse({
            'id': quote.id,
            'text': quote.text,
            'category_id': quote.category_id,
        })

    def delete(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        quote.delete()
        return JsonResponse({'result': 'deleted'}, status=204)


class CategoryQuotesView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        data = [{
            'id': q.id,
            'text': q.text,
            'category_id': q.category_id,
        } for q in category.quotes.all()]
        return JsonResponse({'data': data})


class CategoryListView(CsrfExemptView):
    def get(self, request):
        data = [{'id': c.id, 'name': c.name} for c in Category.objects.all()]
        return JsonResponse({'data': data})

    def post(self, request):
        form = CategoryCreateForm(parse_body(request))
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        category = form.save()
        return JsonResponse({'id': category.id, 'name': category.name}, status=201)


class CategoryDetailView(CsrfExemptView):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        return JsonResponse({'id': category.id, 'name': category.name})

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryUpdateForm(parse_body(request), instance=category)
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        category = form.save()
        return JsonResponse({'id': category.id, 'name': category.name})

    def patch(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        data = parse_body(request)
        if 'name' in data:
            category.name = data['name']
            category.save()
        return JsonResponse({'id': category.id, 'name': category.name})

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return JsonResponse({'result': 'deleted'}, status=204)


class TagQuotesView(View):
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        data = [{
            'id': q.id,
            'text': q.text,
            'category_id': q.category_id,
        } for q in tag.quotes.all()]
        return JsonResponse({'data': data})


class TagListView(CsrfExemptView):
    def get(self, request):
        data = [{'id': t.id, 'name': t.name} for t in Tag.objects.all()]
        return JsonResponse({'data': data})

    def post(self, request):
        form = TagCreateForm(parse_body(request))
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        tag = form.save()
        return JsonResponse({'id': tag.id, 'name': tag.name}, status=201)


class TagDetailView(CsrfExemptView):
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        return JsonResponse({'id': tag.id, 'name': tag.name})

    def put(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        form = TagUpdateForm(parse_body(request), instance=tag)
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        tag = form.save()
        return JsonResponse({'id': tag.id, 'name': tag.name})

    def patch(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        data = parse_body(request)
        if 'name' in data:
            tag.name = data['name']
            tag.save()
        return JsonResponse({'id': tag.id, 'name': tag.name})

    def delete(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
        return JsonResponse({'result': 'deleted'}, status=204)


class QuoteTagsView(CsrfExemptView):
    def get(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        return JsonResponse({'tags': list(quote.tags.values('id', 'name'))})

    def put(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        data = parse_body(request)
        tag_ids = data.get('tag_ids', [])
        tags = Tag.objects.filter(id__in=tag_ids)
        quote.tags.set(tags)
        return JsonResponse({'tags': list(quote.tags.values('id', 'name'))})

    def delete(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        quote.tags.clear()
        return JsonResponse({'tags': []})


class QuoteTagsAddView(CsrfExemptView):
    def post(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        form = QuoteTagsAddForm(parse_body(request))
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        tag = get_object_or_404(Tag, pk=form.cleaned_data['tag_id'])
        quote.tags.add(tag)
        return JsonResponse({'tags': list(quote.tags.values('id', 'name'))})


class QuoteTagsRemoveView(CsrfExemptView):
    def delete(self, request, pk, tag_id):
        quote = get_object_or_404(Quote, pk=pk)
        tag = get_object_or_404(Tag, pk=tag_id)
        quote.tags.remove(tag)
        return JsonResponse({'result': 'deleted'}, status=204)