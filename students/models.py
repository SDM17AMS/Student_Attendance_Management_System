from django.db import models
from django.contrib.auth.models import User
from classrooms.models import ClassRoom

class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        null=True,
        blank=True
    )
    full_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )

    def save(self, *args, **kwargs):
        if not self.student_id:
            last_student = Student.objects.order_by('-id').first()
            if last_student and last_student.student_id:
                prefix = "STU"
                try:
                    last_num = int(last_student.student_id.replace(prefix, ''))
                    new_num = last_num + 1
                except ValueError:
                    new_num = 1
            else:
                new_num = 1
            self.student_id = f"STU{new_num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"