# models.py
from django.db import models


class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    # Many-to-many: one teacher can teach multiple subjects
    subjects = models.ManyToManyField(
        'subjects.Subject',
        related_name='teachers',
        blank=True
    )

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name