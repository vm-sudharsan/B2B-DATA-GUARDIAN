from pathlib import Path
import sys
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, f1_score
import joblib
from typing import List, Tuple, Dict
import re

MODELS_DIR = Path(__file__).parent.parent / "models"
CACHE_DIR = Path(__file__).parent.parent / "cache"

sys.path.insert(0, str(Path(__file__).parent.parent))
CACHE_DIR = Path(__file__).parent.parent / "cache"
MODELS_DIR.mkdir(exist_ok=True)


class EnhancedJobTitleClassifier:
    """Enhanced Job Title Classifier with more training data"""
    
    ROLE_CLASSES = [
        "Sales", "Marketing", "IT", "HR", "Finance", 
        "Operations", "Management", "Support", "Legal", "Other"
    ]
    
    def __init__(self):
        self.tfidf = TfidfVectorizer(max_features=200, ngram_range=(1, 3))
        self.classifier = GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        
    def generate_training_data(self) -> Tuple[List[str], List[str]]:
        """Generate comprehensive training data for B2B job titles"""
        training_data = {
            "Sales": [
                "Account Executive", "Sales Manager", "Business Development Rep",
                "Sales Director", "Account Manager", "Sales Representative",
                "VP Sales", "Chief Revenue Officer", "Sales Engineer", "SDR",
                "BDR", "Territory Manager", "Regional Sales Manager",
                "Inside Sales Rep", "Outside Sales Rep", "Sales Consultant",
                "Key Account Manager", "Enterprise Sales", "Channel Sales Manager",
                "Sales Operations Manager", "Revenue Operations", "Sales Enablement"
            ],
            "Marketing": [
                "Marketing Manager", "Content Writer", "SEO Specialist",
                "Brand Manager", "Digital Marketing Manager", "CMO",
                "Marketing Director", "Social Media Manager", "Growth Hacker",
                "Product Marketing Manager", "Marketing Analyst",
                "Content Marketing Manager", "Email Marketing Specialist",
                "Marketing Coordinator", "Demand Generation Manager",
                "Field Marketing Manager", "Marketing Operations",
                "Brand Strategist", "Creative Director", "Copywriter"
            ],
            "IT": [
                "Software Engineer", "DevOps Engineer", "Data Scientist",
                "Full Stack Developer", "Backend Developer", "Frontend Developer",
                "SRE", "Cloud Architect", "Security Engineer", "QA Engineer",
                "Machine Learning Engineer", "Data Engineer", "CTO", "Tech Lead",
                "Systems Administrator", "Network Engineer", "Database Administrator",
                "IT Manager", "Solutions Architect", "Platform Engineer",
                "Mobile Developer", "UI/UX Designer", "Product Engineer"
            ],
            "HR": [
                "HR Manager", "Recruiter", "Talent Acquisition Specialist",
                "HR Director", "People Operations", "HRBP", "Compensation Analyst",
                "Learning and Development Manager", "Chief People Officer",
                "HR Coordinator", "Talent Manager", "Employee Relations Manager",
                "Benefits Administrator", "HR Generalist", "Organizational Development",
                "Workforce Planning Manager", "HR Business Partner"
            ],
            "Finance": [
                "Financial Analyst", "Accountant", "CFO", "Controller",
                "Finance Manager", "Treasury Analyst", "FP&A Manager",
                "Accounts Payable", "Accounts Receivable", "Auditor",
                "Tax Manager", "Financial Controller", "Budget Analyst",
                "Investment Analyst", "Credit Analyst", "Payroll Manager",
                "Finance Director", "Revenue Analyst", "Cost Accountant"
            ],
            "Operations": [
                "Operations Manager", "COO", "Supply Chain Manager",
                "Logistics Coordinator", "Operations Analyst", "Process Manager",
                "Operations Director", "Warehouse Manager", "Procurement Manager",
                "Inventory Manager", "Operations Coordinator", "Facilities Manager",
                "Project Manager", "Program Manager", "Business Analyst"
            ],
            "Management": [
                "CEO", "President", "General Manager", "VP", "Director",
                "Executive Director", "Managing Director", "Chief Officer",
                "Head of Department", "Division Manager", "Regional Manager",
                "Country Manager", "Business Unit Leader", "Practice Lead"
            ],
            "Support": [
                "Customer Support", "Technical Support", "Help Desk",
                "Customer Success Manager", "Support Engineer", "Client Services",
                "Customer Service Representative", "Support Specialist",
                "Customer Experience Manager", "Client Support Manager",
                "Technical Support Engineer", "Customer Care Specialist"
            ],
            "Legal": [
                "Legal Counsel", "Attorney", "Paralegal", "Legal Manager",
                "General Counsel", "Compliance Officer", "Legal Director",
                "Contract Manager", "Legal Advisor", "Corporate Counsel",
                "Intellectual Property Manager", "Regulatory Affairs Manager"
            ],
            "Other": [
                "Consultant", "Analyst", "Coordinator", "Specialist",
                "Administrator", "Assistant", "Associate", "Advisor",
                "Executive Assistant", "Office Manager", "Researcher"
            ]
        }
        
        titles = []
        labels = []
        for role, title_list in training_data.items():
            titles.extend(title_list)
            labels.extend([role] * len(title_list))
            
        return titles, labels
    
    def train(self):
        """Train enhanced job title classifier"""
        print("Training Enhanced Job Title Classifier...")
        
        # Generate training data
        titles, labels = self.generate_training_data()
        print(f"Training samples: {len(titles)}")
        
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
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        print(f"✓ Accuracy: {accuracy:.3f}")
        print(f"✓ F1 Score: {f1:.3f}")
        print(classification_report(y_test, y_pred, zero_division=0))
        
        # Save models
        joblib.dump(self.tfidf, MODELS_DIR / "job_title_tfidf.pkl")
        joblib.dump(self.classifier, MODELS_DIR / "job_title_classifier.pkl")
        print(f"✓ Enhanced Job Title Classifier saved to {MODELS_DIR}")


