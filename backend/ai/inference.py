from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from typing import Dict, Any
import re

MODELS_DIR = Path(__file__).parent.parent / "models"
CACHE_DIR = Path(__file__).parent.parent / "cache"


class AIInferenceEngine:
    def __init__(self):
        self.models_loaded = False
        self.job_title_tfidf = None
        self.job_title_classifier = None
        self.duplicate_detector = None
        self.anomaly_detectors = None
        self.references = {}

    def load_models(self):
        if self.models_loaded:
            return
        try:
            tfidf_path = MODELS_DIR / "job_title_tfidf.pkl"
            classifier_path = MODELS_DIR / "job_title_classifier.pkl"
            if tfidf_path.exists() and classifier_path.exists():
                self.job_title_tfidf = joblib.load(tfidf_path)
                self.job_title_classifier = joblib.load(classifier_path)
                print("✓ Job Title Classifier loaded")

            dup_path = MODELS_DIR / "duplicate_detector.pkl"
            if dup_path.exists():
                self.duplicate_detector = joblib.load(dup_path)
                print("✓ Duplicate Detector loaded")

            anomaly_path = MODELS_DIR / "anomaly_detectors.pkl"
            if anomaly_path.exists():
                self.anomaly_detectors = joblib.load(anomaly_path)
                print("✓ Anomaly Detectors loaded")

            references_path = MODELS_DIR / "references.pkl"
            if references_path.exists():
                self.references = joblib.load(references_path)
                print(f"✓ References loaded: {list(self.references.keys())}")

            self.models_loaded = True
            print("✓ All models loaded successfully")
        except Exception as e:
            print(f"⚠ Error loading models: {e}")
            self.models_loaded = False

    def classify_job_title(self, title: str) -> Dict[str, Any]:
        if not self.job_title_classifier or not self.job_title_tfidf:
            return {"original_title": title, "predicted_role": "Other", "confidence_score": 0.0, "explanation": ["Models not loaded"]}
        try:
            title_tfidf = self.job_title_tfidf.transform([title])
            predicted_role = self.job_title_classifier.predict(title_tfidf)[0]
            probabilities = self.job_title_classifier.predict_proba(title_tfidf)[0]
            confidence = float(max(probabilities))
            classes = self.job_title_classifier.classes_
            top_indices = np.argsort(probabilities)[-3:][::-1]
            top_predictions = [(classes[i], probabilities[i]) for i in top_indices]
            explanation = [
                f"Top prediction: {predicted_role} ({confidence:.2%})",
                f"Alternatives: {', '.join([f'{c} ({p:.1%})' for c, p in top_predictions[1:]])}",
            ]
            return {"original_title": title, "predicted_role": predicted_role, "confidence_score": round(confidence, 3), "explanation": explanation}
        except Exception as e:
            return {"original_title": title, "predicted_role": "Other", "confidence_score": 0.0, "explanation": [f"Error: {str(e)}"]}

    def detect_duplicate_probability(self, rec1: Dict, rec2: Dict) -> Dict[str, Any]:
        if not self.duplicate_detector:
            from rapidfuzz import fuzz
            email1 = str(rec1.get("email", "")).lower()
            email2 = str(rec2.get("email", "")).lower()
            if email1 and email2 and email1 == email2:
                return {"recordA_id": rec1.get("id", 0), "recordB_id": rec2.get("id", 1), "duplicate_probability": 0.95, "explanation": ["Same email address"]}
            return {"recordA_id": rec1.get("id", 0), "recordB_id": rec2.get("id", 1), "duplicate_probability": 0.0, "explanation": ["Fallback: no model"]}
        try:
            features = self._extract_duplicate_features(rec1, rec2)
            proba = self.duplicate_detector.predict_proba([features])[0][1]
            feature_names = ["name_sim", "email_match", "email_user_sim", "email_domain", "phone_match", "company_sim", "title_sim"]
            explanation = [f"{n}: {v:.2f}" for n, v in zip(feature_names, features) if v > 0.7] or ["Low similarity"]
            return {"recordA_id": rec1.get("id", 0), "recordB_id": rec2.get("id", 1), "duplicate_probability": round(float(proba), 3), "explanation": explanation}
        except Exception as e:
            return {"recordA_id": rec1.get("id", 0), "recordB_id": rec2.get("id", 1), "duplicate_probability": 0.0, "explanation": [f"Error: {str(e)}"]}

    def _extract_duplicate_features(self, rec1: Dict, rec2: Dict) -> np.ndarray:
        from rapidfuzz import fuzz
        email1 = str(rec1.get("email", "")).lower()
        email2 = str(rec2.get("email", "")).lower()
        name1 = str(rec1.get("person_name", "")).lower()
        name2 = str(rec2.get("person_name", "")).lower()
        user1 = email1.split("@")[0] if "@" in email1 else ""
        user2 = email2.split("@")[0] if "@" in email2 else ""
        domain1 = email1.split("@")[1] if "@" in email1 else ""
        domain2 = email2.split("@")[1] if "@" in email2 else ""
        phone1 = re.sub(r"\D", "", str(rec1.get("phone", "")))
        phone2 = re.sub(r"\D", "", str(rec2.get("phone", "")))
        comp1 = str(rec1.get("company_name", "")).lower()
        comp2 = str(rec2.get("company_name", "")).lower()
        title1 = str(rec1.get("job_title", "")).lower()
        title2 = str(rec2.get("job_title", "")).lower()
        return np.array([
            fuzz.ratio(name1, name2) / 100.0,
            1.0 if email1 == email2 and email1 else 0.0,
            fuzz.ratio(user1, user2) / 100.0 if user1 and user2 else 0.0,
            1.0 if domain1 == domain2 and domain1 else 0.0,
            1.0 if phone1 == phone2 and phone1 else 0.0,
            fuzz.token_sort_ratio(comp1, comp2) / 100.0,
            fuzz.token_sort_ratio(title1, title2) / 100.0,
        ])

    def detect_anomaly(self, field: str, value: str) -> Dict[str, Any]:
        if not self.anomaly_detectors or field not in self.anomaly_detectors:
            return {"field": field, "value": value, "anomaly_score": 0.0, "is_suspicious": False, "explanation": ["No detector for this field"]}
        try:
            features = self._extract_string_features(value)
            score = self.anomaly_detectors[field].score_samples([features])[0]
            anomaly_score = 1.0 / (1.0 + np.exp(score))
            is_suspicious = anomaly_score > 0.6
            explanation = []
            if len(value) < 3:
                explanation.append("Very short value")
            if sum(c.isdigit() for c in value) / max(len(value), 1) > 0.5:
                explanation.append("High digit ratio")
            if sum(not c.isalnum() and not c.isspace() for c in value) / max(len(value), 1) > 0.3:
                explanation.append("Many special characters")
            if not explanation:
                explanation = ["Statistical outlier"]
            return {"field": field, "value": value, "anomaly_score": round(float(anomaly_score), 3), "is_suspicious": bool(is_suspicious), "explanation": explanation}
        except Exception as e:
            return {"field": field, "value": value, "anomaly_score": 0.0, "is_suspicious": False, "explanation": [f"Error: {str(e)}"]}

    def _extract_string_features(self, value: str) -> np.ndarray:
        if pd.isna(value) or not value:
            return np.zeros(6)
        value = str(value)
        from collections import Counter
        total = len(value)
        char_counts = Counter(value.lower())
        entropy = -sum((c / total) * np.log2(c / total) for c in char_counts.values())
        return np.array([
            total,
            sum(c.isdigit() for c in value) / total,
            sum(c.isupper() for c in value) / total,
            sum(not c.isalnum() and not c.isspace() for c in value) / total,
            entropy,
            len(value.split()),
        ])

    def suggest_correction(self, field_type: str, value: str, top_k: int = 3) -> Dict[str, Any]:
        if field_type not in self.references:
            return {"original_value": value, "suggested_value": value, "similarity_confidence": 0.0, "explanation": ["No reference data"]}
        try:
            from rapidfuzz import process as rf_process, fuzz
            ref_list = self.references[field_type]
            results = rf_process.extract(value, ref_list, scorer=fuzz.token_sort_ratio, limit=top_k)
            if not results:
                return {"original_value": value, "suggested_value": value, "similarity_confidence": 0.0, "explanation": ["No match found"]}
            best_match, best_score, _ = results[0]
            alternatives = [r[0] for r in results[1:]]
            confidence = round(best_score / 100.0, 3)
            return {
                "original_value": value,
                "suggested_value": best_match,
                "similarity_confidence": confidence,
                "explanation": [f"Closest match: {best_match}", f"Alternatives: {', '.join(alternatives)}"],
            }
        except Exception as e:
            return {"original_value": value, "suggested_value": value, "similarity_confidence": 0.0, "explanation": [f"Error: {str(e)}"]}

    def compute_quality_score(self, stats: Dict[str, int]) -> Dict[str, Any]:
        total = max(stats.get("total_records", 1), 1)
        w = 0.20
        penalties = [
            (stats.get("missing_fields", 0) / total) * w,
            (stats.get("invalid_fields", 0) / total) * w,
            (stats.get("anomalies", 0) / total) * w,
            (stats.get("duplicates", 0) / total) * w,
            (stats.get("low_confidence_fixes", 0) / total) * w,
        ]
        total_penalty = sum(penalties)
        quality_score = max(0, min(100, 100 - (total_penalty * 100)))
        breakdown = {
            "missing_fields_impact": round(penalties[0] * 100, 2),
            "invalid_format_impact": round(penalties[1] * 100, 2),
            "anomaly_impact": round(penalties[2] * 100, 2),
            "duplicate_impact": round(penalties[3] * 100, 2),
            "low_confidence_impact": round(penalties[4] * 100, 2),
        }
        if quality_score >= 90:
            label = "Excellent data quality"
        elif quality_score >= 75:
            label = "Good data quality with minor issues"
        elif quality_score >= 60:
            label = "Fair data quality, improvements needed"
        else:
            label = "Poor data quality, significant issues detected"
        explanation = [label]
        if stats.get("duplicates", 0) > 0:
            explanation.append(f"{stats['duplicates']} duplicate records found")
        if stats.get("anomalies", 0) > 0:
            explanation.append(f"{stats['anomalies']} anomalous values detected")
        return {"quality_score": round(quality_score, 2), "breakdown": breakdown, "explanation": explanation}


_inference_engine = None


def get_inference_engine() -> AIInferenceEngine:
    global _inference_engine
    if _inference_engine is None:
        _inference_engine = AIInferenceEngine()
        _inference_engine.load_models()
    return _inference_engine
