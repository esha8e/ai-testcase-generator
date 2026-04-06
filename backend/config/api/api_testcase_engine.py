# api/api_testcase_engine.py

import json
import yaml

# -------------------------
# LOAD OPENAPI FILE
# -------------------------
def load_openapi_file(file_path):
    if file_path.endswith(".json"):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    elif file_path.endswith((".yaml", ".yml")):
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    else:
        raise ValueError("Unsupported API spec format")

# -------------------------
# EXTRACT ENDPOINTS
# -------------------------
def extract_endpoints(openapi_spec):
    endpoints = []

    paths = openapi_spec.get("paths", {})

    for path, methods in paths.items():
        for method, details in methods.items():
            endpoints.append({
                "path": path,
                "method": method.upper(),
                "summary": details.get("summary", ""),
                "parameters": details.get("parameters", []),
                "requestBody": details.get("requestBody", {})
            })

    return endpoints

# -------------------------
# GENERATE API TEST CASES
# -------------------------
# def generate_api_test_cases(endpoints):
#     """
#     Generates API test cases from extracted endpoints
#     """
#     test_cases = []
#     tc_index = 1

#     def tc_id():
#         nonlocal tc_index
#         tid = f"API_TC_{tc_index:03}"
#         tc_index += 1
#         return tid

#     for ep in endpoints:
#         method = ep["method"]
#         path = ep["path"]

#         # Positive test
#         test_cases.append({
#             "id": tc_id(),
#             "type": "Positive",
#             "priority": "High",
#             "test_case": f"Verify {method} {path} with valid request",
#             "expected_result": "API should return success response"
#         })

#         # Negative test
#         test_cases.append({
#             "id": tc_id(),
#             "type": "Negative",
#             "priority": "Medium",
#             "test_case": f"Verify {method} {path} with invalid data",
#             "expected_result": "API should return validation error"
#         })

#         # Auth test
#         test_cases.append({
#             "id": tc_id(),
#             "type": "Security",
#             "priority": "High",
#             "test_case": f"Verify {method} {path} without authentication",
#             "expected_result": "API should reject unauthorized request"
#         })

#     return test_cases
def generate_api_test_cases(endpoints):
    test_cases = []
    tc_index = 1

    for ep in endpoints:
        method = ep["method"]
        path = ep["path"]

        category = "API"

        # ------------------------------
        # POSITIVE
        # ------------------------------
        test_cases.append({
            "id": f"API_TC_{tc_index:03}",
            "test_category": category,
            "type": "Positive",
            "priority": "High",
            "scenario": f"Verify {method} {path} with valid request",
            "steps": [
                f"Prepare valid request payload for {path}",
                f"Send {method} request",
                "Verify response status code",
                "Validate response body"
            ],
            "test_data": {
                "valid_payload": "Sample valid request body",
                "expected_status": 200
            },
            "expected_result": "API should return success response"
        })
        tc_index += 1

        # ------------------------------
        # NEGATIVE
        # ------------------------------
        test_cases.append({
            "id": f"API_TC_{tc_index:03}",
            "test_category": category,
            "type": "Negative",
            "priority": "Medium",
            "scenario": f"Verify {method} {path} with invalid data",
            "steps": [
                "Prepare invalid request payload",
                f"Send {method} request",
                "Verify error response"
            ],
            "test_data": {
                "invalid_payload": "Incorrect or missing fields",
                "expected_status": 400
            },
            "expected_result": "API should return validation error"
        })
        tc_index += 1

        # ------------------------------
        # SECURITY
        # ------------------------------
        test_cases.append({
            "id": f"API_TC_{tc_index:03}",
            "test_category": category,
            "type": "Security",
            "priority": "High",
            "scenario": f"Verify {method} {path} without authentication",
            "steps": [
                "Remove authentication token",
                f"Send {method} request",
                "Verify unauthorized response"
            ],
            "test_data": {
                "auth_token": None,
                "expected_status": 401
            },
            "expected_result": "API should reject unauthorized request"
        })
        tc_index += 1

    return test_cases