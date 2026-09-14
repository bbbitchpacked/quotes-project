from django.urls import path
from . import views

urlpatterns = [
    path('quotes/random', views.QuoteRandomView.as_view()),
    path('quotes', views.QuoteCreateView.as_view()),
    path('quotes/<int:pk>', views.QuoteDetailView.as_view()),
    path('quotes/<int:pk>/update', views.QuoteUpdateView.as_view()),
    path('quotes/<int:pk>/delete', views.QuoteDeleteView.as_view()),

    path('categories', views.CategoryCreateView.as_view()),
    path('categories/<int:pk>/quotes', views.CategoryQuotesView.as_view()),
    path('categories/<int:pk>/update', views.CategoryUpdateView.as_view()),
    path('categories/<int:pk>/delete', views.CategoryDeleteView.as_view()),

    path('tags', views.TagCreateView.as_view()),
    path('tags/<int:pk>/quotes', views.TagQuotesView.as_view()),
    path('tags/<int:pk>/update', views.TagUpdateView.as_view()),
    path('tags/<int:pk>/delete', views.TagDeleteView.as_view()),

    path('quotes/<int:pk>/tags', views.QuoteTagsSetView.as_view()),
    path('quotes/<int:pk>/tags/add', views.QuoteTagsAddView.as_view()),
    path('quotes/<int:pk>/tags/<int:tag_id>', views.QuoteTagsRemoveView.as_view()),
]