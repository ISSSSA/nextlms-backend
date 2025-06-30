from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    wallet_number = models.CharField(max_length=100, unique=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
