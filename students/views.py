from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 

from accounts.decorators import jwt_required
from .models import Student
from .forms import StudentForm


@jwt_required
def student_list(request):
    students = Student.objects.select_related('classroom').all()
    return render(request, 'students/student_list.html', {
        'students': students,
        'username': request.jwt_payload['username'],
    })


@jwt_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)  # Bind POST data to form

        if form.is_valid():
            form.save()   # Creates a new Student row in the DB
            messages.success(request, "Student created successfully.")
            return redirect('student_list')
    else:
        form = StudentForm()  # Empty unbound form for GET

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Add New Student',
        'username': request.jwt_payload['username'],
    })


@jwt_required
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)

    # Fetch this student's attendance records, newest first
    attendance_records = student.attendance_records.select_related(
        'attendance__classroom', 'attendance__subject', 'attendance__teacher'
    ).order_by('-attendance__date')

    return render(request, 'students/student_detail.html', {
        'student': student,
        'attendance_records': attendance_records,
        'username': request.jwt_payload['username'],
    })


@jwt_required
def student_edit(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"Student '{student.full_name}' updated.")
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)  # Pre-filled form

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': f'Edit — {student.full_name}',
        'student': student,
        'username': request.jwt_payload['username'],
    })


@jwt_required
def student_delete(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        name = student.full_name
        student.delete()
        messages.success(request, f"Student '{name}' deleted.")
        return redirect('student_list')

    return render(request, 'students/student_confirm_delete.html', {
        'student': student,
        'username': request.jwt_payload['username'],
    })
