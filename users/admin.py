from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "last_login",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
    )
    search_fields = ("username", "email")
