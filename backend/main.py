import os
from io import BytesIO, StringIO
from typing import Any, Optional
from datetime import datetime

import numpy as np
import pandas as pd
import requests
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from engine.data_quality_engine import DataQualityEngine
from engine.ai_data_quality_engine import AIDataQualityEngine
from api.ai_routes import router as ai_router
from rapidfuzz import fuzz, process as rf_process


def sanitize_for_json(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(item) for item in obj]
    elif isinstance(obj, float):
        if np.isnan(obj) or np.isinf(obj):
            return None
    return obj


app = FastAPI(title="Data Quality Guardian AI", version="2.0")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_router)

engine = DataQualityEngine()
ai_engine = AIDataQualityEngine()
last_cleaned_df: Optional[pd.DataFrame] = None
last_report: Optional[dict] = None
last_fixes: Optional[list] = None
last_missing_records: Optional[list] = None
last_invalid_records: Optional[list] = None
last_duplicate_records: Optional[list] = None


class OnlineVerifyRequest(BaseModel):
    field_type: str
    value: str


class AiSuggestRequest(BaseModel):
    field_type: str
    value: Optional[str] = ""


@app.get("/")
def healthcheck():
    return {
        "status": "ok",
        "service": "Data Quality Guardian AI",
        "version": "2.0",
        "engines": ["rule-based", "ai-powered"],
    }


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    data_type: str = Form("people"),
    use_ai: bool = Form(True),
):
    global last_cleaned_df, last_report, last_missing_records, last_invalid_records, last_duplicate_records

    file_ext = file.filename.lower().split(".")[-1]
    if file_ext not in ["csv", "xlsx", "xls"]:
        raise HTTPException(status_code=400, detail="Only CSV and Excel (.xlsx, .xls) files are supported")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        selected_engine = ai_engine if use_ai else engine
        if file_ext == "csv":
            result = selected_engine.process_csv(content, data_type=data_type)
        else:
            result = selected_engine.process_excel(content, data_type=data_type)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(exc)}") from exc

    last_cleaned_df = pd.DataFrame(result["cleaned_data"])
    last_report = result["report"]
    last_fixes = result.get("fixes", [])
    last_missing_records = result.get("missing_records", [])
    last_invalid_records = result.get("invalid_records", [])
    last_duplicate_records = result.get("duplicate_records", [])

    response_data = {
        "cleaned_data": result["cleaned_data"],
        "report": result["report"],
        "fixes": result["fixes"],
        "anomaly_records": result.get("anomaly_records", []),
        "low_confidence_records": result.get("low_confidence_records", []),
        "engine_used": "ai-powered" if use_ai else "rule-based",
    }
    return sanitize_for_json(response_data)


@app.get("/download/cleaned")
async def download_cleaned():
    if last_cleaned_df is None:
        raise HTTPException(status_code=404, detail="No cleaned dataset available. Upload first.")
    csv_buffer = StringIO()
    last_cleaned_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    headers = {"Content-Disposition": "attachment; filename=cleaned_data.csv"}
    return StreamingResponse(iter([csv_buffer.getvalue()]), media_type="text/csv", headers=headers)


