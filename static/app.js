async function loadMetrics() {
  const metricsElement = document.getElementById('metrics');
  try {
    const response = await fetch('/metrics');
    if (!response.ok) {
      const errorData = await response.json();
      metricsElement.textContent = errorData.error || 'Unable to load metrics.';
      return;
    }
    const metrics = await response.json();
    metricsElement.innerHTML = `
      <p><strong>Accuracy:</strong> ${metrics.accuracy}</p>
      <p><strong>Test samples:</strong> ${metrics.test_samples}</p>
      <h3>Confusion matrix</h3>
      <table class="metric-table">
        <tr><th></th><th>Pred Legitimate</th><th>Pred Phishing</th></tr>
        <tr><th>True Legitimate</th><td>${metrics.confusion_matrix[0][0]}</td><td>${metrics.confusion_matrix[0][1]}</td></tr>
        <tr><th>True Phishing</th><td>${metrics.confusion_matrix[1][0]}</td><td>${metrics.confusion_matrix[1][1]}</td></tr>
      </table>
    `;
  } catch (error) {
    metricsElement.textContent = 'Error loading metrics.';
  }
}

async function submitEmail(event) {
  event.preventDefault();
  const textarea = document.getElementById('email_text');
  const predictionElement = document.getElementById('prediction');
  predictionElement.textContent = 'Analyzing...';

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email_text: textarea.value }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      predictionElement.textContent = errorData.error || 'Prediction failed.';
      return;
    }

    const result = await response.json();
    predictionElement.innerHTML = `
      <p><strong>Prediction:</strong> ${result.label}</p>
      <p><strong>Phishing probability:</strong> ${result.probability}</p>
      <p><strong>Features:</strong> ${JSON.stringify(result.feature_summary)}</p>
    `;
  } catch (error) {
    predictionElement.textContent = 'Unable to reach the prediction server.';
  }
}

document.getElementById('email-form').addEventListener('submit', submitEmail);
loadMetrics();
