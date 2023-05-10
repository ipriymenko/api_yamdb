from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


admin.side.register(Title)
admin.side.register(Category)
admin.side.register(Genre)
admin.side.register(Review)
admin.side.register(Comment)
