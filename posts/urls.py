from django.urls import path

from .views import (
    CategoryPostListView,
    MyPostListView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    TagPostListView,
)

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('manage/', MyPostListView.as_view(), name='manage_post_list'),
    path('manage/new/', PostCreateView.as_view(), name='post_create'),
    path('manage/<slug:slug>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('manage/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('category/<slug:slug>/', CategoryPostListView.as_view(), name='category'),
    path('tag/<slug:slug>/', TagPostListView.as_view(), name='tag'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
