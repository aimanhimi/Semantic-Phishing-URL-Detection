import streamlit as st
import joblib
import pandas as pd
import wordninja
import re
from urllib.parse import urlparse
import tldextract

# Load common words data
common_words_df = pd.read_csv("data/unigram_freq.csv")
common_words_df = common_words_df[common_words_df['word'].apply(lambda x: isinstance(x, str))]
common_words_df = common_words_df[common_words_df['word'].apply(lambda x: len(x) >= 4)]
common_words_set = set(common_words_df['word'])

# Helper functions for feature extraction
def extract_domain(url):
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    if netloc.startswith('www.'):
        return netloc
    return netloc

def extract_core_domain(domain):
    extracted = tldextract.extract(domain)
    core_domain = '.'.join(part for part in [extracted.subdomain, extracted.domain] if part)
    if core_domain.startswith("www."):
        core_domain = core_domain[4:]
    return core_domain

def compute_ratio(CoreDomain):
    split_words = wordninja.split(CoreDomain)
    actual_words = [word for word in split_words if len(word) > 3 and word.isalpha()]
    num_common_words = sum(1 for word in actual_words if word in common_words_set)
    if len(split_words) == 0:
        ratio = 0
    else:
        ratio = sum(len(word) ** 2 for word in actual_words) / (len(CoreDomain) * len(split_words))
    return ratio, num_common_words

def is_ip_address(domain):
    ip_pattern = re.compile(r'(^|\.)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}($|\.)')
    return 0 if ip_pattern.search(domain) is None else 1

def calculate_char_continuation_rate(domain):
    if domain.startswith("www."):
        domain = domain[4:]
    groups = re.findall(r'[a-zA-Z]+|\d+|[^a-zA-Z\d]', domain)
    groups = groups[:-2]
    num_switches = len(groups)
    total_length = len("".join(groups))
    if len(groups) <= 2:
        return 1.0
    if groups[-2] == ".":
        num_switches += 1
    return (total_length - (num_switches - 2)) / total_length

def count_other_special_chars_domain(domain):
    return sum(1 for c in domain if not c.isalnum())

def preprocess_url(url):
    domain = extract_domain(url)
    FirstSubDomain = domain.split('.')[0] if len(domain.split('.')) > 2 else ""
    CoreDomain = extract_core_domain(domain)
    ratio_nlp, common_words = compute_ratio(CoreDomain)
    if len(domain.split('.')) == 2 and domain.split('.')[0] != 'www':
        domain = "www." + domain
    features = {
        'LengthFirstSubdomain': len(FirstSubDomain),
        'DigitsFirstSubdomain': sum(c.isdigit() for c in FirstSubDomain),
        'IsDomainIP': is_ip_address(domain),
        'NoOfDigitsInDomain': sum(c.isdigit() for c in domain),
        'DigitRatioInDomain': sum(c.isdigit() for c in domain) / len(domain),
        'NoOfHyphenInDomain': domain.count('-'),
        'NoOfOtherSpecialInDomain': count_other_special_chars_domain(domain),
        'SpecialCharRatioInDomain': count_other_special_chars_domain(domain) / len(domain),
        'CharContinuationRate': calculate_char_continuation_rate(domain),
        'IsHTTPS': 1 if url.startswith('https') else 0,
        'RatioNLP': ratio_nlp,
        'CommonWords': common_words,
    }
    return pd.DataFrame([features])

# Load the trained model
model = joblib.load('rf_model.pkl')

# Streamlit layout adjustments
st.set_page_config(page_title="Semantic Malicious URL Detector", page_icon="🔍", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #ADDFFF;
        }
        .stButton>button {
            font-size: 16px;
            padding: 10px;
            margin: auto;
            display: block;
            background-color: #008CBA;
            color: white;
            border: none;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #005F73;
        }
    </style>
""", unsafe_allow_html=True)

st.title("**Semantic Malicious URL Detector**")
st.markdown("### Enter a URL below to check if it's phishing or legitimate:")

# Input box for URL
user_input = st.text_input("Enter the URL here:", placeholder="e.g., https://example.com")

new_feats = ['DigitsFirstSubdomain', 'LengthFirstSubdomain','IsDomainIP', 'NoOfDigitsInDomain', 'DigitRatioInDomain',
             'NoOfHyphenInDomain', 'NoOfOtherSpecialInDomain', 'SpecialCharRatioInDomain', 'CharContinuationRate', 'IsHTTPS',
             'RatioNLP', 'CommonWords']

# Submit button centered
if st.button("Submit"):
    if user_input:
        try:
            input_features = preprocess_url(user_input)
            # Ensure that the order of columns is the same as the one used during training
            input_features = input_features[new_feats]
            prediction = model.predict(input_features)[0]
            prediction_proba = model.predict_proba(input_features)
            if prediction == 0:
                st.error(f"The URL is likely **phishing**. Confidence: {prediction_proba[0][0]:.2f}")
            else:
                st.success(f"The URL is likely **legitimate**. Confidence: {prediction_proba[0][1]:.2f}")
        except Exception as e:
            st.error(f"Error processing the URL: {e}")
    else:
        st.warning("Please enter a valid URL.")