class EnhancedDuplicateDetector:
    """Enhanced Duplicate Detection with better features"""
    
    def __init__(self):
        # Use RandomForest with more trees for better accuracy
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            class_weight='balanced'
        )
        
    def extract_features(self, rec1: Dict, rec2: Dict) -> np.ndarray:
        """Extract comprehensive similarity features"""
        from rapidfuzz import fuzz
        
        features = []
        
        # Name similarity (multiple algorithms)
        name1 = str(rec1.get('person_name', '') or rec1.get('company_name', '')).lower()
        name2 = str(rec2.get('person_name', '') or rec2.get('company_name', '')).lower()
        features.append(fuzz.ratio(name1, name2) / 100.0)
        features.append(fuzz.partial_ratio(name1, name2) / 100.0)
        features.append(fuzz.token_sort_ratio(name1, name2) / 100.0)
        
        # Email exact match
        email1 = str(rec1.get('email', '')).lower()
        email2 = str(rec2.get('email', '')).lower()
        features.append(1.0 if email1 == email2 and email1 else 0.0)
        
        # Email username similarity
        user1 = email1.split('@')[0] if '@' in email1 else ''
        user2 = email2.split('@')[0] if '@' in email2 else ''
        features.append(fuzz.ratio(user1, user2) / 100.0 if user1 and user2 else 0.0)
        
        # Email domain match
        domain1 = email1.split('@')[1] if '@' in email1 else ''
        domain2 = email2.split('@')[1] if '@' in email2 else ''
        features.append(1.0 if domain1 == domain2 and domain1 else 0.0)
        
        # Phone similarity
        phone1 = re.sub(r'\D', '', str(rec1.get('phone', '')))
        phone2 = re.sub(r'\D', '', str(rec2.get('phone', '')))
        features.append(1.0 if phone1 == phone2 and phone1 else 0.0)
        
        # Phone partial match (last 7 digits)
        if len(phone1) >= 7 and len(phone2) >= 7:
            features.append(1.0 if phone1[-7:] == phone2[-7:] else 0.0)
        else:
            features.append(0.0)
        
        # Company similarity
        comp1 = str(rec1.get('company_name', '')).lower()
        comp2 = str(rec2.get('company_name', '')).lower()
        features.append(fuzz.token_sort_ratio(comp1, comp2) / 100.0)
        
        # Title similarity
        title1 = str(rec1.get('job_title', '')).lower()
        title2 = str(rec2.get('job_title', '')).lower()
        features.append(fuzz.token_sort_ratio(title1, title2) / 100.0)
        
        # Website/domain similarity
        web1 = str(rec1.get('website', '') or rec1.get('domain', '')).lower()
        web2 = str(rec2.get('website', '') or rec2.get('domain', '')).lower()
        features.append(fuzz.ratio(web1, web2) / 100.0 if web1 and web2 else 0.0)
        
        return np.array(features)
    
    def generate_training_pairs(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Generate balanced positive and negative pairs"""
        X = []
        y = []
        
        # Generate positive pairs (duplicates)
        for i in range(min(100, len(df))):
            for j in range(i + 1, min(i + 10, len(df))):
                rec1 = df.iloc[i].to_dict()
                rec2 = df.iloc[j].to_dict()
                features = self.extract_features(rec1, rec2)
                
                # Label as duplicate if high similarity
                is_duplicate = (
                    features[3] > 0.9 or  # Same email
                    features[6] > 0.9 or  # Same phone
                    (features[0] > 0.85 and features[8] > 0.85)  # Same name + company
                )
                
                X.append(features)
                y.append(1 if is_duplicate else 0)
        
        return np.array(X), np.array(y)
    
    def train(self, sample_df: pd.DataFrame):
        """Train enhanced duplicate detection model"""
        print("Training Enhanced Duplicate Detector...")
        
        X, y = self.generate_training_pairs(sample_df)
        
        if len(X) == 0:
            print("⚠ Not enough data, using default model")
            return
        
        print(f"Training samples: {len(X)} (Duplicates: {sum(y)}, Non-duplicates: {len(y)-sum(y)})")
        
        # Train model
        self.model.fit(X, y)
        
        # Cross-validation score
        if len(X) > 10:
            cv_scores = cross_val_score(self.model, X, y, cv=min(5, len(X)//2))
            print(f"✓ Cross-validation accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
        
        # Save model
        joblib.dump(self.model, MODELS_DIR / "duplicate_detector.pkl")
        print(f"✓ Enhanced Duplicate Detector saved to {MODELS_DIR}")


def train_all_enhanced_models():
    """Main enhanced training pipeline"""
    print("=" * 60)
    print("ENHANCED ML TRAINING PIPELINE - B2B Customer Data")
    print("=" * 60)
    
    # Load sample data
    sample_data_path = Path(__file__).parent.parent.parent / "sample_data.csv"
    if sample_data_path.exists():
        df = pd.read_csv(sample_data_path)
        print(f"Loaded sample data: {len(df)} records")
    else:
        print("⚠ No sample data found, using minimal training")
        df = pd.DataFrame()
    
    # Train Enhanced Model 1: Job Title Classifier
    job_classifier = EnhancedJobTitleClassifier()
    job_classifier.train()
    
    # Train Enhanced Model 2: Duplicate Detector
    if not df.empty:
        duplicate_detector = EnhancedDuplicateDetector()
        duplicate_detector.train(df)
    
    from ml.train import AnomalyDetector, CorrectionSuggester
    
    # Train Model 3: Anomaly Detector
    if not df.empty:
        anomaly_detector = AnomalyDetector()
        anomaly_detector.train(df)
    
    # Train Model 4: Correction Suggester
    correction_suggester = CorrectionSuggester()
    correction_suggester.train()
    
    print("=" * 60)
    print("✓ ALL ENHANCED MODELS TRAINED SUCCESSFULLY")
    print(f"Models saved to: {MODELS_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    train_all_enhanced_models()
