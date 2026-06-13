def jwt_context(request):
    if hasattr(request, 'jwt_payload'):
        return {
            'role': getattr(request, 'jwt_role', 'student'),
            'username': getattr(request, 'jwt_username', ''),
        }
    return {}