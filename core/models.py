from django.db import models
from django.contrib.auth.models import User


class AuditMix(models.Model):
    created_by = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True