from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import jwt_required
from .models import AttendanceDetail
from .forms import AttendanceDetailForm


@jwt_required
def attendance_record_edit(request, id):
    record = get_object_or_404(AttendanceDetail, id=id)
    if request.method == 'POST':
        form = AttendanceDetailForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated.")
            return redirect('attendance_detail', id=record.attendance.id)
    else:
        form = AttendanceDetailForm(instance=record)

    return render(request, 'attendance_details/attendance_detail_form.html', {
        'form': form,
        'record': record,
        'username': request.jwt_payload['username'],
    })


@jwt_required
def attendance_record_delete(request, id):
    record = get_object_or_404(AttendanceDetail, id=id)
    attendance_id = record.attendance.id
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Record deleted.")
        return redirect('attendance_detail', id=attendance_id)

    return render(request, 'attendance_details/attendance_detail_confirm_delete.html', {
        'record': record,
        'username': request.jwt_payload['username'],
    })