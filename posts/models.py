from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from core.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('posts:category', kwargs={'slug': self.slug})


class Tag(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('posts:tag', kwargs={'slug': self.slug})


class PostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            status=Post.Status.PUBLISHED,
            published_at__isnull=False,
            published_at__lte=now,
        )


class Post(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', '下書き'
        PUBLISHED = 'published', '公開'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', '-published_at']),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base = slugify(self.title)
            candidate = base
            counter = 2
            while candidate and Post.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f'{base}-{counter}'
                counter += 1
            self.slug = candidate or self.slug
        if self.status == self.Status.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('posts:post_detail', kwargs={'slug': self.slug})
