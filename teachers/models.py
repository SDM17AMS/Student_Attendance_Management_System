from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        null=True,
        blank=True
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subjects = models.ManyToManyField(
        'subjects.Subject',
        related_name='teachers',
        blank=True
    )

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name