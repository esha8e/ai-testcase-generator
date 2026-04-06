from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from rest_framework.response import Response
from functools import wraps
from .models import User

def get_user_from_token(request):
    """
    Extract token from Authorization header, verify it, and return the user.
    Returns None if token is missing or invalid.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None

    # Support "Bearer <token>" or just the token
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]   # split by space, not empty string
    else:
        token = auth_header

    signer = TimestampSigner()
    try:
        user_id = signer.unsign(token, max_age=86400)  # 24 hours expiry
        user = User.objects(id=user_id).first()
        return user
    except (BadSignature, SignatureExpired):
        return None

def login_required(view_func):
    """
    Decorator to require authentication for a view.
    If authenticated, sets request.user and proceeds.
    Otherwise returns 401 Unauthorized.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = get_user_from_token(request)
        if not user:
            return Response({"error": "Authentication required"}, status=401)
        request.user = user
        return view_func(request, *args, **kwargs)
    return wrapper