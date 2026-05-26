# Phishing Email Detection Web App

A simple phishing email detector built with Python, scikit-learn, and Flask.

## Features
- Trains on a labeled dataset of phishing and legitimate emails
- Extracts email features such as URLs, keywords, suspicious domains, uppercase usage, and punctuation
- Displays accuracy and confusion matrix after training
- Provides a web interface for testing new emails

## Setup
1. Open a terminal in `d:\thiranex-3`
2. Create and activate a Python environment
   - `python -m venv .venv`
   - `.venv\Scripts\activate`
3. Install dependencies
   - `pip install -r requirements.txt`
4. Train the model
   - `python train_model.py`
5. Start the web app
   - `python app.py`
6. Open your browser at `http://localhost:5000`

## Notes
- The app reads sample data from `data/emails.csv`
- Training metrics are saved to `model/metrics.json`
- The prediction API is available at `/predict`
