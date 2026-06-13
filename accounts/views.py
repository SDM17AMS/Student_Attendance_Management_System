# accounts/views.py
import jwt
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.conf import settings
from django.db.models import Count, Avg
from accounts.decorators import jwt_required

# Import your models
from students.models import Student
from classrooms.models import ClassRoom
from subjects.models import Subject
from teachers.models import Teacher
from attendances.models import Attendance


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            now = datetime.datetime.now(datetime.timezone.utc)
            payload = {
                'user_id': user.id,
                'username': user.username,
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
                'error': 'Invalid username or password.'
            })

    return render(request, 'accounts/login.html')


def logout_view(request):
    response = redirect('login')
    response.delete_cookie(settings.JWT_COOKIE_NAME)
    return response


@jwt_required
def dashboard_view(request):
    """
    Enhanced dashboard with all the data your frontend needs.
    """
    # Get counts
    total_students = Student.objects.count()
    total_classrooms = ClassRoom.objects.count()
    total_subjects = Subject.objects.count()
    total_teachers = Teacher.objects.count()
    
    # Get recent attendance sessions
    recent_sessions = Attendance.objects.select_related(
        'classroom', 'subject', 'teacher'
    ).order_by('-date')[:5]
    
    # Get student stats for the table
    students = Student.objects.select_related('classroom').all()
    
    # Get teachers
    teachers = Teacher.objects.prefetch_related('subjects').all()
    
    # Get classrooms with student counts
    classrooms = ClassRoom.objects.annotate(
        student_count=Count('students')
    ).all()
    
    # Get attendance data for charts
    attendance_data = []  # You'll populate this from your attendance model
    
    context = {
        'username': request.jwt_payload['username'],
        'total_students': total_students,
        'total_classrooms': total_classrooms,
        'total_subjects': total_subjects,
        'total_teachers': total_teachers,
        'recent_sessions': recent_sessions,
        'students': students,
        'teachers': teachers,
        'classrooms': classrooms,
        'attendance_data': attendance_data,
    }
    return render(request, 'accounts/dashboard.html', context)