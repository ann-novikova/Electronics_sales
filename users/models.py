from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    """Кастомный менеджер для модели User с email вместо username"""

    def create_user(self, email, password=None, **extra_fields):
        """Создает и возвращает пользователя с email и паролем"""
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и возвращает суперпользователя"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Кастомная модель пользователя, заменяющая стандартную модель.

    Вместо поля `username` используется `email` как уникальный идентификатор
    для аутентификации. Позволяет хранить дополнительную информацию о пользователе:
    телефон, город, аватар.

    email (EmailField): Уникальный адрес электронной почты. Используется для входа.
    phone (CharField): Номер телефона пользователя. Максимум 15 символов.
    city (CharField): Город проживания пользователя. Максимум 50 символов.
    avatar (ImageField): Аватар пользователя. Загружается в папку 'users/avatar'.
    """

    username = None
    objects = UserManager()

    email = models.EmailField(
        unique=True,
        verbose_name="Почта",
        help_text="Введите почту",
        blank=False,
        null=False,
    )
    phone = models.CharField(
        max_length=15, verbose_name="Телефон", help_text="Введите номер телефона"
    )
    city = models.CharField(max_length=50, verbose_name="Город")
    avatar = models.ImageField(upload_to="users/avatar", verbose_name="Аватар")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """
        Определяет человекочитаемое имя модели и его множественную форму
        для отображения в интерфейсе администратора.
        """

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"