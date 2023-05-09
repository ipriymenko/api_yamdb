from django.http import HttpResponse


def titles(request, titles_id):
    return HttpResponse(f"Главная страница приложения reviews "
                        f"произведения по номеру категории {titles_id}")


def categories(request, slug):
    return HttpResponse(
        f"<h1>Страница отображения по категориям</h1><p>{slug}</p>")


def genres(request, slug):
    return HttpResponse(
        f"<h1>Страница отображения по жанрам</h1><p>{slug}</p>")
