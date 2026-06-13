# models.py
from django.db import models


class Attendance(models.Model):
    classroom = models.ForeignKey(
        'classrooms.ClassRoom',
        on_delete=models.PROTECT
    )
    subject = models.ForeignKey(
        'subjects.Subject',
        on_delete=models.PROTECT
    )
    teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=models.PROTECT
    )
    date = models.DateField()

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['classroom', 'subject', 'teacher', 'date'],
                name='unique_attendance_session'
            )
        ]

    class Meta:
        ordering = ['-date']
        # Prevent duplicate sessions
        constraints = [
            models.UniqueConstraint(
                fields=['classroom', 'subject', 'teacher', 'date'],
                name='unique_attendance_session'
            )
        ]

    def __str__(self):
        return f"{self.classroom} — {self.subject} on {self.date}"


# If you need to track individual students (present/absent)
class AttendanceRecord(models.Model):
    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        related_name='records'
    )
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE
    )
    is_present = models.BooleanField(default=False)
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ['attendance', 'student']

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student} — {status}"