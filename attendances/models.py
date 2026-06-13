from django import forms
from .models import Attendance


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = ['classroom', 'subject', 'teacher', 'date']
        widgets = {
            'classroom': forms.Select(attrs={'class': 'form-select'}),
            'subject':   forms.Select(attrs={'class': 'form-select'}),
            'teacher':   forms.Select(attrs={'class': 'form-select'}),
            'date':      forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }