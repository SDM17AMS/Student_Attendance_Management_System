from django.db import models


class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=50,blank=True,null=False)
    class Meta:
        ordering = ['name', 'section']

    def __str__(self):
        if self.section:
            return f"{self.name} - {self.section}"
        return self.name