from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView

from posts.models import Post

from .forms import CommentForm
from .models import Comment


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post.objects.published(), slug=kwargs['post_slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.post_obj
        self.object.save()
        messages.success(self.request, 'コメントを投稿しました。')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return f"{reverse('posts:post_detail', kwargs={'slug': self.post_obj.slug})}#comments"
