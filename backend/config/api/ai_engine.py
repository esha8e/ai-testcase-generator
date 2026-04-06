# ai_engine.py
import os
import re
import nltk
import spacy
import pytesseract
import fitz  # PyMuPDF
import docx

from PIL import Image
from transformers import pipeline
from django.conf import settings

# -------------------------
# BASIC SETUP
# -------------------------
nltk.download("punkt", quiet=True)

if getattr(settings, "TESSERACT_CMD", None):
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

nlp = spacy.load("en_core_web_sm")

# -------------------------
# SENTIMENT MODEL (SAFE, LAZY)
# -------------------------
_SENTIMENT_MODEL = None

def get_sentiment_model():
    global _SENTIMENT_MODEL
    if _SENTIMENT_MODEL is None:
        _SENTIMENT_MODEL = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
    return _SENTIMENT_MODEL

# -------------------------
# PRIORITY INFERENCE
# -------------------------

def infer_priority(action, sentiment):
    action = action.lower()

    # High priority if negative sentiment
    if sentiment == "negative":
        return "High"

    # Critical flows
    if any(word in action for word in ["login", "payment", "checkout", "register"]):
        return "High"

    # Medium for CRUD
    if any(word in action for word in ["add", "update", "delete", "edit"]):
        return "Medium"

    return "Low"
# -------------------------
# TEST CATEGORY INFERENCE
# -------------------------
def infer_test_category(action, objects):
    text = f"{action} {' '.join(objects)}".lower()

    if any(w in text for w in ["login", "auth", "password", "token", "permission"]):
        return "security"
    if any(w in text for w in ["time", "speed", "load", "performance", "response"]):
        return "performance"
    if any(w in text for w in ["db", "database", "record", "table", "store"]):
        return "database"
    if any(w in text for w in ["ui", "button", "screen", "page", "form"]):
        return "ui"

    return "functional"

# -------------------------
# COVERAGE & TEST DATA
# -------------------------
def infer_coverage(action):
    if action in ["create", "update", "submit", "upload"]:
        return ["boundary", "equivalence"]
    return ["equivalence"]

def generate_test_data(action):
    if "login" in action or "auth" in action:
        return {
            "valid": "user@example.com / Password123",
            "invalid": "user@ / 123",
            "boundary": "a" * 256
        }
    return {
        "valid": "valid_input",
        "invalid": "",
        "boundary": "a" * 255
    }

# -------------------------
# OCR IMAGE TEXT
# -------------------------
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    raw_text = pytesseract.image_to_string(image, config="--psm 6")

    cleaned = []
    for line in raw_text.splitlines():
        line = re.sub(r"[^a-zA-Z0-9\s]", " ", line.lower()).strip()
        words = [w for w in line.split() if len(w) > 2]
        if words:
            cleaned.append(" ".join(words))

    return "\n".join(cleaned)

# -------------------------
# PDF / DOCX
# -------------------------
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

def extract_text_from_docx(docx_path):
    document = docx.Document(docx_path)
    return "\n".join(p.text for p in document.paragraphs if p.text.strip())

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(file_path)
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    if ext == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError("Unsupported file type")

# -------------------------
# REQUIREMENT NLP ANALYSIS
# -------------------------
def analyze_requirement(text):
    doc = nlp(text)

    actors, actions, objects = set(), set(), set()

    for token in doc:
        if token.dep_ == "nsubj":
            actors.add(token.text.lower())
        if token.pos_ == "VERB":
            actions.add(token.lemma_.lower())
        if token.pos_ in ("NOUN", "PROPN"):
            objects.add(token.text.lower())

    # SAFE sentiment fallback
    try:
        sentiment = get_sentiment_model()(text)[0]
        label = sentiment["label"]
        score = round(sentiment["score"], 2)
    except Exception:
        label = "NEUTRAL"
        score = 0.5

    return {
        "actors": list(actors) or ["user"],
        "actions": list(actions),
        "objects": list(objects),
        "sentiment": label,
        "confidence": score
    }
def infer_category(action, objects):
    action = action.lower()

    if any(word in action for word in ["login", "logout", "register", "authentication"]):
        return "Authentication"

    elif any(word in action for word in ["search", "filter", "sort"]):
        return "Search"

    elif any(word in action for word in ["add", "update", "delete", "edit"]):
        return "CRUD Operation"

    elif any(word in action for word in ["payment", "checkout", "order"]):
        return "Transaction"

    elif any(word in action for word in ["upload", "download"]):
        return "File Handling"

    else:
        return "General"
