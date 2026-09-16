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


class QuoteDetailView(View):
    def get(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        return JsonResponse({
            'id': quote.id,
            'text': quote.text,
            'category_id': quote.category_id,
            'tags': list(quote.tags.values('id', 'name')),
        })


class QuoteRandomView(View):
    def get(self, request):
        quote = Quote.objects.order_by('?').first()
        return JsonResponse({
            'id': quote.id,
            'text': quote.text,
            'category_id': quote.category_id,
            'tags': list(quote.tags.values('id', 'name')),
        })


class QuoteCreateView(CsrfExemptView):
    def post(self, request):
        form = QuoteCreateForm(parse_body(request))
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        quote = form.save()
        
        return JsonResponse({
            'id': quote.id,
            'text': quote.text,
            'category_id': quote.category_id,
        })


class QuoteUpdateView(CsrfExemptView):
    def post(self, request, pk):
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


class QuoteDeleteView(CsrfExemptView):
    def post(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        quote.delete()
        return JsonResponse({'result': 'deleted'})


class CategoryQuotesView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        data = [{
            'id': q.id,
            'text': q.text,
            'category_id': q.category_id,
        } for q in category.quotes.all()]
        return JsonResponse({'data': data})



class CategoryCreateView(CsrfExemptView):
    def post(self, request):
        form = CategoryCreateForm(parse_body(request))
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        category = form.save()
        return JsonResponse({'id': category.id, 'name': category.name})


class CategoryUpdateView(CsrfExemptView):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryUpdateForm(parse_body(request), instance=category)
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        category = form.save()
        return JsonResponse({'id': category.id, 'name': category.name})


class CategoryDeleteView(CsrfExemptView):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return JsonResponse({'result': 'deleted'})




class TagQuotesView(View):
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        data = [{
            'id': q.id,
            'text': q.text,
            'category_id': q.category_id,
        } for q in tag.quotes.all()]
        return JsonResponse({'data': data})


class TagCreateView(CsrfExemptView):
    def post(self, request):
        form = TagCreateForm(parse_body(request))
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        tag = form.save()
        return JsonResponse({'id': tag.id, 'name': tag.name})


class TagUpdateView(CsrfExemptView):
    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        form = TagUpdateForm(parse_body(request), instance=tag)
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        tag = form.save()
        return JsonResponse({'id': tag.id, 'name': tag.name})


class TagDeleteView(CsrfExemptView):
    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
        return JsonResponse({'result': 'deleted'})




class QuoteTagsView(View):
    def get(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        return JsonResponse({'tags': list(quote.tags.values('id', 'name'))})


class QuoteTagsSetView(CsrfExemptView):
    def post(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        quote.tags.clear()
        return JsonResponse({'tags': list(quote.tags.values('id', 'name'))})


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
    def post(self, request, pk, tag_id):
        quote = get_object_or_404(Quote, pk=pk)
        tag = get_object_or_404(Tag, pk=tag_id)
        quote.tags.remove(tag)
        return JsonResponse({'result': 'deleted'})