from django.contrib import admin
from django.utils.html import format_html
from .models import UserCustom


class UserCustomAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "last_name",
        "first_name",
        "email",
        "username",
        "avatar_tag",
    )
    list_filter = ("first_name",)
    search_fields = ("first_name", "email", "username")
    ordering = ("first_name",)

    def avatar_tag(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 50px; height:50px;" />'.format(
                    obj.avatar.url
                )
            )
        return "-"

    avatar_tag.short_description = "Avatar"


# Register your models here.
admin.site.register(UserCustom, UserCustomAdmin)
