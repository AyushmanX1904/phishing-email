import re

PHISHING_KEYWORDS = [
    'login', 'verify', 'account', 'password', 'urgent', 'bank', 'secure', 'click',
    'update', 'confirm', 'notice', 'limited', 'winner', 'free', 'validate', 'expire',
    'security', 'payment', 'unauthorized', 'credential'
]
SUSPICIOUS_DOMAINS = [
    'paypalsecurity', 'account-update', 'secure-login', 'verify-account',
    'banking-update', 'login-verify', 'confirm-account', 'security-alert'
]
SUSPICIOUS_TLDS = ['ru', 'cn', 'tk', 'xyz', 'top', 'club', 'info', 'cc', 'ml']

URL_PATTERN = re.compile(r'https?://|www\.|mailto:', re.IGNORECASE)
SUSPICIOUS_DOMAIN_PATTERN = re.compile(
    r'\b(?:' + '|'.join(re.escape(token) for token in SUSPICIOUS_DOMAINS) + r')\b',
    re.IGNORECASE,
)
SUSPICIOUS_TLD_PATTERN = re.compile(r'\.(?:' + '|'.join(re.escape(tld) for tld in SUSPICIOUS_TLDS) + r')\b', re.IGNORECASE)


def extract_features(email_text):
    text = (email_text or '').strip()
    lower = text.lower()
    urls = URL_PATTERN.findall(text)
    url_count = len(urls)
    keyword_count = sum(lower.count(keyword) for keyword in PHISHING_KEYWORDS)
    suspicious_domain_count = len(SUSPICIOUS_DOMAIN_PATTERN.findall(lower))
    suspicious_tld_count = len(SUSPICIOUS_TLD_PATTERN.findall(lower))
    exclamation_count = text.count('!')
    dollar_count = text.count('$')
    digit_count = sum(char.isdigit() for char in text)
    words = re.findall(r"[A-Za-z']+", text)
    uppercase_words = sum(1 for word in words if word.isupper() and len(word) > 1)
    uppercase_ratio = uppercase_words / max(len(words), 1)
    has_login = int(any(token in lower for token in ['login', 'verify', 'password', 'click', 'confirm', 'secure', 'bank']))

    return {
        'length': len(text),
        'url_count': url_count,
        'keyword_count': keyword_count,
        'suspicious_domain_count': suspicious_domain_count,
        'suspicious_tld_count': suspicious_tld_count,
        'exclamation_count': exclamation_count,
        'dollar_count': dollar_count,
        'digit_count': digit_count,
        'uppercase_ratio': uppercase_ratio,
        'has_login': has_login,
    }
