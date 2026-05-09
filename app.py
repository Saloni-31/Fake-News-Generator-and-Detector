import streamlit as st
from generator import generate_fake_news
from detector import detect_fake_news

# Page configuration
st.set_page_config(
    page_title="Fake News AI | Professional Edition",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI
st.markdown("""
    <style>
    /* Global Reset & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        background-color: #f4f6f9;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #1e293b;
        color: #ffffff;
    }
    .sidebar .sidebar-content h3 {
        color: #ffffff;
        font-weight: 700;
    }
    .sidebar .stRadio label {
        color: #cbd5e1;
    }
    .sidebar .stRadio label:hover {
        color: #ffffff;
    }

    /* Main Header */
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
        padding-top: 1rem;
    }
    .main-header h1 {
        color: #1e293b;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    .main-header p {
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 400;
    }

    /* Card Container */
    .card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
    }
    
    .card-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Input Styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        padding: 12px;
        font-size: 1rem;
    }
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        padding: 12px;
        font-size: 1rem;
    }

    /* Button Styling */
    .stButton > button {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
    }
    .stButton > button:hover {
        background-color: #1d4ed8;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(37, 99, 235, 0.3);
    }

    /* Result Boxes */
    .result-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 5px solid;
    }
    .result-fake {
        background-color: #fef2f2;
        border-color: #ef4444;
        color: #991b1b;
    }
    .result-real {
        background-color: #f0fdf4;
        border-color: #22c55e;
        color: #166534;
    }
    .result-uncertain {
        background-color: #fffbeb;
        border-color: #f59e0b;
        color: #92400e;
    }

    /* Metric Styling */
    .metric-container {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
    }
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        color: #94a3b8;
        font-size: 0.875rem;
        border-top: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>🛡️ Fake News Genterator And Detector</h1>
        <p>Advanced Generation & Detection System</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("""
    <div style="padding: 10px; background-color: #1e293b; border-radius: 12px; margin-bottom: 20px;">
        <h3 style="color: white; margin: 0;">📋 Navigation</h3>
    </div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Select Module",
    ["Generate News", "Detect News", "About"],
    index=0,
    label_visibility="collapsed"
)

# ==================== GENERATOR PAGE ====================
if page == "Generate News":

    st.markdown('<div class="card-title">📝 News Generator</div>', unsafe_allow_html=True)
    st.markdown("Create synthetic news articles to test detection capabilities.")
    
    topic = st.text_input(
        "Enter Topic:",
        placeholder="e.g., climate change, election, health",
        label_visibility="collapsed"
    )
    
    if st.button("🚀 Generate News", type="primary"):
        if topic.strip():
            with st.spinner("⏳ AI is crafting the article..."):
                generated_text = generate_fake_news(topic)
                
                st.markdown("### 📰 Generated Article")
                st.info(generated_text, icon="📰")
                
                st.markdown("---")
                st.markdown("### 🔍 Auto-Detection Analysis")
                
                with st.spinner("⏳ Analyzing authenticity..."):
                    result = detect_fake_news(generated_text)
                    
                    # Result Box
                    if result['label'] == 'FAKE':
                        st.markdown(f"""
                            <div class="result-box result-fake">
                                <strong>⚠️ Prediction: {result['label']}</strong>
                                <p style="margin: 5px 0 0 0;">{result.get('reason', 'High probability of fabrication detected.')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    elif result['label'] == 'REAL':
                        st.markdown(f"""
                            <div class="result-box result-real">
                                <strong>✅ Prediction: {result['label']}</strong>
                                <p style="margin: 5px 0 0 0;">{result.get('reason', 'Text appears consistent with real news patterns.')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="result-box result-uncertain">
                                <strong>⚠️ Prediction: {result['label']}</strong>
                                <p style="margin: 5px 0 0 0;">{result.get('reason', 'Model is uncertain about this text.')}</p>
                            </div>
                        """, unsafe_allow_html=True)

                    # Metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                            <div class="metric-container">
                                <div class="metric-label">Confidence</div>
                                <div class="metric-value">{result['score']:.2%}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                            <div class="metric-container">
                                <div class="metric-label">Model Status</div>
                                <div class="metric-value">Active</div>
                            </div>
                        """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter a topic to generate news.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== DETECTOR PAGE ====================
elif page == "Detect News":
    st.markdown('<div class="card-title">🔍 News Detector</div>', unsafe_allow_html=True)
    st.markdown("Paste any news text to verify its authenticity.")
    
    user_input = st.text_area(
        "Enter News Text:",
        height=200,
        placeholder="Paste your news article here...",
        label_visibility="collapsed"
    )
    
    if st.button("🔍 Analyze Text", type="primary"):
        if user_input.strip():
            with st.spinner("⏳ Analyzing text patterns..."):
                result = detect_fake_news(user_input)
                
                # Result Box
                if result['label'] == 'FAKE':
                    st.markdown(f"""
                        <div class="result-box result-fake">
                            <strong>⚠️ Prediction: {result['label']}</strong>
                            <p style="margin: 5px 0 0 0;">{result.get('reason', 'High probability of fabrication detected.')}</p>
                        </div>
                    """, unsafe_allow_html=True)
                elif result['label'] == 'REAL':
                    st.markdown(f"""
                        <div class="result-box result-real">
                            <strong>✅ Prediction: {result['label']}</strong>
                            <p style="margin: 5px 0 0 0;">{result.get('reason', 'Text appears consistent with real news patterns.')}</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="result-box result-uncertain">
                            <strong>⚠️ Prediction: {result['label']}</strong>
                            <p style="margin: 5px 0 0 0;">{result.get('reason', 'Model is uncertain about this text.')}</p>
                        </div>
                    """, unsafe_allow_html=True)

                # Metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                        <div class="metric-container">
                            <div class="metric-label">Confidence</div>
                            <div class="metric-value">{result['score']:.2%}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                        <div class="metric-container">
                            <div class="metric-label">Input Length</div>
                            <div class="metric-value">{len(user_input)} chars</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 📝 Input Preview")
                st.write(user_input)
        else:
            st.warning("⚠️ Please enter some text to analyze.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== ABOUT PAGE ====================
elif page == "About":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">ℹ️ Project Information</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Purpose
    This application demonstrates the dual capabilities of AI in the media landscape:
    - **Generation:** Creating synthetic content using GPT-2.
    - **Detection:** Identifying authenticity using RoBERTa.
    
    ### 🛠️ Tech Stack"""
    )