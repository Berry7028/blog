from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic.edit import CreateView

from .forms import SignupForm


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:post_list')


@method_decorator(never_cache, name='dispatch')
class CustomLoginView(auth_views.LoginView):
    """キャッシュを無効にするカスタムログインビュー"""
    pass

