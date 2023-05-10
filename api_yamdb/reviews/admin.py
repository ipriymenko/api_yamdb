from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


# Из-за того, что genre = models.ManyToManyField, поле нельзя зарегистрировать
# напрямую, только так
@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category', 'display_genre')

    def display_genre(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])
    display_genre.short_description = 'Жанры'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date',)
