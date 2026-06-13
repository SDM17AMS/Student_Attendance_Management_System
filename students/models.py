from django.db import models
from classrooms.models import ClassRoom  # Import the model we reference


class Student(models.Model):

    full_name = models.CharField(max_length=100)

    student_id = models.CharField(max_length=50,unique=True)

    classroom = models.ForeignKey(ClassRoom,on_delete=models.SET_NULL,null=True,blank=True,related_name='students')


    def __str__(self):
        return f"{self.full_name} {self.student_id} {self.classroom.name if self.classroom else 'No Class'}"