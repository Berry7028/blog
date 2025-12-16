from django.contrib.auth import views as auth_views
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .views import SignupView, CustomLoginView

app_name = 'accounts'

# ログアウトビューをデコレートする
LogoutView = method_decorator(never_cache, name='dispatch')(auth_views.LogoutView)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
