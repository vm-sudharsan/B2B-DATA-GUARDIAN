from __future__ import annotations

from io import BytesIO
from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd
import re
from email_validator import EmailNotValidError, validate_email

from ai.inference import get_inference_engine


class AIDataQualityEngine:
    def __init__(self):
        self.ai_engine = get_inference_engine()
        self.accept_threshold = 0.80
        self.suggest_threshold = 0.60

    def process_csv(self, file_bytes: bytes, data_type: str = "people") -> Dict[str, Any]:
        df = pd.read_csv(BytesIO(file_bytes))
        return self._process_dataframe(df, data_type=data_type)

    def process_excel(self, file_bytes: bytes, data_type: str = "people") -> Dict[str, Any]:
        df = pd.read_excel(BytesIO(file_bytes))
        return self._process_dataframe(df, data_type=data_type)

    def _process_dataframe(self, df: pd.DataFrame, data_type: str = "people") -> Dict[str, Any]:
        df = self._normalize_columns(df)
        df = df.replace({"": np.nan, " ": np.nan})

        fixes: List[Dict[str, Any]] = []
        invalid_count = 0
        standardized_count = 0
        offline_fixes = 0
        online_fixes = 0
        manual_review = 0
        anomaly_count = 0
        low_confidence_count = 0

        missing_records = []
        invalid_records = []
        duplicate_records = []
        anomaly_records = []
        low_confidence_records = []

        duplicate_flags, duplicate_count = self._detect_duplicates_ml(df, data_type)
        df["is_duplicate"] = duplicate_flags

        for idx, is_dup in enumerate(duplicate_flags):
            if is_dup:
                duplicate_records.append({"row_index": idx})

        for idx, row in df.iterrows():
            if "job_title" in df.columns or "jobtitle" in df.columns:
                job_field = "job_title" if "job_title" in df.columns else "jobtitle"
                job_val = row.get(job_field, "")

                if pd.notna(job_val):
                    result = self.ai_engine.classify_job_title(str(job_val))
                    predicted_role = result["predicted_role"]
                    confidence = result["confidence_score"]
                    df.at[idx, "job_role_normalized"] = predicted_role

                    if confidence < self.suggest_threshold:
                        low_confidence_count += 1
                        low_confidence_records.append({"row_index": idx, "field": job_field, "value": job_val, "prediction": predicted_role, "confidence": confidence})
                        fixes.append(self._make_fix(idx, job_field, job_val, predicted_role, confidence, "MANUAL", f"Low confidence: {'; '.join(result['explanation'])}"))
                        manual_review += 1
                    elif confidence < self.accept_threshold:
                        fixes.append(self._make_fix(idx, job_field, job_val, predicted_role, confidence, "ONLINE", f"ML prediction: {'; '.join(result['explanation'])}"))
                        online_fixes += 1
                    else:
                        fixes.append(self._make_fix(idx, job_field, job_val, predicted_role, confidence, "OFFLINE", f"ML prediction: {'; '.join(result['explanation'])}"))
                        offline_fixes += 1
                        standardized_count += 1

            if "email" in df.columns or "people_email" in df.columns:
                email_field = "email" if "email" in df.columns else "people_email"
                email_val = row.get(email_field, "")

                if pd.notna(email_val):
                    is_valid_format = self._validate_email_format(str(email_val))
                    if not is_valid_format:
                        invalid_count += 1
                        invalid_records.append({"row_index": idx, "field": email_field, "value": email_val, "issue": "Invalid email format"})
                        suggestion = self._suggest_email_fix_ml(str(email_val))
                        fixes.append(self._make_fix(idx, email_field, email_val, suggestion, 0.0, "MANUAL", "Invalid format - needs verification"))
                        manual_review += 1
                    else:
                        anomaly_result = self.ai_engine.detect_anomaly(email_field, str(email_val))
                        if anomaly_result["is_suspicious"]:
                            anomaly_count += 1
                            anomaly_records.append({"row_index": idx, "field": email_field, "value": email_val, "anomaly_score": anomaly_result["anomaly_score"], "reason": "; ".join(anomaly_result["explanation"])})
                            fixes.append(self._make_fix(idx, email_field, email_val, email_val, 1.0 - anomaly_result["anomaly_score"], "ONLINE", f"Anomaly: {'; '.join(anomaly_result['explanation'])}"))
                            online_fixes += 1
                elif pd.isna(email_val):
                    missing_records.append({"row_index": idx, "field": email_field, "issue": "Missing"})

            if "phone" in df.columns or "people_phone" in df.columns:
                phone_field = "phone" if "phone" in df.columns else "people_phone"
                phone_val = row.get(phone_field, "")

                if pd.notna(phone_val):
                    is_valid, cleaned_phone, p_conf, p_note = self._validate_phone_strict(str(phone_val))
                    if not is_valid:
                        invalid_count += 1
                        invalid_records.append({"row_index": idx, "field": phone_field, "value": phone_val, "issue": p_note})
                        fixes.append(self._make_fix(idx, phone_field, phone_val, cleaned_phone, 0.0, "MANUAL", p_note))
                        manual_review += 1
                    elif cleaned_phone != phone_val:
                        standardized_count += 1
                        fixes.append(self._make_fix(idx, phone_field, phone_val, cleaned_phone, p_conf, "OFFLINE", p_note))
                        offline_fixes += 1
                elif pd.isna(phone_val):
                    missing_records.append({"row_index": idx, "field": phone_field, "issue": "Missing"})

            for field in ["country", "industry"]:
                if field not in df.columns:
                    continue
                value = row.get(field, "")
                if pd.notna(value) and str(value).strip():
                    correction_result = self.ai_engine.suggest_correction(f"{field}s", str(value))
                    suggested = correction_result["suggested_value"]
                    confidence = correction_result["similarity_confidence"]
                    if suggested != value and confidence >= self.suggest_threshold:
                        standardized_count += 1
                        mode = "OFFLINE" if confidence >= self.accept_threshold else "ONLINE"
                        fixes.append(self._make_fix(idx, field, value, suggested, confidence, mode, f"ML match: {'; '.join(correction_result['explanation'])}"))
                        if mode == "OFFLINE":
                            offline_fixes += 1
                        else:
                            online_fixes += 1
                elif pd.isna(value):
                    missing_records.append({"row_index": idx, "field": field, "issue": "Missing"})

        stats = {
            "total_records": len(df),
            "missing_fields": len(missing_records),
            "invalid_fields": invalid_count,
            "anomalies": anomaly_count,
            "duplicates": duplicate_count,
            "low_confidence_fixes": low_confidence_count,
        }
        quality_result = self.ai_engine.compute_quality_score(stats)

        report = {
            "missing_fields": len(missing_records),
            "invalid_fields": invalid_count,
            "duplicate_rows": duplicate_count,
            "standardized_fields": standardized_count,
            "offline_fixes": offline_fixes,
            "online_fixes": online_fixes,
            "manual_review": manual_review,
            "anomalies_detected": anomaly_count,
            "low_confidence_predictions": low_confidence_count,
            "overall_quality_score": quality_result["quality_score"],
            "quality_breakdown": quality_result["breakdown"],
            "quality_explanation": quality_result["explanation"],
            "records": len(df),
            "total_columns": df.shape[1],
            "all_columns": list(df.columns),
            "missing_per_column": df.isnull().sum().to_dict(),
            "ai_powered": True,
        }

        cleaned_data = df.drop(columns=["is_duplicate"], errors="ignore").to_dict(orient="records")

        return {
            "report": report,
            "cleaned_data": cleaned_data,
            "fixes": fixes,
            "missing_records": missing_records,
            "invalid_records": invalid_records,
            "duplicate_records": duplicate_records,
            "anomaly_records": anomaly_records,
            "low_confidence_records": low_confidence_records,
        }

    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(columns={c: c.strip().lower() for c in df.columns})

    def _detect_duplicates_ml(self, df: pd.DataFrame, data_type: str) -> Tuple[List[bool], int]:
        flags = [False] * len(df)
        duplicate_count = 0
        seen_indices = set()

        for i in range(len(df)):
            if i in seen_indices:
                continue
            for j in range(i + 1, len(df)):
                if j in seen_indices:
                    continue
                result = self.ai_engine.detect_duplicate_probability(df.iloc[i].to_dict(), df.iloc[j].to_dict())
                if result["duplicate_probability"] >= 0.75:
                    flags[j] = True
                    seen_indices.add(j)
                    duplicate_count += 1

        return flags, duplicate_count

    def _validate_email_format(self, email: str) -> bool:
        if not email or email.count("@") != 1:
            return False
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False

    def _suggest_email_fix_ml(self, email: str) -> str:
        email = str(email).strip()
        if email.count("@") > 1:
            parts = email.split("@")
            email = parts[0] + "@" + "".join(parts[1:])
        if "@" in email:
            local, domain = email.split("@", 1)
            domain = re.sub(r"[^a-zA-Z0-9.-]", "", domain)
            local = re.sub(r"[^a-zA-Z0-9._+-]", "", local)
            email = f"{local}@{domain}"
        if "@" in email:
            local, domain = email.split("@", 1)
            if "." not in domain and domain:
                email = f"{local}@{domain}.com"
        return email

    def _validate_phone_strict(self, phone: str) -> Tuple[bool, str, float, str]:
        if not phone:
            return False, "", 0.0, "Phone number missing"
        digits = re.sub(r"\D", "", phone)
        if len(digits) < 10:
            return False, phone, 0.0, f"Invalid: only {len(digits)} digits (need 10+)"
        if len(digits) > 15:
            return False, phone, 0.0, f"Invalid: too many digits ({len(digits)})"
        formatted = "+" + digits
        if formatted != phone:
            return True, formatted, 0.85, "Standardized format"
        return True, phone, 1.0, "Valid"

    def _make_fix(self, row_index: int, field: str, original: Any, suggested: Any, confidence: float, processing_mode: str, note: str) -> Dict[str, Any]:
        return {
            "row_index": int(row_index),
            "field": field,
            "original": original,
            "suggested": suggested,
            "confidence": round(confidence, 3),
            "processing_mode": processing_mode,
            "note": note,
            "ai_powered": True,
        }
