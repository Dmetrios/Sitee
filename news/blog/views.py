from turtle import title
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout


from blog.models import *
from blog.forms import AddPostForm, RegisterUserForm, LoginUserForm
from blog.utils import DataMixin

menu = [{'title': 'О сайте', 'url_name': 'about'},
{'title': 'Добавить статью', 'url_name': 'add_page'},
{'title': 'Обратная свзяь', 'url_name': 'contact'},
]


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = "Регистрация")
        return dict(list(context.items())+list(c_def.items()))

class LoginUser(DataMixin, LoginView):
    from_class = LoginUserForm
    template_name = 'blog/login.html'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self):
        return reverse_lazy('home')


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'blog/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        context['menu'] = menu
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ShowPost(DataMixin, DetailView):
    model = Post
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['posts'])
        return dict(list(context.items()) + list(c_def.items()))

class PostUpdate(UpdateView):
    model = Post
    template_name = 'blog/addpage.html'
    slug_url_kwarg = 'post_slug'
    form_class = AddPostForm

class PostDelete(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    slug_url_kwarg = 'post_slug'
    success_url = reverse_lazy('home')

class PostCategory(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context


class BlogHome(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published = True).order_by('-time_create')

def about(request):
    context ={
        'menu': menu,
        'title': 'Информация о Сайте',
    }
    return render(request, 'blog/about.html', context= context)

def categories(request, cat):
    if(request.GET):
        print(request.GET)
    return HttpResponse(f"<h1>Statya Dimi</h1><p>{cat}</p>")

def archive(request, year):
    if int(year) > 2022:
        return redirect('home', permanent=True)
    else:
        return HttpResponse(f"<h1>Archive on year</h1><p>{year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def logout_user(request):
    logout(request)
    return redirect('login')

def contact(request):
    context ={
        'menu': menu,
        'title': 'Контакты связи',
    }
    return render(request, 'blog/contact.html', context= context)

    
    
# def show_category(request, cat_id):
#     posts = Post.objects.filter(cat_id = cat_id)

#     context ={
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_id,
#     }


#     return render(request, 'blog/index.html', context= context)


    #def index(request):
    #posts = Post.objects.all()

    #context ={
        #'posts': posts,
        #'menu': menu,
       # 'title': 'Главная страница',
       # 'cat_selected': 0,
   # }
   # return render(request, 'blog/index.html', context= context)
   # 
   # 
# def show_post(request, post_slug):
#     post = get_object_or_404(Post, slug = post_slug)

#     context ={
#         'posts': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'blog/post.html', context= context)# 
# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)

#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else: 
#         form = AddPostForm()
#     return render(request, 'blog/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

