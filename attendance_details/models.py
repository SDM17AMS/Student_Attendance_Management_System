from django import forms
from .models import AttendanceDetail


class AttendanceDetailForm(forms.ModelForm):
    class Meta:
        model = AttendanceDetail
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }