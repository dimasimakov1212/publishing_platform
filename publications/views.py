from random import sample

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from publications.forms import PublicationForm
from publications.models import Publication
from users.models import User


def main_page_view(request):
    """ Выводит главную страницу и 6 случайных пользователей"""

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


def other_users_page_view(request):
    """ Выводит список публикаций всех пользователей, кроме текущего """

    user = request.user  # получаем текущего пользователя

    # Получаем список пользователей кроме суперпользователя и текущего пользователя
    user_list = User.objects.filter(is_superuser=False).exclude(id=user.pk)

    context = {
        'title': 'Пользователи',
        'title_2': 'публикации пользователей',
        'user_list': user_list
    }

    return render(request, 'publications/homepage.html', context)


class UserPublicationListView(ListView):
    """ Выводит список публикаций текущего пользователя """

    model = Publication
    template_name = 'publications/publications_list.html'

    def get_context_data(self, **kwargs):
        """ Выводит контекстную информацию в шаблон """

        context = super(UserPublicationListView, self).get_context_data(**kwargs)
        context['title'] = 'Публикации'
        context['title_2'] = 'Мои публикации'
        context['author'] = self.request.user.first_name  # передаем в контекст имя владельца публикации

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

    success_url = reverse_lazy('publications:user_publications_list')

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


class PublicationDetailView(DetailView):
    """ Выводит информаццию о статье """

    model = Publication

    def get_context_data(self, **kwargs):
        """ Выводит контекстную информацию в шаблон """

        context = super(PublicationDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Просмотр'
        context['title_2'] = 'Просмотр публикации'
        return context


class PublicationUpdateView(UpdateView):
    """ Выводит форму редактирования статьи """

    model = Publication
    form_class = PublicationForm
    success_url = reverse_lazy('publications:home')

    def form_valid(self, form):
        """ Реализует сохранение формы редактирования публикации """

        if form.is_valid():
            new_article = form.save()
            new_article.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """ Выводит контекстную информацию в шаблон """

        context = super(PublicationUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Редактирование'
        context['title_2'] = 'Редактирование публикации'
        return context


class PublicationDeleteView(DeleteView):
    """ Выводит форму удаления статьи """

    model = Publication
    success_url = reverse_lazy('publications:publications_list')

    def get_context_data(self, **kwargs):
        """ Выводит контекстную информацию в шаблон """

        context = super(PublicationDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Удаление'
        context['title_2'] = 'Удаление публикации'
        return context


class OtherUserPublicationListView(ListView):
    """ Выводит список публикаций выбранного пользователя """

    model = Publication
    template_name = 'publications/publications_list.html'

    def get_context_data(self, **kwargs):
        """ Выводит контекстную информацию в шаблон """

        user = User.objects.get(id=self.kwargs['pk'])  # получаем пользователя автора публикации

        context = super(OtherUserPublicationListView, self).get_context_data(**kwargs)
        context['title'] = 'Публикации'
        context['title_2'] = 'публикации пользователя'
        context['author'] = user.first_name  # передаем в контекст имя владельца публикации

        return context

    def get_queryset(self, *args, **kwargs):
        """ Выводит в список только публикации определенного пользователя """

        queryset = super().get_queryset(*args, **kwargs)

        try:
            user = self.kwargs['pk']

            queryset = queryset.filter(publication_owner=user)
            return queryset

        except TypeError:
            pass


def user_subscriptions_view(request):
    """ Выводит список публикаций, на которые подписан пользователь """

    user = request.user  # получаем текущего пользователя

    # Получаем список публикаций, на которые подписан текущий пользователь
    subscriptions_list = user.user_subscriptions.all()

    context = {
        'title': 'Публикации',
        'title_2': 'мои подписки',
        'object_list': subscriptions_list
    }

    return render(request, 'publications/publications_list.html', context)
