from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="e-mail", help_text="Введите e-mail")
    first_name = models.CharField(max_length=50, verbose_name="Имя", help_text="Введите имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", help_text="Введите фамилию")
    phone_number = models.CharField(max_length=50, verbose_name="Номер телефона", help_text="Введите телефон")
    city = models.CharField(max_length=50, verbose_name="Город", help_text="Ваш город")
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True, verbose_name="Аватар", help_text="Загрузите аватар"
    )
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True, help_text="Последний вход")
    is_active = models.BooleanField(default=True, blank=True, null=True, help_text="Статус УЗ")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number", "city"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("card", "Карта"),
        ("cache", "Наличные"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey("lms.Course", on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey("lms.Lesson", on_delete=models.CASCADE, null=True, blank=True)
    payment_amount = models.IntegerField(default=0)
    payment_method = models.CharField(choices=PAYMENT_METHOD_CHOICES)
    link = models.URLField(
        max_length=255, null=True, blank=True, verbose_name="Ссылка на оплату", help_text="Укажите ссылку на оплату"
    )
    session_id = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="ID сессии", help_text="Укажите ID сессии"
    )

    def __str__(self):
        return f"{self.user} | {self.payment_amount}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["payment_date"]