@app.get("/download/pdf")
async def download_pdf_report():
    if last_cleaned_df is None or last_report is None:
        raise HTTPException(status_code=404, detail="No report available. Upload first.")
    try:
        import tempfile
        from reports.pdf_generator import B2BDataQualityReport

        with tempfile.NamedTemporaryFile(mode="w+b", suffix=".pdf", delete=False) as tmp_file:
            pdf_path = tmp_file.name

        pdf_generator = B2BDataQualityReport()
        pdf_generator.generate_report(
            original_data=last_cleaned_df.copy(),
            cleaned_data=last_cleaned_df,
            report_metrics=last_report,
            fixes=last_fixes or [],
            output_path=pdf_path,
        )

        with open(pdf_path, "rb") as f:
            pdf_content = f.read()
        os.unlink(pdf_path)

        headers = {
            "Content-Disposition": f"attachment; filename=data_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        }
        return StreamingResponse(BytesIO(pdf_content), media_type="application/pdf", headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation error: {str(e)}")


@app.get("/download/excel")
async def download_excel():
    if last_cleaned_df is None or last_report is None:
        raise HTTPException(status_code=404, detail="No cleaned dataset available. Upload first.")
    try:
        from reports.excel_generator import ProfessionalExcelReport

        excel_generator = ProfessionalExcelReport()
        cleaned_df = last_cleaned_df if isinstance(last_cleaned_df, pd.DataFrame) else pd.DataFrame(last_cleaned_df)

        output = excel_generator.generate_report(
            original_data=cleaned_df.copy(),
            cleaned_data=cleaned_df,
            report_metrics=last_report,
            fixes=last_fixes or [],
            missing_records=last_missing_records or [],
            invalid_records=last_invalid_records or [],
            duplicate_records=last_duplicate_records or [],
        )

        headers = {
            "Content-Disposition": f"attachment; filename=data_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        }
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excel generation error: {str(e)}")


@app.post("/ai-suggest")
async def ai_suggest(request: AiSuggestRequest):
    field_type = request.field_type.lower()
    value = (request.value or "").strip()

    if not value:
        raise HTTPException(status_code=400, detail="Value cannot be empty")

    try:
        if field_type in ("email", "people_email"):
            import re
            from email_validator import validate_email, EmailNotValidError
            suggested = engine._suggest_email_fix(value)
            try:
                info = validate_email(suggested, check_deliverability=False)
                return {"original": value, "suggestion": info.normalized, "confidence": 0.9, "source": "Online AI", "details": f"Cleaned: {value} → {info.normalized}"}
            except EmailNotValidError:
                return {"original": value, "suggestion": suggested, "confidence": 0.6, "source": "Online AI", "details": "Cleaned but still invalid. Manual review recommended."}

        if field_type in ("phone", "people_phone"):
            import re
            digits = re.sub(r"\D", "", value)
            if 7 <= len(digits) <= 15:
                return {"original": value, "suggestion": "+" + digits, "confidence": 0.85, "source": "Online AI", "details": f"Normalized digits: {len(digits)}"}
            return {"original": value, "suggestion": value, "confidence": 0.3, "source": "Online AI", "details": "Invalid length (need 7-15 digits)"}

        if field_type in ("first_name", "last_name", "middle_name", "person_name", "name"):
            suggested = engine._suggest_name_fix(value)
            if suggested and not suggested.startswith("[") and suggested != value:
                return {"original": value, "suggestion": suggested, "confidence": 0.85, "source": "Online AI", "details": "Removed numbers/special characters"}
            return {"original": value, "suggestion": suggested, "confidence": 0.4, "source": "Online AI", "details": "Name requires manual review"}

        if field_type in ("jobtitle", "job_title"):
            is_valid, mapped, j_conf, j_note = engine._validate_job_title(value)
            if mapped:
                return {"original": value, "suggestion": mapped, "confidence": max(j_conf, 0.90), "source": "Online AI", "details": j_note}
            choices = list(engine.job_title_map.keys()) if engine.job_title_map else []
            if choices:
                match, score, _ = rf_process.extractOne(value.strip(), choices, scorer=fuzz.token_sort_ratio)
                if score:
                    return {"original": value, "suggestion": engine.job_title_map.get(match, match), "confidence": max(score / 100.0, 0.80), "source": "Online AI", "details": f"Closest: '{match}' - {score}% match"}
            return {"original": value, "suggestion": "(No match found - manual review needed)", "confidence": 0.0, "source": "Online AI", "details": j_note}

        if field_type == "id":
            suggested = engine._suggest_id_fix(value)
            if str(suggested).isdigit():
                return {"original": value, "suggestion": suggested, "confidence": 0.9, "source": "Online AI", "details": "Converted to positive integer"}
            return {"original": value, "suggestion": suggested, "confidence": 0.4, "source": "Online AI", "details": "ID requires manual review"}

        raise HTTPException(status_code=400, detail=f"Unsupported field type: {field_type}")

    except Exception as e:
        return {"original": value, "suggestion": value, "confidence": 0.0, "source": "Online AI (Failed)", "details": f"Error: {str(e)}"}


@app.post("/verify-online")
async def verify_online(request: OnlineVerifyRequest):
    field_type = request.field_type.lower()
    value = request.value.strip()

    if not value:
        raise HTTPException(status_code=400, detail="Value cannot be empty")

    try:
        if field_type == "email":
            result = await verify_email_online(value)
        elif field_type == "phone":
            result = await verify_phone_online(value)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported field type: {field_type}")

        return {
            "original": value,
            "verified": result["verified"],
            "suggestion": result.get("suggestion", value),
            "confidence": result.get("confidence", 0.0),
            "source": "Online API",
            "details": result.get("details", "Verified via external API"),
        }
    except Exception as e:
        return {"original": value, "verified": False, "suggestion": value, "confidence": 0.0, "source": "Online API (Failed)", "details": f"Error: {str(e)}"}


async def verify_email_online(email: str) -> dict:
    import re
    from email_validator import validate_email, EmailNotValidError

    API_KEY = os.getenv("ABSTRACT_API_KEY", "")

    if not API_KEY:
        cleaned = email.strip()
        if cleaned.count("@") > 1:
            parts = cleaned.split("@")
            cleaned = parts[0] + "@" + "".join(parts[1:])
        if "@" in cleaned:
            local, domain = cleaned.split("@", 1)
            domain = re.sub(r"[^a-zA-Z0-9.-]", "", domain)
            local = re.sub(r"[^a-zA-Z0-9._+-]", "", local)
            cleaned = f"{local}@{domain}"
        if "@" in cleaned:
            local, domain = cleaned.split("@", 1)
            if "." not in domain and domain:
                cleaned = f"{local}@{domain}.com"
        try:
            info = validate_email(cleaned, check_deliverability=False)
            return {"verified": True, "suggestion": info.normalized, "confidence": 0.92, "details": f"Cleaned: {email} → {info.normalized}"}
        except EmailNotValidError:
            return {"verified": False, "suggestion": cleaned, "confidence": 0.65, "details": "Cleaned but format still invalid"}

    try:
        url = f"https://emailvalidation.abstractapi.com/v1/?api_key={API_KEY}&email={email}"
        response = requests.get(url, timeout=5)
        data = response.json()
        is_valid = data.get("deliverability") == "DELIVERABLE" and data.get("is_valid_format", {}).get("value", False)
        return {"verified": is_valid, "suggestion": data.get("autocorrect", email) if is_valid else email, "confidence": 0.95 if is_valid else 0.3, "details": f"Deliverability: {data.get('deliverability', 'unknown')}"}
    except Exception as e:
        return {"verified": False, "suggestion": email, "confidence": 0.0, "details": f"API Error: {str(e)}"}


async def verify_phone_online(phone: str) -> dict:
    import re

    API_KEY = os.getenv("ABSTRACT_API_KEY", "")
    digits = re.sub(r"\D", "", phone)

    if not API_KEY:
        if 10 <= len(digits) <= 15:
            formatted = f"+{digits}"
            return {"verified": True, "suggestion": formatted, "confidence": 0.90, "details": f"Cleaned: {phone} → {formatted}"}
        return {"verified": False, "suggestion": phone, "confidence": 0.30, "details": f"Invalid: {len(digits)} digits (need 10-15)"}

    try:
        url = f"https://phonevalidation.abstractapi.com/v1/?api_key={API_KEY}&phone={phone}"
        response = requests.get(url, timeout=5)
        data = response.json()
        is_valid = data.get("valid", False)
        formatted = data.get("format", {}).get("international", phone) if is_valid else phone
        return {"verified": is_valid, "suggestion": formatted, "confidence": 0.95 if is_valid else 0.3, "details": f"Country: {data.get('country', {}).get('name', 'unknown')}"}
    except Exception as e:
        return {"verified": False, "suggestion": phone, "confidence": 0.0, "details": f"API Error: {str(e)}"}


@app.get("/report")
async def get_report():
    if last_report is None:
        raise HTTPException(status_code=404, detail="No report available. Upload first.")
    return last_report
