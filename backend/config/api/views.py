import os
import uuid
from datetime import datetime  # new import
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.ai_engine import (
    process_requirement_text,
    process_uploaded_requirement,
    process_api_spec,
    export_test_cases
)

from .models import TestCaseRun, TestCase, User
from django.contrib.auth.hashers import make_password, check_password
from django.core.signing import TimestampSigner

# Import authentication helpers
from .auth import login_required, get_user_from_token  # new import


# -------------------------
# AUTHENTICATION
# -------------------------
@api_view(["POST"])
def signup(request):
    data = request.data
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return Response({"error": "All fields are required"}, status=400)

    if User.objects(username=username).first():
        return Response({"error": "Username already exists"}, status=400)
    
    if User.objects(email=email).first():
        return Response({"error": "Email already exists"}, status=400)

    user = User(
        username=username,
        email=email,
        password=make_password(password)
    )
    user.save()
    return Response({"message": "User created successfully"}, status=201)


@api_view(["POST"])
def login(request):
    data = request.data
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=400)

    user = User.objects(username=username).first()
    
    if not user:
        user = User.objects(email=username).first()

    if not user:
        return Response({"error": "Invalid credentials"}, status=400)

    if check_password(password, user.password):
        signer = TimestampSigner()
        token = signer.sign(str(user.id))
        
        return Response({
            "message": "Login successful",
            "username": user.username,
            "email": user.email,
            "token": token
        })
    else:
        return Response({"error": "Invalid credentials"}, status=400)


@api_view(["GET"])
def verify_token(request):
    token = request.headers.get("Authorization")
    if not token:
        token = request.query_params.get("token")
    
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        return Response({"error": "Token required"}, status=400)

    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    signer = TimestampSigner()
    try:
        user_id = signer.unsign(token, max_age=86400)
        user = User.objects(id=user_id).first()
        if not user:
            return Response({"error": "User not found"}, status=404)
             
        return Response({
            "valid": True,
            "username": user.username,
            "email": user.email,
            "id": str(user.id)
        })
    except Exception as e:
        return Response({"error": "Invalid or expired token"}, status=400)


# -------------------------
# UTIL: SAVE UPLOADED FILE
# -------------------------
def save_uploaded_file(file):
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    ext = file.name.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(settings.MEDIA_ROOT, filename)

    with open(path, "wb+") as dest:
        for chunk in file.chunks():
            dest.write(chunk)

    return path


# -------------------------
# HEALTH CHECK
# -------------------------
@api_view(["GET"])
def backend_status(request):
    return Response({
        "status": "Backend running",
        "project": "AI Test Case Generator"
    })


# -------------------------
# GENERATE TEST CASES (TEXT / FILE) – PROTECTED
# -------------------------
@api_view(["POST"])
@login_required
def generate_testcases(request):

    # FILE UPLOAD
    if request.FILES.get("file"):
        file_path = save_uploaded_file(request.FILES["file"])
        result = process_uploaded_requirement(file_path)

    # RAW TEXT
    else:
        requirement_text = request.data.get("requirement", "").strip()

        if not requirement_text:
            return Response(
                {"error": "Requirement text or file is required"},
                status=400
            )

        result = process_requirement_text(requirement_text)

    # SAVE TO DB WITH USER AND TIMESTAMP
    run = TestCaseRun(
        user=request.user,  # associate with logged-in user
        requirement=result.get("analysis", {}),
        test_cases=[
            TestCase(
                test_id=tc.get("id"),
                type=tc.get("type"),
                priority=tc.get("priority"),
                test_case=tc.get("test_case"),
                expected_result=tc.get("expected_result")
            )
            for tc in result.get("test_cases", [])
        ],
        created_at=datetime.now()
    )
    run.save()

    return Response(result)


# -------------------------
# GENERATE API TEST CASES – PROTECTED
# -------------------------
@api_view(["POST"])
@login_required
def generate_api_testcases(request):

    if not request.FILES.get("file"):
        return Response({"error": "API spec file required"}, status=400)

    file_path = save_uploaded_file(request.FILES["file"])
    result = process_api_spec(file_path)

    run = TestCaseRun(
        user=request.user,  # associate with logged-in user
        requirement={"type": "API_SPEC"},
        test_cases=[
            TestCase(
                test_id=tc.get("id"),
                type=tc.get("type"),
                priority=tc.get("priority"),
                test_case=tc.get("test_case"),
                expected_result=tc.get("expected_result")
            )
            for tc in result.get("test_cases", [])
        ],
        created_at=datetime.now()
    )
    run.save()

    return Response(result)


# -------------------------
# EXPORT TEST CASES – PROTECTED (optional, but user must be authenticated to export)
# -------------------------
@api_view(["POST"])
@login_required
def export_testcases(request):
    test_cases = request.data.get("test_cases")
    export_format = request.data.get("format", "csv")

    if not test_cases:
        return Response({"error": "test_cases data required"}, status=400)

    try:
        file_path = export_test_cases(test_cases, export_format)
    except ValueError as e:
        return Response({"error": str(e)}, status=400)

    return Response({
        "message": "Export successful",
        "file_path": file_path
    })


# -------------------------
# HISTORY ENDPOINTS – PROTECTED
# -------------------------
@api_view(["GET"])
@login_required
def get_history(request):
    """List all test case runs for the authenticated user."""
    runs = TestCaseRun.objects(user=request.user).order_by('-created_at')
    data = []
    for run in runs:
        data.append({
            "id": str(run.id),
            "created_at": run.created_at.isoformat() if run.created_at else None,
            "summary": run.requirement.get("actions", ["N/A"])[0] if run.requirement else "N/A",
            "test_case_count": len(run.test_cases)
        })
    return Response(data)


@api_view(["GET"])
@login_required
def get_run_detail(request, run_id):
    """Retrieve a specific test case run."""
    run = TestCaseRun.objects(id=run_id, user=request.user).first()
    if not run:
        return Response({"error": "Run not found"}, status=404)

    return Response({
        "id": str(run.id),
        "created_at": run.created_at.isoformat() if run.created_at else None,
        "requirement": run.requirement,
        "test_cases": [
            {
                "test_id": tc.test_id,
                "type": tc.type,
                "priority": tc.priority,
                "test_case": tc.test_case,
                "expected_result": tc.expected_result
            }
            for tc in run.test_cases
        ]
    })