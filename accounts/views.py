import jwt
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.conf import settings
from accounts.decorators import jwt_required


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
    from students.models import Student
    from classrooms.models import ClassRoom
    from subjects.models import Subject
    from teachers.models import Teacher
    from attendances.models import Attendance

    context = {
        'total_students': Student.objects.count(),
        'total_classrooms': ClassRoom.objects.count(),
        'total_subjects': Subject.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'recent_sessions': Attendance.objects.select_related(
            'classroom', 'subject', 'teacher'
        ).order_by('-date')[:5],
        'username': request.jwt_payload['username'],
    }
    return render(request, 'accounts/dashboard.html', context)