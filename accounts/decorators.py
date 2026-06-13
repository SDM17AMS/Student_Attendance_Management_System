import jwt
from functools import wraps
from django.shortcuts import redirect
from django.conf import settings


def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get(settings.JWT_COOKIE_NAME)

        if not token:
            return redirect('login')

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            request.jwt_payload = payload
            request.jwt_user_id = payload.get('user_id')
            request.jwt_username = payload.get('username')
        except jwt.ExpiredSignatureError:
            return redirect('login')
        except jwt.InvalidTokenError:
            return redirect('login')

        return view_func(request, *args, **kwargs)

    return wrapper