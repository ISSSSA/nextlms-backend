from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class CourseContent(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='contents'
    )
    page = models.IntegerField()
    text = models.TextField()

    class Meta:
        verbose_name = 'Содержание курса'
        verbose_name_plural = 'Содержания курсов'
        ordering = ['page']

    def __str__(self):
        return f"Страница {self.page} курса {self.course.title}"


class CourseHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Используем AUTH_USER_MODEL вместо прямой ссылки
        on_delete=models.CASCADE,
        related_name='course_histories'
    )
    course_content = models.ForeignKey(
        'CourseContent',
        on_delete=models.CASCADE,
        related_name='course_histories'
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'История курса'
        verbose_name_plural = 'Истории курсов'
        unique_together = [['user', 'course_content']]

    def __str__(self):
        return f"{self.user} - {self.course_content}"
