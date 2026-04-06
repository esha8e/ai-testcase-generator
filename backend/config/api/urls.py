from django.urls import path
from .views import (
    backend_status,
    generate_testcases,
    generate_api_testcases,
    export_testcases,
    signup,
    login,
    verify_token,
    get_history,
    get_run_detail,
    # change_password,   # <-- remove this line
)

urlpatterns = [
    path("", backend_status),
    path("generate/", generate_testcases),
    path("generate/api/", generate_api_testcases),
    path("export/", export_testcases),
    path("auth/signup/", signup),
    path("auth/login/", login),
    path("auth/verify/", verify_token),
    path("history/", get_history),
    path("history/<str:run_id>/", get_run_detail),
]