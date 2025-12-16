"""
ブログプロジェクトのURL設定。

`urlpatterns`リストはURLをビューにルーティングします。詳細については以下を参照してください：
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
例：
関数ベースのビュー
    1. インポートを追加します：from my_app import views
    2. urlpatternsに追加します：path('', views.home, name='home')
クラスベースのビュー
    1. インポートを追加します：from other_app.views import Home
    2. urlpatternsに追加します：path('', Home.as_view(), name='home')
別のURLconfをインクルード
    1. include()関数をインポートします：from django.urls import include, path
    2. urlpatternsに追加します：path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('comments.urls')),
    path('', include('posts.urls')),
]

# 開発環境でのメディアファイルの提供
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