# -------------------------
# FUNCTIONAL TEST CASES
# -------------------------
def generate_test_cases(analysis):
    test_cases = []
    tc_index = 1

    for action in analysis["actions"]:
        priority = infer_priority(action, analysis["sentiment"])
        category = infer_category(action, analysis["objects"])

        # ---------------------------------
        # POSITIVE TEST CASE
        # ---------------------------------
        positive_data = {
            "username": "validUser",
            "password": "ValidPass123"
        }

        test_cases.append({
            "id": f"TC_{tc_index:03}",
            "test_category": category,
            "type": "Positive",
            "priority": priority,
            "scenario": f"Verify successful {action}",
            "steps": [
                f"Navigate to {action} page",
                "Enter valid data",
                "Click submit"
            ],
            "test_data": positive_data,
            "expected_result": f"{action.capitalize()} should be successful"
        })
        tc_index += 1

        # ---------------------------------
        # NEGATIVE TEST CASE
        # ---------------------------------
        negative_data = {
            "username": "invalidUser",
            "password": "wrongPass"
        }

        test_cases.append({
            "id": f"TC_{tc_index:03}",
            "test_category": category,
            "type": "Negative",
            "priority": "High",
            "scenario": f"Verify {action} fails with invalid credentials",
            "steps": [
                f"Navigate to {action} page",
                "Enter invalid data",
                "Click submit"
            ],
            "test_data": negative_data,
            "expected_result": "System should display error message"
        })
        tc_index += 1

        # ---------------------------------
        # EDGE CASE - EMPTY INPUT
        # ---------------------------------
        edge_data = {
            "username": "",
            "password": ""
        }

        test_cases.append({
            "id": f"TC_{tc_index:03}",
            "test_category": category,
            "type": "Edge Case",
            "priority": "High",
            "scenario": f"Verify {action} with empty fields",
            "steps": [
                f"Navigate to {action} page",
                "Leave fields empty",
                "Click submit"
            ],
            "test_data": edge_data,
            "expected_result": "System should show mandatory field validation"
        })
        tc_index += 1

        # ---------------------------------
        # BOUNDARY VALUE ANALYSIS
        # ---------------------------------
        boundary_data = {
            "min_length": 1,
            "min_plus_one": 2,
            "max_length": 255,
            "max_minus_one": 254,
            "below_min": 0,
            "above_max": 256
        }

        test_cases.append({
            "id": f"TC_{tc_index:03}",
            "test_category": category,
            "type": "Boundary Value Analysis",
            "priority": "Medium",
            "scenario": f"Verify {action} with boundary input values",
            "test_data": boundary_data,
            "expected_result": "System should handle boundary values correctly"
        })
        tc_index += 1

        # ---------------------------------
        # EQUIVALENCE PARTITIONING
        # ---------------------------------
        equivalence_data = {
            "valid_class": "Correct format input",
            "invalid_empty": "",
            "invalid_special_characters": "@@@###"
        }

        test_cases.append({
            "id": f"TC_{tc_index:03}",
            "test_category": category,
            "type": "Equivalence Partitioning",
            "priority": "Medium",
            "scenario": f"Verify {action} using equivalence classes",
            "test_data": equivalence_data,
            "expected_result": "Valid class should pass, invalid classes should fail"
        })
        tc_index += 1

    return test_cases
# def generate_test_cases(analysis):
#     test_cases = []
#     actors = analysis["actors"]
#     actions = analysis["actions"]
#     objects = analysis["objects"]

#     tc_index = 1
#     def tc_id():
#         nonlocal tc_index
#         tid = f"TC_{tc_index:03}"
#         tc_index += 1
#         return tid

#     for action in actions:
#         priority = infer_priority(action)
#         category = infer_test_category(action, objects)
#         coverage = infer_coverage(action)
#         test_data = generate_test_data(action)

#         test_cases.append({
#             "id": tc_id(),
#             "test_category": category,
#             "type": "Positive",
#             "priority": priority,
#             "test_case": f"Verify {actors[0]} can {action} with valid data",
#             "expected_result": f"{action.capitalize()} should be successful",
#             "coverage": coverage,
#             "test_data": test_data
#         })

#         test_cases.append({
#             "id": tc_id(),
#             "test_category": category,
#             "type": "Negative",
#             "priority": priority,
#             "test_case": f"Verify {action} fails with invalid input",
#             "expected_result": "Error message should be displayed",
#             "coverage": coverage,
#             "test_data": test_data
#         })

#         test_cases.append({
#             "id": tc_id(),
#             "test_category": category,
#             "type": "Validation",
#             "priority": priority,
#             "test_case": f"Verify mandatory field validation during {action}",
#             "expected_result": "Validation message should be shown",
#             "coverage": ["equivalence"]
#         })

#         if objects:
#             test_cases.append({
#                 "id": tc_id(),
#                 "test_category": category,
#                 "type": "Boundary",
#                 "priority": "Medium",
#                 "test_case": f"Verify boundary values for {objects[0]} during {action}",
#                 "expected_result": f"{objects[0].capitalize()} limits should be enforced",
#                 "coverage": ["boundary"]
#             })

#     if not test_cases:
#         test_cases.append({
#             "id": "TC_001",
#             "test_category": "functional",
#             "type": "Info",
#             "priority": "Low",
#             "test_case": "No actionable requirement detected",
#             "expected_result": "Requirement needs clarification"
#         })

#     return test_cases

# -------------------------
# ENTRY POINTS
# -------------------------
def process_requirement_text(text):
    analysis = analyze_requirement(text)
    return {"analysis": analysis, "test_cases": generate_test_cases(analysis)}

def process_uploaded_requirement(file_path):
    return process_requirement_text(extract_text_from_file(file_path))

# -------------------------
# EXPORT SUPPORT
# -------------------------
from api.export_utils import (
    export_to_csv,
    export_to_excel,
    export_to_json,
    export_to_pdf
)

def export_test_cases(test_cases, export_type="csv"):
    os.makedirs("exports", exist_ok=True)
    filename = f"exports/test_cases_{os.urandom(4).hex()}.{export_type}"

    if export_type == "csv":
        return export_to_csv(test_cases, filename)
    if export_type == "excel":
        return export_to_excel(test_cases, filename)
    if export_type == "json":
        return export_to_json(test_cases, filename)
    if export_type == "pdf":
        return export_to_pdf(test_cases, filename)

    raise ValueError("Unsupported export format")

# -------------------------
# API SPEC PROCESSING
# -------------------------
from api.api_testcase_engine import (
    load_openapi_file,
    extract_endpoints,
    generate_api_test_cases
)

def process_api_spec(file_path):
    spec = load_openapi_file(file_path)
    endpoints = extract_endpoints(spec)
    return {
        "analysis": {"type": "API_SPEC"},
        "test_cases": generate_api_test_cases(endpoints)
    }
