from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number", "city"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='moderator_profile', verbose_name='Пользователь')
    can_edit_courses = models.BooleanField(default=True, verbose_name='Может редактировать курсы')
    can_edit_lessons = models.BooleanField(default=True, verbose_name='Может редактировать уроки')

    def __str__(self):
        return f"Модератор: {self.user.email}"

    class Meta:
        verbose_name = 'Модератор'
        verbose_name_plural = 'Модераторы'


class Payments(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("card", "Карта"),
        ("cache", "Наличные"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    payment_amount = models.IntegerField(default=0)
    payment_method = models.CharField(choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"{self.user} | {self.payment_amount}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["payment_date"]
