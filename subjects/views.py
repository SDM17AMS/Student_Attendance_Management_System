from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import jwt_required
from .models import Subject
from .forms import SubjectForm


@jwt_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/subject_list.html', {
        'subjects': subjects,
        'username': request.jwt_payload['username'],
    })


@jwt_required
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject created.")
            return redirect('subject_list')
    else:
        form = SubjectForm()

    return render(request, 'subjects/subject_form.html', {
        'form': form,
        'title': 'Add New Subject',
        'username': request.jwt_payload['username'],
    })


@jwt_required
def subject_edit(request, id):
    subject = get_object_or_404(Subject, id=id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated.")
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)

    return render(request, 'subjects/subject_form.html', {
        'form': form,
        'title': f'Edit — {subject}',
        'username': request.jwt_payload['username'],
    })


@jwt_required
def subject_delete(request, id):
    subject = get_object_or_404(Subject, id=id)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, "Subject deleted.")
        return redirect('subject_list')

    return render(request, 'subjects/subject_confirm_delete.html', {
        'subject': subject,
        'username': request.jwt_payload['username'],
    })