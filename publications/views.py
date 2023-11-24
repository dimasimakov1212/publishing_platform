from django.shortcuts import render


def main_page_view(request):
    """
    Выводит главную страницу
    :return:
    """

    # blogs = Blog.objects.filter(blog_is_active=True)  # Получаем все опубликованные статьи

    context = {
        'title': 'Главная',
        'title_2': 'сервис создания рассылок',
    }
    return render(request, 'publications/homepage.html', context)
