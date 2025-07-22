from django.db import models

from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название", help_text="Введите название курса")
    preview = models.ImageField(
        upload_to="previews/courses/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Добавьте изображение к курсу",
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True, help_text="Добавьте описание курса")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Владелец", help_text="Владелец курса"
    )
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название", help_text="Введите название урока")
    description = models.TextField(verbose_name="Описание", blank=True, null=True, help_text="Добавьте описание урока")
    preview = models.ImageField(
        upload_to="previews/lessons/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Добавьте изображение к уроку",
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео", blank=True, null=True, help_text="Добавьте ссылку на видео"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Курс")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Владелец", help_text="Владелец урока"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title", "course"]


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Курс: {self.course} | Пользователь: {self.user}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["course"]
