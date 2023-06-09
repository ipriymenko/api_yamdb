from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

from users.models import User
from .validators import year_validator


class Title(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    description = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    year = models.PositiveSmallIntegerField(
        validators=(year_validator,),
        verbose_name='Год',
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField('Genre', through='GenreTitle')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.STR_TEXT_LIMIT]


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Ссылка на категорию'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)

    def __str__(self):
        return self.name[:settings.STR_TEXT_LIMIT]


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Жанр'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Ссылка на жанр'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('id',)

    def __str__(self):
        return self.name[:settings.STR_TEXT_LIMIT]


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title_id} - {self.genre_id}'


class Review(models.Model):
    MIN_SCORE = 1
    MAX_SCORE = 10

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        'Текст отзыва',
        help_text='Оставьте свой отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_SCORE, f'Минимальная оценка - {MIN_SCORE}'),
            MaxValueValidator(MAX_SCORE, f'Максимальная оценка - {MAX_SCORE}'),
        ],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_title_author'
            ),
        )

    def __str__(self):
        return self.text[:settings.STR_TEXT_LIMIT]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Оставьте свой комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:settings.STR_TEXT_LIMIT]
