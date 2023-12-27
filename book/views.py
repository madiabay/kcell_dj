from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # for registration and login
from django.contrib.auth.views import LoginView # for login
from django.contrib.auth import logout, login # for logout and login

#class
from django.views.generic import ListView, DetailView, CreateView

from .models import Books, Category
from .forms import AddPostForm
from .utils import *


# Create your views here.
class BooksHome(DataMixin, ListView):
    model = Books
    template_name = 'books/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cats_def = self.get_user_context(title="Madi's site")
        return dict(list(context.items()) + list(cats_def.items()))

    def get_queryset(self):
        return Books.objects.filter(is_published=True)


def about(request):
    contact_list = Books.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'books/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cats_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(cats_def.items()))


def contact(request):
    favourites = Books.objects.filter(is_favourite=True)
    return HttpResponse('contact')


class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'books/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cats_def = self.get_user_context(title='Registration')
        return dict(list(context.items()) + list(cats_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(to='home')


class LoginUser(DataMixin, LoginView):

    form_class = AuthenticationForm
    template_name = 'books/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cats_def = self.get_user_context(title='Login')
        return dict(list(context.items()) + list(cats_def.items()))


def logout_user(request):
    logout(request)
    return redirect(to='login')


class ShowPost(DataMixin, DetailView):
    model = Books
    template_name = 'books/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cats_def = self.get_user_context(title='Пост - ' + str(context['post']))
        return dict(list(context.items()) + list(cats_def.items()))


class BooksCategory(DataMixin, ListView):
    model = Books
    template_name = 'books/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cats_def = self.get_user_context(
            title='Категория - ' + str(context['posts'][0].cat),
            cat_selected=context['posts'][0].cat_id
        )
        return dict(list(context.items()) + list(cats_def.items()))

    def get_queryset(self):
        return Books.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


def pageNotFound(request, exception):
    return HttpResponseNotFound('Not found ------------------------')
