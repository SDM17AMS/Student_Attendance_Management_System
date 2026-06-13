from django.db import models


class Teacher(models.Model):

    full_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.full_name
