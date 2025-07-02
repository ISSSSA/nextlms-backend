from django.db import models
from django.db.models import JSONField
from django.contrib.auth import get_user_model

User = get_user_model()

class XAPIStatement(models.Model):
    statement_id = models.UUIDField(unique=True)
    actor = JSONField()
    verb = JSONField()
    object = JSONField()
    result = JSONField(null=True, blank=True)
    context = JSONField(null=True, blank=True)
    timestamp = models.DateTimeField()
    stored = models.DateTimeField(auto_now_add=True)
    authority = JSONField(null=True, blank=True)
    version = models.CharField(max_length=10)

    class Meta:
        verbose_name = "xAPI Statement"
        verbose_name_plural = "xAPI Statements"
        ordering = ['-stored']

    def __str__(self):
        return f"xAPI Statement {self.statement_id}"
