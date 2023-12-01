from random import sample

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from publications.forms import PublicationForm
from publications.models import Publication
from users.models import User


def main_page_view(request):
    """ Выводит главную страницу """

    users = User.objects.filter(is_superuser=False)  # Получаем список пользователей
    if len(users) >= 6:
        user_list = sample(list(users), 6)  # Получаем 6 случайных пользователя
    else:
        user_list = users

    context = {
        'title': 'Главная',
        'title_2': 'Сервис интересного контента',
        'user_list': user_list
    }

    return render(request, 'publications/homepage.html', context)


class PublicationListView(ListView):
    """ Выводит список публикаций пользователя """

    model = Publication
    template_name = 'publications/publications_list.html'

    def get_context_data(self, **kwargs):
        """ Выводит контекстную информацию в шаблон """

        context = super(PublicationListView, self).get_context_data(**kwargs)
        context['title'] = 'Публикации'
        context['title_2'] = 'Мои публикации'

        return context

    def get_queryset(self, *args, **kwargs):
        """ Выводит в список только публикации пользователя """

        queryset = super().get_queryset(*args, **kwargs)

        try:
            user = self.request.user

            queryset = queryset.filter(publication_owner=user)
            return queryset

        except TypeError:
            pass


class PublicationCreateView(CreateView):
    """ Выводит форму создания статьи """

    model = Publication
    form_class = PublicationForm

    success_url = reverse_lazy('publications:publications_list')

    def form_valid(self, form):
        """ Реализует сохранение формы создания публикации """

        user = self.request.user

        self.object = form.save(commit=False)
        self.object.publication_owner = user
        self.object.save()

        # if form.is_valid():
        #     new_publication = form.save()
        #     new_publication.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """ Выводит контекстную информацию в шаблон """

        context = super(PublicationCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Публикация'
        context['title_2'] = 'создание публикации'
        return context
