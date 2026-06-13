# forms.py
from django import forms
from .models import AttendanceDetail


class AttendanceDetailForm(forms.ModelForm):
    class Meta:
        model = AttendanceDetail
        fields = ['attendance', 'student', 'status']
        widgets = {
            'attendance': forms.HiddenInput(),
            'student':    forms.HiddenInput(),
            'status':     forms.Select(attrs={
                'class': 'form-select form-select-sm'
            }),
        }