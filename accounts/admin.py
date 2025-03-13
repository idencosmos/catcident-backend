from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_approved", "is_staff")
    list_filter = ("is_approved", "is_staff")
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_approved'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
