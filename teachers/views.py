from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import jwt_required
from .models import Teacher
from .forms import TeacherForm


@jwt_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {
        'teachers': teachers,
        'username': request.jwt_payload['username'],
    })


@jwt_required
def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher created.")
            return redirect('teacher_list')
    else:
        form = TeacherForm()

    return render(request, 'teachers/teacher_form.html', {
        'form': form,
        'title': 'Add New Teacher',
        'username': request.jwt_payload['username'],
    })


@jwt_required
def teacher_detail(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    sessions = teacher.attendance_set.select_related('classroom', 'subject').order_by('-date')
    return render(request, 'teachers/teacher_detail.html', {
        'teacher': teacher,
        'sessions': sessions,
        'username': request.jwt_payload['username'],
    })


@jwt_required
def teacher_edit(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher updated.")
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)

    return render(request, 'teachers/teacher_form.html', {
        'form': form,
        'title': f'Edit — {teacher.full_name}',
        'username': request.jwt_payload['username'],
    })


@jwt_required
def teacher_delete(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    if request.method == 'POST':
        name = teacher.full_name
        teacher.delete()
        messages.success(request, f"Teacher '{name}' deleted.")
        return redirect('teacher_list')

    return render(request, 'teachers/teacher_confirm_delete.html', {
        'teacher': teacher,
        'username': request.jwt_payload['username'],
    })