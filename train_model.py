import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from features import extract_features

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / 'model'
DATA_FILE = BASE_DIR / 'data' / 'emails.csv'
MODEL_FILE = MODEL_DIR / 'phishing_model.pkl'
METRICS_FILE = MODEL_DIR / 'metrics.json'


def load_dataset():
    df = pd.read_csv(DATA_FILE)
    df = df.dropna(subset=['email_text', 'label'])
    return df


def build_features(dataframe):
    X = [extract_features(text) for text in dataframe['email_text'].astype(str)]
    y = [1 if label.strip().lower() == 'phishing' else 0 for label in dataframe['label']]
    return X, y


def main():
    df = load_dataset()
    X, y = build_features(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ('vectorizer', DictVectorizer(sparse=False)),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')),
    ])
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred).tolist()
    report = classification_report(y_test, y_pred, target_names=['legitimate', 'phishing'], zero_division=0)

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_FILE)

    metrics = {
        'accuracy': round(float(accuracy), 4),
        'confusion_matrix': conf_matrix,
        'classification_report': report,
        'test_samples': len(y_test),
    }

    with METRICS_FILE.open('w', encoding='utf-8') as file:
        json.dump(metrics, file, indent=2)

    print('Model trained and saved to', MODEL_FILE)
    print('Metrics saved to', METRICS_FILE)
    print('Accuracy:', metrics['accuracy'])
    print('Confusion matrix:')
    print(metrics['confusion_matrix'])
    print('\nClassification report:\n', metrics['classification_report'])


if __name__ == '__main__':
    main()
