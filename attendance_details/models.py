# models.py
from django.db import models


class AttendanceDetail(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    attendance = models.ForeignKey(
        'attendances.Attendance',
        on_delete=models.CASCADE,
        related_name='details'
    )
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='present'
    )

    class Meta:
        unique_together = ['attendance', 'student']

    def __str__(self):
        return f"{self.student} — {self.get_status_display()}"