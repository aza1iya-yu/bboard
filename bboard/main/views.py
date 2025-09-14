from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.signing import BadSignature
from django.contrib.auth import logout

from .models import AdvUser
from .forms import ProfileEditForm, RegisterForm
from .signals import post_register
from .utilities import signer


def index(request):
    return render(request, "main/index.html")


def other_page(request, page):
    try:
        template = get_template(f"main/{page}.html")
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class BBLoginView(LoginView):
    template_name = "main/login.html"


@login_required
def profile(request):
    return render(request, "main/profile.html")


class BBLogoutView(LogoutView):
    pass


class ProfileEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = "main/profile_edit.html"
    form_class = ProfileEditForm
    success_url = reverse_lazy("main:profile")
    success_message = "Данные посетителя изменены"

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class PasswordEditView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = "main/password_edit.html"
    success_url = reverse_lazy("main:profile")
    success_message = "Пароль посетителя изменен"


class RegisterView(CreateView):
    model = AdvUser
    template_name = "main/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("main:register_done")

    def form_valid(self, form):
        result = super().form_valid(form)
        post_register.send(RegisterForm, request=self.request, user=self.object)
        return result


class RegisterDoneView(TemplateView):
    template_name = "main/register_done.html"


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, "main/activation_failed.html")
    user = get_object_or_404(AdvUser, username=username)
    if user.is_active:
        template = "main/activation_done_earlier.html"
    else:
        template = "main/activation_done.html"
        user.is_active = True
        user.save()
    return render(request, template)


class ProfileDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = "main/profile_delete.html"
    success_url = reverse_lazy("main:index")
    success_message = "Посетитель удален"

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class BBPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = "main/password_reset.html"
    subject_template_name = "emails/reset_letter_subject.txt"
    email_template_name = "emails/reset_letter_body.txt"
    success_url = reverse_lazy("main:index")
    success_message = "Письмо с гиперссылкой на страницу сброса пароля отправлено"


class BBPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = "main/password_reset_confirm.html"
    success_url = reverse_lazy("main:index")
    success_message = "Новый пароль сохранен"


def rubric_bbs(request, pk):
    pass
