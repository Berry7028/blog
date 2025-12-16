from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from comments.forms import CommentForm

from .forms import PostForm
from .models import Category, Post, Tag


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return (
            Post.objects.published()
            .select_related('author', 'category')
            .prefetch_related('tags')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return (
            Post.objects.published()
            .select_related('author', 'category')
            .prefetch_related('tags')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.public()
        context['form'] = CommentForm()
        return context


class CategoryPostListView(PostListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return queryset.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_category'] = self.category
        return context


class TagPostListView(PostListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return queryset.filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tag'] = self.tag
        return context


class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        post = self.get_object()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return True
        return post.author_id == self.request.user.id


class MyPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/manage/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        return (
            Post.objects.filter(author=self.request.user)
            .select_related('category')
            .prefetch_related('tags')
            .order_by('-updated_at')
        )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/manage/post_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        form.save_m2m()
        messages.success(self.request, '投稿を作成しました。')
        return redirect('posts:manage_post_list')


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/manage/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '投稿を更新しました。')
        return response

    def get_success_url(self):
        return reverse('posts:manage_post_list')


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/manage/post_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        messages.success(self.request, '投稿を削除しました。')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:manage_post_list')
