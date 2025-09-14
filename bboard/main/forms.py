from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import AdvUser, SuperRubric, SubRubric


class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Адрес электронной почты")

    class Meta:
        model = AdvUser
        fields = ("username", "email", "first_name", "last_name", "send_messages")


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Адрес электронной почты")
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password_confirm = forms.CharField(
        label="Пароль (повторно)",
        widget=forms.PasswordInput,
        help_text="Введите тот же самый пароль еще раз для проверки",
    )

    def clean_password(self):
        password = self.cleaned_data["password"]
        password_validation.validate_password(password)
        return password

    def clean(self):
        super().clean()
        if "password" in self.cleaned_data:
            password = self.cleaned_data["password"]
            password_confirm = self.cleaned_data["password_confirm"]
            if password != password_confirm:
                raise ValidationError(
                    {"password_confirm": "Введенные пароли не совпадают"},
                    code="password_mismatch",
                )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False
        if commit:
            user.save()
        return user

    class Meta:
        model = AdvUser
        fields = (
            "username",
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "send_messages",
        )


class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(
        queryset=SuperRubric.objects.all(),
        empty_label=None,
        label="Надрубрика",
        required=True,
    )

    class Meta:
        model = SubRubric
        fields = "__all__"


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=40, label="")
