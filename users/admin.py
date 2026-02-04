from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdminModel(admin.ModelAdmin):
    """Регистрация модели пользователя в админ панели"""

    list_display = ("id", "email")
