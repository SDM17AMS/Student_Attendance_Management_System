from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import jwt_required
from .models import Attendance, AttendanceRecord
from .forms import AttendanceForm
from students.models import Student


@jwt_required
def attendance_list(request):
    sessions = Attendance.objects.select_related('classroom', 'subject', 'teacher').order_by('-date')
    return render(request, 'attendances/attendance_list.html', {
        'sessions': sessions,
        'username': request.jwt_payload['username'],
    })


@jwt_required
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save()
            messages.success(request, "Attendance session created.")
            return redirect('attendance_detail', id=attendance.id)
    else:
        form = AttendanceForm()

    return render(request, 'attendances/attendance_form.html', {
        'form': form,
        'title': 'New Attendance Session',
        'username': request.jwt_payload['username'],
    })


@jwt_required
def attendance_detail(request, id):
    attendance = get_object_or_404(
        Attendance.objects.select_related('classroom', 'subject', 'teacher'),
        id=id
    )
    records = attendance.records.select_related('student').all()
    return render(request, 'attendances/attendance_detail.html', {
        'attendance': attendance,
        'records': records,
        'username': request.jwt_payload['username'],
    })


@jwt_required
def attendance_edit(request, id):
    attendance = get_object_or_404(Attendance, id=id)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, "Session updated.")
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)

    return render(request, 'attendances/attendance_form.html', {
        'form': form,
        'title': f'Edit Session — {attendance}',
        'username': request.jwt_payload['username'],
    })


@jwt_required
def attendance_delete(request, id):
    attendance = get_object_or_404(Attendance, id=id)
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, "Session deleted.")
        return redirect('attendance_list')

    return render(request, 'attendances/attendance_confirm_delete.html', {
        'attendance': attendance,
        'username': request.jwt_payload['username'],
    })


@jwt_required
def attendance_mark(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    students = Student.objects.filter(classroom=attendance.classroom).order_by('full_name')

    if request.method == 'POST':
        # Save attendance records
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'absent')
            AttendanceRecord.objects.update_or_create(
                attendances=attendance,
                student=student,
                defaults={'status': status}
            )
        messages.success(request, "Attendance saved successfully.")
        return redirect('attendance_detail', id=attendance.id)

    # GET: Build lookup and display form
    existing_records = AttendanceRecord.objects.filter(attendances=attendance)
    existing_statuses = {str(r.student_id): r.status for r in existing_records}

    student_statuses = []
    for student in students:
        sid = str(student.id)
        status = existing_statuses.get(sid, '')
        student_statuses.append({
            'student': student,
            'status': status,
        })

    return render(request, 'attendances/attendance_mark.html', {
        'attendance': attendance,
        'student_statuses': student_statuses,
        'username': request.jwt_payload['username'],
    })