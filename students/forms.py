from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'classroom']   # exclude student_id
        # OR explicitly exclude:
        # exclude = ['student_id']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input'}),
            'classroom': forms.Select(attrs={'class': 'form-input'}),
        }