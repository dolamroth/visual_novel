from django.urls import path


from .translations_list import TranslationListView, TranslationListNestedView

urlpatterns = [
    path(r'all-nested', TranslationListNestedView.as_view()),
    path(r'all', TranslationListView.as_view()),
]
