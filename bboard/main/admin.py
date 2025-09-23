from django.contrib import admin
import datetime

from .forms import SubRubricForm
from .models import AdvUser, SuperRubric, SubRubric, Bb, AdditionalImage, Comment
from .utilities import send_activation_notification


@admin.action(description="Отправить письма с требованиями активации")
def send_notifications(modeladmin, request, queryset):
    for user in queryset:
        if not user.is_active:
            send_activation_notification(request, user)
    modeladmin.message_user(request, "Письма с требованиями отправлены")


class NonactivatedFilter(admin.SimpleListFilter):
    title = "Прошли активацию?"
    parameter_name = "actstate"

    def lookups(self, request, model_admin):
        return (
            ("activated", "Прошли"),
            ("threedays", "Не прошли более 3 дней"),
            ("week", "Не прошли более недели"),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == "activated":
            return queryset.filter(is_active=True)
        elif val == "threedays":
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, date_joined__date__lt=d)
        elif val == "week":
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, date_joined__date__lt=d)


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_active", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = (NonactivatedFilter,)
    fields = (
        ("username", "email"),
        ("first_name", "last_name"),
        ("send_messages", "is_active"),
        ("is_staff", "is_superuser"),
        "groups",
        "user_permissions",
        ("last_login", "date_joined"),
    )
    readonly_fields = ("last_login", "date_joined")
    actions = (send_notifications,)


admin.site.register(AdvUser, AdvUserAdmin)


class SubRubricInline(admin.TabularInline):
    model = SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ("super_rubric",)
    inlines = (SubRubricInline,)


admin.site.register(SuperRubric, SuperRubricAdmin)


class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm


admin.site.register(SubRubric, SubRubricAdmin)


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


class BbAdmin(admin.ModelAdmin):
    list_display = (
        "rubric",
        "title",
        "content",
        "author",
        "created_at",
    )
    fields = (
        ("rubric", "author"),
        ("title", "price"),
        "content",
        "contacts",
        "image",
        "is_active",
    )
    inlines = (AdditionalImageInline,)


admin.site.register(Bb, BbAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "created_at", "is_active")
    list_display_links = ("author", "content")
    list_filter = ("is_active",)
    search_fields = (
        "author",
        "content",
    )
    date_hierarchy = "created_at"
    fields = ("author", "content", "is_active", "created_at")
    readonly_fields = ("created_at",)


admin.site.register(Comment, CommentAdmin)
