from django import forms
from django.utils.text import slugify

from .models import Category, Post, Tag


class PostForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100,
        required=False,
        label='新しいカテゴリ',
        help_text='既存のカテゴリがない場合は、ここに新しいカテゴリ名を入力してください。',
        widget=forms.TextInput(attrs={'placeholder': '例: 技術記事'})
    )
    new_tags = forms.CharField(
        max_length=200,
        required=False,
        label='新しいタグ',
        help_text='カンマ区切りで複数のタグを追加できます。例: Python, Django, チュートリアル',
        widget=forms.TextInput(attrs={'placeholder': '例: Python, Django, チュートリアル'})
    )

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

    def clean_new_category(self):
        new_category = (self.cleaned_data.get('new_category') or '').strip()
        if new_category:
            # 既に存在するカテゴリかチェック
            if Category.objects.filter(name__iexact=new_category).exists():
                raise forms.ValidationError('このカテゴリは既に存在します。')
        return new_category

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')
        
        # カテゴリと新しいカテゴリの両方が指定されている場合はエラー
        if category and new_category:
            raise forms.ValidationError({
                'new_category': '既存のカテゴリを選択している場合は、新しいカテゴリを入力できません。'
            })
        
        # カテゴリが選択されていない場合、新しいカテゴリは必須ではない（blank=Trueのため）
        return cleaned_data

