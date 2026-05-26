function extract_features(text){text=(text||'').trim();const lower=text.toLowerCase();const url_count=(text.match(/https?:\/\/|www\.|mailto:/gi)||[]).length;const PHISHING_KEYWORDS=['login','verify','account','password','urgent','bank','secure','click','update','confirm','notice','limited','winner','free','validate','expire','security','payment','unauthorized','credential'];let keyword_count=0;for(const k of PHISHING_KEYWORDS){keyword_count+= (lower.split(k).length-1);}const exclamation_count=(text.match(/!/g)||[]).length;const dollar_count=(text.match(/\$/g)||[]).length;const digit_count=(text.match(/\d/g)||[]).length;const words=(text.match(/[A-Za-z']+/g)||[]);const uppercase_words=words.filter(w=>w===w.toUpperCase()&&w.length>1).length;const uppercase_ratio=uppercase_words/Math.max(words.length,1);return{length:text.length,url_count,keyword_count,exclamation_count,dollar_count,digit_count,uppercase_ratio};}

function predict_js(features){ // simple heuristic scoring
  let score = 0;
  score += features.url_count * 2;
  score += features.keyword_count * 1.5;
  score += features.exclamation_count * 0.5;
  score += features.dollar_count * 1.0;
  score += features.uppercase_ratio * 5;
  // threshold
  return score >= 3.5 ? {label:'phishing',probability:Math.min(0.99,(score/10).toFixed(2))} : {label:'legitimate',probability:Math.max(0.01,(score/10).toFixed(2))};
}

async function loadMetrics(){const el=document.getElementById('metrics');try{const res=await fetch('/phishing-email/model/metrics.json');if(!res.ok){el.textContent='Metrics not available.';return;}const metrics=await res.json();el.innerHTML=`<p><strong>Accuracy:</strong> ${metrics.accuracy}</p><p><strong>Test samples:</strong> ${metrics.test_samples}</p><h3>Confusion matrix</h3><table class="metric-table"><tr><th></th><th>Pred Legitimate</th><th>Pred Phishing</th></tr><tr><th>True Legitimate</th><td>${metrics.confusion_matrix[0][0]}</td><td>${metrics.confusion_matrix[0][1]}</td></tr><tr><th>True Phishing</th><td>${metrics.confusion_matrix[1][0]}</td><td>${metrics.confusion_matrix[1][1]}</td></tr></table>`;}catch(e){el.textContent='Error loading metrics.'}}

async function submitEmail(e){e.preventDefault();const ta=document.getElementById('email_text');const predEl=document.getElementById('prediction');predEl.textContent='Analyzing...';const features=extract_features(ta.value);const result=predict_js(features);predEl.innerHTML=`<p><strong>Prediction:</strong> ${result.label}</p><p><strong>Phishing probability:</strong> ${result.probability}</p><p><strong>Features:</strong> ${JSON.stringify(features)}</p>`}

document.getElementById('email-form').addEventListener('submit',submitEmail);loadMetrics();