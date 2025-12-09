import streamlit as st
import joblib
from streamlit_lottie import st_lottie
import json
import time

# --------- Load Model & Vectorizer ----------
vectorizer = joblib.load("vectorizer.jb")
model = joblib.load("lr_model.jb")

# --------- Page Config ----------
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="📰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------- Premium Custom CSS with Dark Mode ----------
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0F172A 0%, #1A1F35 100%);
        min-height: 100vh;
    }
    
    [data-testid="stMainBlockContainer"] {
        padding: 40px 20px;
        max-width: 700px;
        margin: 0 auto;
    }
    
    /* Title Section */
    .title-container {
        text-align: center;
        margin-bottom: 50px;
        animation: fadeInDown 0.6s ease-out;
    }
    
    .title-container h1 {
        font-size: 48px;
        font-weight: 700;
        background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 12px;
        letter-spacing: -0.5px;
    }
    
    .title-container p {
        font-size: 16px;
        color: #94A3B8;
        line-height: 1.6;
        font-weight: 500;
    }
    
    /* Card Container */
    .input-card {
        background: linear-gradient(135deg, #1E293B 0%, #1A1F35 100%);
        border-radius: 20px;
        padding: 35px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(71, 85, 105, 0.3);
        margin-bottom: 25px;
        animation: fadeInUp 0.6s ease-out 0.2s both;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .input-card:hover {
        box-shadow: 0 20px 60px rgba(59, 130, 246, 0.2);
        border-color: rgba(59, 130, 246, 0.3);
        transform: translateY(-2px);
    }
    
    /* Textarea Styling */
    textarea {
        border-radius: 12px !important;
        border: 2px solid #334155 !important;
        font-size: 15px !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        padding: 16px !important;
        transition: all 0.3s ease !important;
        background-color: #0F172A !important;
        color: #E2E8F0 !important;
        line-height: 1.6 !important;
    }
    
    textarea:focus {
        border-color: #60A5FA !important;
        background-color: #1E293B !important;
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1) !important;
    }
    
    textarea::placeholder {
        color: #64748B !important;
    }
    
    /* Label Styling */
    .input-label {
        display: block;
        font-size: 14px;
        font-weight: 600;
        color: #E2E8F0;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Button Styling */
    .stButton > button {
        width: 100%;
        padding: 14px 28px !important;
        background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Loading Animation Container */
    .loading-container {
        background: linear-gradient(135deg, #1E293B 0%, #1A1F35 100%);
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        text-align: center;
        animation: fadeIn 0.3s ease-out;
        border: 1px solid rgba(71, 85, 105, 0.3);
    }
    
    .loading-text {
        font-size: 18px;
        color: #CBD5E1;
        margin-top: 20px;
        font-weight: 600;
    }
    
    /* Result Boxes */
    .result-container {
        animation: fadeIn 0.5s ease-out;
    }
    
    .result-box {
        padding: 30px;
        border-radius: 16px;
        font-size: 18px;
        font-weight: 600;
        margin-top: 20px;
        display: flex;
        align-items: center;
        gap: 16px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        border: 2px solid;
        animation: slideInUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .result-box.real {
        background: linear-gradient(135deg, #064E3B 0%, #065F46 100%);
        border-color: #10B981;
        color: #A7F3D0;
    }
    
    .result-box.fake {
        background: linear-gradient(135deg, #7C2D12 0%, #9A3412 100%);
        border-color: #F97316;
        color: #FED7AA;
    }
    
    .result-icon {
        font-size: 32px;
    }
    
    /* SVG Icon Styling */
    .news-icon {
        display: inline-block;
        width: 64px;
        height: 64px;
        margin-bottom: 20px;
    }
    
    .icon-section {
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    /* Spinner */
    .spinner {
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 4px solid #334155;
        border-top-color: #60A5FA;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Warning/Error Messages */
    [data-testid="stAlert"] {
        border-radius: 12px !important;
        padding: 16px 20px !important;
        border-left: 4px solid !important;
        background-color: #1E293B !important;
        color: #E2E8F0 !important;
    }
    
    /* Responsive */
    @media (max-width: 640px) {
        .title-container h1 {
            font-size: 36px;
        }
        
        .input-card {
            padding: 25px;
        }
        
        .result-box {
            font-size: 16px;
            padding: 24px;
        }
    }
</style>
""", unsafe_allow_html=True)

# --------- Lottie Animation URL ----------
loading_animation = "https://assets1.lottiefiles.com/packages/lf20_p8bfn5to.json"

news_icon_svg = """
<svg class="news-icon" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <rect x="10" y="15" width="80" height="70" rx="5" fill="none" stroke="#60A5FA" stroke-width="2"/>
    <line x1="20" y1="30" x2="80" y2="30" stroke="#60A5FA" stroke-width="2"/>
    <line x1="20" y1="40" x2="80" y2="40" stroke="#3B82F6" stroke-width="1.5" opacity="0.7"/>
    <line x1="20" y1="48" x2="60" y2="48" stroke="#3B82F6" stroke-width="1.5" opacity="0.7"/>
    <line x1="20" y1="56" x2="80" y2="56" stroke="#3B82F6" stroke-width="1.5" opacity="0.7"/>
    <line x1="20" y1="64" x2="70" y2="64" stroke="#3B82F6" stroke-width="1.5" opacity="0.7"/>
    <circle cx="75" cy="58" r="8" fill="#60A5FA" opacity="0.8"/>
</svg>
"""

# --------- Title Section ----------
st.markdown(f"""
<div class="title-container">
        {news_icon_svg}
    📰 Fake News Detector
    Enter a news article and instantly discover whether it's authentic or misleading. 
    Powered by advanced machine learning analysis.
</div>
""", unsafe_allow_html=True)

verification_icon_svg = """
<svg viewBox="0 0 24 24" width="24" height="24" xmlns="http://www.w3.org/2000/svg" style="display: inline; margin-right: 8px;">
    <path fill="#60A5FA" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"/>
    <path fill="#60A5FA" d="M10.5 13.5l-2-2v3l2 2 4-4-1.5-1.5z"/>
</svg>
"""

# --------- Input Card ----------
input_card_html = f"""
<div class="input-card">
    <label class="input-label">{verification_icon_svg}📝 News Article</label>
    <p style="color: #64748B; font-size: 14px; margin-bottom: 12px;">Type or paste your news article below to analyze its authenticity...</p>
</div>
"""
st.markdown(input_card_html, unsafe_allow_html=True)

input_text = st.text_area(
    "News Article",
    placeholder="Type or paste your news article here to analyze its authenticity...",
    height=180,
    label_visibility="collapsed"
)

check_btn = st.button("🔍 Analyze News", use_container_width=True)

authentic_icon_svg = """
<svg viewBox="0 0 100 100" width="40" height="40" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="50" r="45" fill="none" stroke="#10B981" stroke-width="3"/>
    <path d="M 30 50 L 45 65 L 70 35" stroke="#10B981" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

misleading_icon_svg = """
<svg viewBox="0 0 100 100" width="40" height="40" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="50" r="45" fill="none" stroke="#F97316" stroke-width="3"/>
    <line x1="35" y1="35" x2="65" y2="65" stroke="#F97316" stroke-width="4" stroke-linecap="round"/>
    <line x1="65" y1="35" x2="35" y2="65" stroke="#F97316" stroke-width="4" stroke-linecap="round"/>
</svg>
"""

# --------- Prediction Logic ----------
if check_btn:
    if input_text.strip():
        with st.spinner(""):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                loading_html = """
                <div class="loading-container">
                """
                st.markdown(loading_html, unsafe_allow_html=True)
                st_lottie(loading_animation, height=200, key="loader")
                st.markdown('<p class="loading-text">Analyzing article...</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            time.sleep(2)

        transformed = vectorizer.transform([input_text])
        prediction = model.predict(transformed)[0]

        if prediction == 1:
            result_html = f"""
            <div class="result-container">
                <div class="result-box real">{authentic_icon_svg}<span><strong>The News is Authentic!</strong><br><small>This article appears to be genuine and reliable based on our analysis.</small></span></div>
            </div>
            """
        else:
            result_html = f"""
            <div class="result-container">
                <div class="result-box fake">{misleading_icon_svg}<span><strong>The News is Misleading!</strong><br><small>This article shows characteristics commonly associated with misinformation.</small></span></div>
            </div>
            """
        
        st.markdown(result_html, unsafe_allow_html=True)
    else:
        st.warning("Please enter some text to analyze.", icon="⚠️")
