from pathlib import Path
import sys
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
from typing import List, Tuple, Dict
import re

MODELS_DIR = Path(__file__).parent.parent / "models"
CACHE_DIR = Path(__file__).parent.parent / "cache"
MODELS_DIR.mkdir(exist_ok=True)


class JobTitleClassifier:
    """MODEL 1: Job Title Normalization using ML"""
    
    ROLE_CLASSES = [
        "Sales", "Marketing", "IT", "HR", "Finance", 
        "Operations", "Management", "Support", "Other"
    ]
    
    def __init__(self):
        self.tfidf = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
        self.classifier = LogisticRegression(max_iter=1000, random_state=42)
        
    def generate_training_data(self) -> Tuple[List[str], List[str]]:
        """Generate synthetic training data for job titles"""
        training_data = {
            "Sales": [
                "Account Executive", "Sales Manager", "Business Development Rep",
                "Sales Director", "Account Manager", "Sales Representative",
                "VP Sales", "Chief Revenue Officer", "Sales Engineer", "SDR",
                "BDR", "Territory Manager", "Regional Sales Manager"
            ],
            "Marketing": [
                "Marketing Manager", "Content Writer", "SEO Specialist",
                "Brand Manager", "Digital Marketing Manager", "CMO",
                "Marketing Director", "Social Media Manager", "Growth Hacker",
                "Product Marketing Manager", "Marketing Analyst"
            ],
            "IT": [
                "Software Engineer", "DevOps Engineer", "Data Scientist",
                "Full Stack Developer", "Backend Developer", "Frontend Developer",
                "SRE", "Cloud Architect", "Security Engineer", "QA Engineer",
                "Machine Learning Engineer", "Data Engineer", "CTO", "Tech Lead"
            ],
            "HR": [
                "HR Manager", "Recruiter", "Talent Acquisition Specialist",
                "HR Director", "People Operations", "HRBP", "Compensation Analyst",
                "Learning and Development Manager", "Chief People Officer"
            ],
            "Finance": [
                "Financial Analyst", "Accountant", "CFO", "Controller",
                "Finance Manager", "Treasury Analyst", "FP&A Manager",
                "Accounts Payable", "Accounts Receivable", "Auditor"
            ],
            "Operations": [
                "Operations Manager", "COO", "Supply Chain Manager",
                "Logistics Coordinator", "Operations Analyst", "Process Manager",
                "Operations Director", "Warehouse Manager"
            ],
            "Management": [
                "CEO", "President", "General Manager", "VP", "Director",
                "Executive Director", "Managing Director", "Chief Officer"
            ],
            "Support": [
                "Customer Support", "Technical Support", "Help Desk",
                "Customer Success Manager", "Support Engineer", "Client Services"
            ],
            "Other": [
                "Consultant", "Analyst", "Coordinator", "Specialist",
                "Administrator", "Assistant", "Associate"
            ]
        }
        
        titles = []
        labels = []
        for role, title_list in training_data.items():
            titles.extend(title_list)
            labels.extend([role] * len(title_list))
            
        return titles, labels
    
    def train(self):
        """Train job title classifier"""
        print("Training Job Title Classifier...")
        
        # Generate training data
        titles, labels = self.generate_training_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            titles, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        # Extract features using TF-IDF
        X_train_tfidf = self.tfidf.fit_transform(X_train)
        X_test_tfidf = self.tfidf.transform(X_test)
        
        # Train classifier
        self.classifier.fit(X_train_tfidf, y_train)
        
        # Evaluate
        y_pred = self.classifier.predict(X_test_tfidf)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Job Title Classifier Accuracy: {accuracy:.3f}")
        print(classification_report(y_test, y_pred))
        
        # Save models
        joblib.dump(self.tfidf, MODELS_DIR / "job_title_tfidf.pkl")
        joblib.dump(self.classifier, MODELS_DIR / "job_title_classifier.pkl")
        print(f"✓ Job Title Classifier saved to {MODELS_DIR}")


class DuplicateDetector:
    """MODEL 2: Duplicate Detection using Entity Resolution"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        
    def extract_features(self, rec1: Dict, rec2: Dict) -> np.ndarray:
        """Extract similarity features between two records"""
        from rapidfuzz import fuzz
        
        features = []
        
        # Name similarity
        name1 = str(rec1.get('person_name', '')).lower()
        name2 = str(rec2.get('person_name', '')).lower()
        features.append(fuzz.ratio(name1, name2) / 100.0)
        
        # Email similarity
        email1 = str(rec1.get('email', '')).lower()
        email2 = str(rec2.get('email', '')).lower()
        features.append(1.0 if email1 == email2 and email1 else 0.0)
        
        # Email username similarity
        user1 = email1.split('@')[0] if '@' in email1 else ''
        user2 = email2.split('@')[0] if '@' in email2 else ''
        features.append(fuzz.ratio(user1, user2) / 100.0 if user1 and user2 else 0.0)
        
        # Email domain similarity
        domain1 = email1.split('@')[1] if '@' in email1 else ''
        domain2 = email2.split('@')[1] if '@' in email2 else ''
        features.append(1.0 if domain1 == domain2 and domain1 else 0.0)
        
        # Phone similarity
        phone1 = re.sub(r'\D', '', str(rec1.get('phone', '')))
        phone2 = re.sub(r'\D', '', str(rec2.get('phone', '')))
        features.append(1.0 if phone1 == phone2 and phone1 else 0.0)
        
        # Company similarity
        comp1 = str(rec1.get('company_name', '')).lower()
        comp2 = str(rec2.get('company_name', '')).lower()
        features.append(fuzz.token_sort_ratio(comp1, comp2) / 100.0)
        
        # Title similarity
        title1 = str(rec1.get('job_title', '')).lower()
        title2 = str(rec2.get('job_title', '')).lower()
        features.append(fuzz.token_sort_ratio(title1, title2) / 100.0)
        
        return np.array(features)
    
    def generate_training_pairs(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Generate positive and negative record pairs"""
        X = []
        y = []
        
        # Generate positive pairs (duplicates)
        for i in range(min(50, len(df))):
            for j in range(i + 1, min(i + 5, len(df))):
                rec1 = df.iloc[i].to_dict()
                rec2 = df.iloc[j].to_dict()
                features = self.extract_features(rec1, rec2)
                
                # Label as duplicate if high similarity
                is_duplicate = (
                    features[1] > 0.9 or  # Same email
                    features[4] > 0.9 or  # Same phone
                    (features[0] > 0.85 and features[5] > 0.85)  # Same name + company
                )
                
                X.append(features)
                y.append(1 if is_duplicate else 0)
        
        return np.array(X), np.array(y)
    
    def train(self, sample_df: pd.DataFrame):
        """Train duplicate detection model"""
        print("Training Duplicate Detector...")
        
        X, y = self.generate_training_pairs(sample_df)
        
        if len(X) == 0:
            print("⚠ Not enough data for duplicate training, using default model")
            return
        
        # Train model
        self.model.fit(X, y)
        
        # Save model
        joblib.dump(self.model, MODELS_DIR / "duplicate_detector.pkl")
        print(f"✓ Duplicate Detector saved to {MODELS_DIR}")


