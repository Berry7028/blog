from django.db import models

from core.models import TimeStampedModel


class CommentQuerySet(models.QuerySet):
    def public(self):
        return self.filter(is_public=True)


class Comment(TimeStampedModel):
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    is_public = models.BooleanField(default=True, db_index=True)

    objects = CommentQuerySet.as_manager()

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'is_public', 'created_at']),
        ]

    def __str__(self) -> str:
        return f'{self.name}: {self.body[:20]}'
