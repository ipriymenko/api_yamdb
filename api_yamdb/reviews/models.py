from django.db import models


class Title(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название')
    year = models.IntegerField()
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведение'
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Категория')
    slug = models.SlugField(
        unique=True,
        verbose_name='Ссылка на группу')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'
        ordering = ['id']


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Жанр')
    slug = models.SlugField(
        unique=True,
        verbose_name='Ссылка на жанр')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанр'
        ordering = ['id']


class Genre_title(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.PROTECT)
    genre_id = models.ForeignKey(Genre, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'
