from django.urls import path

from .views import titles, categories, genres

urlpatterns = [
    path('titles/<int:titles_id>', titles, name='titles'),
    path('categories/<slug:slug>/', categories, name='categories'),
    path('genres/<slug:slug>/', genres, name='genres'),
]
