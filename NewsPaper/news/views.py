from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from .models import Post, Category, Subscriber
from .filters import NewsFilter
from django.urls import reverse_lazy
from .forms import NewsForm, ArticlesForm
from .resources import news, article

# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class NewsSearch(ListView):
    model = Post
    ordering = '-date'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsPostList(ListView):
    model = Post
    ordring = '-date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(content='NE')

class ArticlePostList(ListView):
    model = Post
    ordring = '-date'
    template_name = 'article_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(content='AR')

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.content = news
        return super().form_valid(form)

class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = ArticlesForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.content = article
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

@login_required
@csrf_protect
def subscription(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user = request.user, category = category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user = request.user,
                category = category,
            ).delete()
    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed = Exists(
            Subscriber.objects.filter(
                user = request.user,
                category = OuterRef('pk'),
            )
        )
    )
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions}
    )