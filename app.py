import json
from pathlib import Path

import joblib
from flask import Flask, jsonify, render_template, request

from features import extract_features

BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / 'model' / 'phishing_model.pkl'
METRICS_FILE = BASE_DIR / 'model' / 'metrics.json'

app = Flask(__name__)
model = None

if MODEL_FILE.exists():
    model = joblib.load(MODEL_FILE)
else:
    print('Warning: model file not found. Run python train_model.py first.')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not available. Run python train_model.py first.'}), 500

    data = request.get_json(force=True)
    email_text = data.get('email_text', '')
    features = extract_features(email_text)
    label_code = model.predict([features])[0]
    probability = model.predict_proba([features])[0][1]
    label = 'phishing' if label_code == 1 else 'legitimate'

    return jsonify({
        'label': label,
        'probability': round(float(probability), 4),
        'feature_summary': features,
    })


@app.route('/metrics', methods=['GET'])
def metrics():
    if not METRICS_FILE.exists():
        return jsonify({'error': 'Metrics not available. Run python train_model.py first.'}), 404

    with METRICS_FILE.open('r', encoding='utf-8') as file:
        metrics_data = json.load(file)
    return jsonify(metrics_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
