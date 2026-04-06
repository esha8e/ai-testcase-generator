# export_utils.py
import os
import json
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from textwrap import wrap

# -------------------------
# CSV EXPORT
# -------------------------
def export_to_csv(test_cases, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df = pd.DataFrame(test_cases)
    df.to_csv(file_path, index=False)
    return file_path

# -------------------------
# EXCEL EXPORT
# -------------------------
def export_to_excel(test_cases, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df = pd.DataFrame(test_cases)
    df.to_excel(file_path, index=False)
    return file_path

# -------------------------
# JSON EXPORT
# -------------------------
def export_to_json(test_cases, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(test_cases, f, indent=4, ensure_ascii=False)
    return file_path

# -------------------------
# PDF EXPORT
# -------------------------
def export_to_pdf(test_cases, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    x = 40
    y = height - 40
    max_width = width - 80

    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, "Generated Test Cases")
    y -= 30

    c.setFont("Helvetica", 10)

    for i, tc in enumerate(test_cases, start=1):

        if y < 100:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 40

        lines = [
            f"{i}. Test ID: {tc.get('id', 'N/A')}",
            f"Category: {tc.get('test_category', 'N/A')}",
            f"Type: {tc.get('type', 'N/A')}",
            f"Priority: {tc.get('priority', 'N/A')}",
            f"Test Case: {tc.get('test_case', '')}",
            f"Expected Result: {tc.get('expected_result', '')}",
        ]

        for line in lines:
            wrapped = wrap(line, 90)
            for wline in wrapped:
                c.drawString(x, y, wline)
                y -= 14

        y -= 10

    c.save()
    return file_path
