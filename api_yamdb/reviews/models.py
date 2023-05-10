from django.db import models


class Title(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    year = models.IntegerField()
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField('Genre', through='GenreTitle')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Ссылка на группу'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['id']


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'
