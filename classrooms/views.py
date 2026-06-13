from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import jwt_required
from .models import ClassRoom
from .forms import ClassRoomForm


@jwt_required
def class_list(request):
    classes = ClassRoom.objects.prefetch_related('students').all()
    return render(request, 'classrooms/class_list.html', {
        'classes': classes,
        'username': request.jwt_payload['username'],
    })


@jwt_required
def class_create(request):
    if request.method == 'POST':
        form = ClassRoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Classroom created.")
            return redirect('class_list')
    else:
        form = ClassRoomForm()

    return render(request, 'classrooms/class_form.html', {
        'form': form,
        'title': 'Add New Classroom',
        'username': request.jwt_payload['username'],
    })


@jwt_required
def class_detail(request, id):
    classroom = get_object_or_404(ClassRoom, id=id)
    students = classroom.students.all()
    return render(request, 'classrooms/class_detail.html', {
        'classroom': classroom,
        'students': students,
        'username': request.jwt_payload['username'],
    })


@jwt_required
def class_edit(request, id):
    classroom = get_object_or_404(ClassRoom, id=id)
    if request.method == 'POST':
        form = ClassRoomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, "Classroom updated.")
            return redirect('class_list')
    else:
        form = ClassRoomForm(instance=classroom)

    return render(request, 'classrooms/class_form.html', {
        'form': form,
        'title': f'Edit — {classroom}',
        'username': request.jwt_payload['username'],
    })


@jwt_required
def class_delete(request, id):
    classroom = get_object_or_404(ClassRoom, id=id)
    if request.method == 'POST':
        name = str(classroom)
        classroom.delete()
        messages.success(request, f"Classroom '{name}' deleted.")
        return redirect('class_list')

    return render(request, 'classrooms/class_confirm_delete.html', {
        'classroom': classroom,
        'username': request.jwt_payload['username'],
    })