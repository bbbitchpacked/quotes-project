from django.urls import path
from . import views

urlpatterns = [
    path('quotes/random', views.QuoteRandomView.as_view()),
    path('quotes', views.QuoteListView.as_view()),
    path('quotes/<int:pk>', views.QuoteDetailView.as_view()),

    path('categories', views.CategoryListView.as_view()),
    path('categories/<int:pk>', views.CategoryDetailView.as_view()),
    path('categories/<int:pk>/quotes', views.CategoryQuotesView.as_view()),

    path('tags', views.TagListView.as_view()),
    path('tags/<int:pk>', views.TagDetailView.as_view()),
    path('tags/<int:pk>/quotes', views.TagQuotesView.as_view()),

    path('quotes/<int:pk>/tags', views.QuoteTagsView.as_view()),
    path('quotes/<int:pk>/tags/add', views.QuoteTagsAddView.as_view()),
    path('quotes/<int:pk>/tags/<int:tag_id>', views.QuoteTagsRemoveView.as_view()),
]