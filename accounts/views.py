import jwt
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from accounts.decorators import jwt_required, admin_required, teacher_required

from students.models import Student
from classrooms.models import ClassRoom
from subjects.models import Subject
from teachers.models import Teacher
from attendances.models import Attendance


def get_user_role(user):
    """Determine user role based on associated models."""
    if user.is_superuser or user.is_staff:
        return 'admin'
    if hasattr(user, 'teacher_profile'):
        return 'teacher'
    if hasattr(user, 'student_profile'):
        return 'student'
    return 'student'


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            now = datetime.datetime.now(datetime.timezone.utc)
            role = get_user_role(user)
            
            payload = {
                'user_id': user.id,
                'username': user.username,
                'role': role,
                'token_type': 'access',
                'iat': now,
                'exp': now + datetime.timedelta(minutes=settings.JWT_EXPIRY_MINUTES),
            }
            token = jwt.encode(
                payload,
                settings.JWT_SECRET_KEY,
                algorithm=settings.JWT_ALGORITHM
            )

            response = redirect('dashboard')
            response.set_cookie(
                settings.JWT_COOKIE_NAME,
                token,
                max_age=settings.JWT_EXPIRY_MINUTES * 60,
                httponly=True,
                samesite='Lax'
            )
            return response
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password.',
                'hide_sidebar': True,
            })

    return render(request, 'accounts/login.html', {'hide_sidebar': True})


def logout_view(request):
    response = redirect('login')
    response.delete_cookie(
        settings.JWT_COOKIE_NAME,
        path='/',
        samesite='Lax'
    )
    return response


@jwt_required
def dashboard_view(request):
    role = request.jwt_role
    
    if role == 'admin':
        total_students = Student.objects.count()
        total_classrooms = ClassRoom.objects.count()
        total_subjects = Subject.objects.count()
        total_teachers = Teacher.objects.count()
        
        recent_sessions = Attendance.objects.select_related(
            'classroom', 'subject', 'teacher'
        ).order_by('-date')[:5]
        
        context = {
            'total_students': total_students,
            'total_classrooms': total_classrooms,
            'total_subjects': total_subjects,
            'total_teachers': total_teachers,
            'recent_sessions': recent_sessions,
        }
    
    elif role == 'teacher':
        try:
            teacher = Teacher.objects.get(user_id=request.jwt_user_id)
            total_students = Student.objects.filter(classroom__teacher=teacher).count()
            total_classrooms = ClassRoom.objects.filter(teacher=teacher).count()
            total_subjects = Subject.objects.filter(teacher=teacher).count()
            
            recent_sessions = Attendance.objects.filter(
                teacher=teacher
            ).select_related('classroom', 'subject').order_by('-date')[:5]
            
            context = {
                'teacher': teacher,
                'total_students': total_students,
                'total_classrooms': total_classrooms,
                'total_subjects': total_subjects,
                'recent_sessions': recent_sessions,
            }
        except Teacher.DoesNotExist:
            context = {
                'error': 'Teacher profile not found.',
            }
    
    else:  # student
        try:
            student = Student.objects.get(user_id=request.jwt_user_id)
            
            from attendances.models import AttendanceRecord
            attendance_records = AttendanceRecord.objects.filter(
                student=student
            ).select_related('attendances__subject', 'attendances__classroom').order_by('-attendances__date')[:10]
            
            present_count = attendance_records.filter(status='present').count()
            total_count = attendance_records.count()
            attendance_rate = round((present_count / total_count * 100), 1) if total_count > 0 else 0
            
            context = {
                'student': student,
                'classroom': student.classroom,
                'attendance_records': attendance_records,
                'attendance_rate': attendance_rate,
                'present_count': present_count,
                'total_count': total_count,
            }
        except Student.DoesNotExist:
            context = {
                'error': 'Student profile not found.',
            }
    
    return render(request, 'accounts/dashboard.html', context)


# ─── User Creation Views ───

@admin_required
def create_teacher_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" already exists.')
            return render(request, 'accounts/create_teacher.html')
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user.is_staff = True
        user.save()
        
        Teacher.objects.create(user=user, full_name=full_name, email=email)
        messages.success(request, f'Teacher "{full_name}" created successfully.')
        return redirect('teacher_list')
    
    return render(request, 'accounts/create_teacher.html')


@admin_required
def create_student_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        classroom_id = request.POST.get('classroom')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" already exists.')
            classrooms = ClassRoom.objects.all()
            return render(request, 'accounts/create_student.html', {'classrooms': classrooms})
        
        user = User.objects.create_user(username=username, password=password, email=email)
        
        classroom = None
        if classroom_id:
            classroom = ClassRoom.objects.filter(id=classroom_id).first()
        
        Student.objects.create(user=user, full_name=full_name, classroom=classroom)
        messages.success(request, f'Student "{full_name}" created successfully.')
        return redirect('student_list')
    
    classrooms = ClassRoom.objects.all()
    return render(request, 'accounts/create_student.html', {'classrooms': classrooms})