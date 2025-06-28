from django.db import models


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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title", "course"]
