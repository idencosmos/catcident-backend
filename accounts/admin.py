from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_approved", "is_superuser")
    list_filter = ("is_approved", "is_superuser")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "is_approved")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
