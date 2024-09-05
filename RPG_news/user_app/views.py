from django.contrib.auth.views import LoginView
from .forms import LoginForm, RegistrationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from .tasks import activate_email_task
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render



class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'user_app/login.html'
    extra_context = {'title': 'Авторизация на сайте'}

class CustomRegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'user_app/signup.html'
    extra_context = {'title': 'Регистрация на сайте'}

    def get_success_url(self):
        return reverse_lazy("user_app:signup_done")

    def form_valid(self, form):
        user: User = form.save()
        user.is_active = False
        user.save()
        activate_email_task(user)
        return HttpResponseRedirect(self.get_success_url())

class CustomRegistrationDoneView(TemplateView):
    template_name = "user_app/signup_done.html"
    extra_context = {"title": "Регистрация завершена, активируйте учётную запись."}

class CustomRegistrationConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(
                request,
                "user_app/signup_confirmed.html",
                {"title": "Учётная запись активирована."},
            )
        else:
            return render(
                request,
                "user_app/signup_not_confirmed.html",
                {"title": "Ошибка активации учётной записи."},
            )