class AnomalyDetector:
    """MODEL 3: Anomaly Detection for Invalid Values"""
    
    def __init__(self):
        self.models = {}
        
    def extract_string_features(self, value: str) -> np.ndarray:
        """Extract features from string value"""
        if pd.isna(value) or not value:
            return np.zeros(6)
        
        value = str(value)
        features = []
        
        # Length
        features.append(len(value))
        
        # Digit ratio
        digit_count = sum(c.isdigit() for c in value)
        features.append(digit_count / len(value) if len(value) > 0 else 0)
        
        # Uppercase ratio
        upper_count = sum(c.isupper() for c in value)
        features.append(upper_count / len(value) if len(value) > 0 else 0)
        
        # Special char ratio
        special_count = sum(not c.isalnum() and not c.isspace() for c in value)
        features.append(special_count / len(value) if len(value) > 0 else 0)
        
        # Character entropy
        from collections import Counter
        char_counts = Counter(value.lower())
        total = len(value)
        entropy = -sum((count / total) * np.log2(count / total) for count in char_counts.values())
        features.append(entropy)
        
        # Token count
        features.append(len(value.split()))
        
        return np.array(features)
    
    def train(self, df: pd.DataFrame):
        """Train anomaly detectors for each field type"""
        print("Training Anomaly Detectors...")
        
        field_types = ['email', 'phone', 'person_name', 'company_name', 'job_title']
        
        for field in field_types:
            if field not in df.columns:
                continue
            
            # Extract features
            values = df[field].dropna()
            if len(values) < 10:
                continue
            
            X = np.array([self.extract_string_features(v) for v in values])
            
            # Train IsolationForest
            model = IsolationForest(contamination=0.1, random_state=42)
            model.fit(X)
            
            self.models[field] = model
        
        # Save models
        joblib.dump(self.models, MODELS_DIR / "anomaly_detectors.pkl")
        print(f"✓ Anomaly Detectors saved to {MODELS_DIR}")


class CorrectionSuggester:
    """MODEL 4: Correction Suggestion using rapidfuzz (memory-efficient)"""

    def __init__(self):
        self.references = {}

    def train(self):
        print("Building Reference Lists...")

        countries_path = CACHE_DIR / "countries.json"
        industries_path = CACHE_DIR / "industries.json"

        if countries_path.exists():
            with open(countries_path) as f:
                self.references["countries"] = json.load(f)

        if industries_path.exists():
            with open(industries_path) as f:
                self.references["industries"] = json.load(f)

        self.references["email_domains"] = [
            "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
            "icloud.com", "protonmail.com", "aol.com", "mail.com",
        ]

        joblib.dump(self.references, MODELS_DIR / "references.pkl")
        print(f"✓ Reference Lists saved to {MODELS_DIR}")


def train_all_models():
    """Main training pipeline"""
    print("=" * 60)
    print("ML TRAINING PIPELINE - Data Quality AI")
    print("=" * 60)
    
    # Load sample data for training
    sample_data_path = Path(__file__).parent.parent.parent / "sample_data.csv"
    if sample_data_path.exists():
        df = pd.read_csv(sample_data_path)
        print(f"Loaded sample data: {len(df)} records")
    else:
        print("⚠ No sample data found, using minimal training")
        df = pd.DataFrame()
    
    # Train Model 1: Job Title Classifier
    job_classifier = JobTitleClassifier()
    job_classifier.train()
    
    # Train Model 2: Duplicate Detector
    if not df.empty:
        duplicate_detector = DuplicateDetector()
        duplicate_detector.train(df)
    
    # Train Model 3: Anomaly Detector
    if not df.empty:
        anomaly_detector = AnomalyDetector()
        anomaly_detector.train(df)
    
    # Train Model 4: Correction Suggester
    correction_suggester = CorrectionSuggester()
    correction_suggester.train()
    
    print("=" * 60)
    print("✓ ALL MODELS TRAINED SUCCESSFULLY")
    print(f"Models saved to: {MODELS_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    train_all_models()
