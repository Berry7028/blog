from django.urls import path

from .views import CommentCreateView

app_name = 'comments'

urlpatterns = [
    path('<slug:post_slug>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
]

