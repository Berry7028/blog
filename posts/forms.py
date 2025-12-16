from django import forms
from django.utils.text import slugify

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'category', 'tags', 'excerpt', 'body', 'status')
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 3}),
            'body': forms.Textarea(attrs={'rows': 12}),
        }

    def clean_slug(self):
        slug = (self.cleaned_data.get('slug') or '').strip()
        title = (self.cleaned_data.get('title') or '').strip()
        if not slug and title:
            slug = slugify(title)
        return slug

