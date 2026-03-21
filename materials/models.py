from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    preview = models.ImageField(
        upload_to="migrations/course_previews",
        blank=True,
        null=True,
        verbose_name="Превью(картинка)",
        help_text="Загрузите превью(картинку)",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Опишите название курса",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    description = models.TextField(verbose_name="Описание", help_text="Опишите урок")
    preview = models.ImageField(
        upload_to="migrations/lesson_previews",
        blank=True,
        null=True,
        verbose_name="Превью(картинка)",
        help_text="Загрузите превью(картинку)",
    )
    video_link = models.URLField(
        verbose_name="Ссылка на видео", help_text="Добавьте ссылку"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
