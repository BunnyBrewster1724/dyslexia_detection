import streamlit as st
import random
import speech_recognition as sr
from fuzzywuzzy import fuzz
import statistics
import time

# ------------------------------------------------------------
# Streamlit UI Setup - ENHANCED VERSION
# ------------------------------------------------------------

st.set_page_config(
    page_title="Dyslexia Reading Aid",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with modern design, animations, and accessibility
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Root Variables for consistent theming */
    :root {
        --primary-bg: #f8f9fa;
        --card-bg: #ffffff;
        --accent-color: #4f46e5;
        --accent-hover: #3730a3;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --success-color: #059669;
        --warning-color: #d97706;
        --error-color: #dc2626;
        --border-radius: 16px;
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
        --shadow-lg: 0 10px 25px rgba(0,0,0,0.15);
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* General Body Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', 'Noto Sans Devanagari', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        color: var(--text-primary);
    }
    
    /* Main App Container */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }

    /* Main Content Area */
    .main .block-container {
        padding: 3rem 1rem 2rem 1rem;
        max-width: 800px;
    }

    /* Enhanced Card Design */
    .modern-card {
        background: var(--card-bg);
        border-radius: var(--border-radius);
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-lg);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }

    .modern-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--accent-color), #7c3aed);
        border-radius: var(--border-radius) var(--border-radius) 0 0;
    }

    .modern-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }

    /* Typography */
    h1 {
        font-family: 'Inter', sans-serif;
        color: #ffffff;
        font-weight: 700;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    h2, h3 {
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
        font-weight: 600;
        text-align: center;
        margin-bottom: 1rem;
    }

    h2 {
        font-size: 2rem;
        color: #ffffff;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    /* Enhanced Sentence Box */
    .sentence-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: var(--border-radius);
        padding: 2rem;
        font-size: 1.8rem;
        font-weight: 600;
        color: #ffffff;
        text-align: center;
        margin: 2rem 0;
        border: 3px solid rgba(255,255,255,0.2);
        box-shadow: var(--shadow-md);
        position: relative;
        line-height: 1.6;
        font-family: 'Noto Sans Devanagari', sans-serif;
    }

    .sentence-display::before {
        content: '"';
        position: absolute;
        top: -10px;
        left: 20px;
        font-size: 4rem;
        color: rgba(255,255,255,0.3);
        font-family: serif;
    }

    .sentence-display::after {
        content: '"';
        position: absolute;
        bottom: -30px;
        right: 20px;
        font-size: 4rem;
        color: rgba(255,255,255,0.3);
        font-family: serif;
    }

    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-color) 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 2.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        cursor: pointer;
        transition: var(--transition);
        box-shadow: var(--shadow-md);
        position: relative;
        overflow: hidden;
        min-width: 200px;
        text-transform: none;
        letter-spacing: 0.5px;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.6s;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4);
        background: linear-gradient(135deg, var(--accent-hover) 0%, #6d28d9 100%);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Progress Indicators */
    .progress-container {
        background: rgba(255,255,255,0.1);
        border-radius: 50px;
        padding: 8px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }

    .progress-bar {
        background: linear-gradient(90deg, var(--success-color), #10b981);
        height: 12px;
        border-radius: 50px;
        transition: width 0.8s ease;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.3);
    }

    /* Status Messages */
    .status-success {
        background: linear-gradient(135deg, var(--success-color), #10b981);
        color: white;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
        border-left: 4px solid #059669;
        animation: slideIn 0.5s ease-out;
    }

    .status-warning {
        background: linear-gradient(135deg, var(--warning-color), #f59e0b);
        color: white;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
        border-left: 4px solid #d97706;
        animation: slideIn 0.5s ease-out;
    }

    .status-error {
        background: linear-gradient(135deg, var(--error-color), #ef4444);
        color: white;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
        border-left: 4px solid #dc2626;
        animation: slideIn 0.5s ease-out;
    }

    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    /* Loading Animation */
    .loading-spinner {
        border: 4px solid rgba(255,255,255,0.3);
        border-top: 4px solid #ffffff;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 1rem auto;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Metric Display */
    .metric-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
        padding: 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-md);
        backdrop-filter: blur(10px);
    }

    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        color: var(--accent-color);
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 1.2rem;
        color: var(--text-secondary);
        font-weight: 500;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 2rem 1rem;
        }
        
        .modern-card {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .sentence-display {
            font-size: 1.4rem;
            padding: 1.5rem;
        }
        
        h1 {
            font-size: 2.5rem;
        }
        
        .stButton > button {
            min-width: 150px;
            padding: 0.8rem 2rem;
        }
    }

    /* Accessibility Improvements */
    .stButton > button:focus {
        outline: 3px solid rgba(79, 70, 229, 0.5);
        outline-offset: 2px;
    }

    /* Custom Streamlit Component Overrides */
    .stAlert {
        border-radius: var(--border-radius);
        border: none;
        box-shadow: var(--shadow-md);
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, var(--accent-color), #7c3aed);
        border-radius: 50px;
    }

    /* Hide Streamlit Branding */
    .stDeployButton {
        display: none;
    }
    
    footer {
        display: none;
    }
    
    .stApp > header {
        display: none;
    }

    </style>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
# Hindi sentences
# ------------------------------------------------------------
sentences = [
    "भारत एक विशाल देश है और इसकी संस्कृति विविधता से भरपूर है।",
    "गंगा नदी भारत की सबसे पवित्र नदियों में से एक मानी जाती है।",
    "ताजमहल प्रेम का अद्भुत प्रतीक है।",
    "हिमालय पर्वत श्रृंखला प्राकृतिक सौंदर्य का खजाना है।",
    "दिल्ली भारत की राजधानी और ऐतिहासिक धरोहरों का केंद्र है।",
    "सत्य और अहिंसा महात्मा गांधी के मुख्य सिद्धांत थे।",
    "भारत में विभिन्न भाषाएँ और परंपराएँ एकता में बंधी हैं।",
    "कड़ी मेहनत और दृढ़ निश्चय सफलता की कुंजी हैं।",
    "पेड़ हमें स्वच्छ हवा और छाया प्रदान करते हैं।",
    "पुस्तकें ज्ञान का सबसे बड़ा स्रोत होती हैं।"
]
LINES_PER_TEST = 3
recognizer = sr.Recognizer()

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'all_scores' not in st.session_state:
    st.session_state.all_scores = []
if 'chosen_lines' not in st.session_state:
    st.session_state.chosen_lines = []
if 'current_sentence_idx' not in st.session_state:
    st.session_state.current_sentence_idx = 0

# --- Functions ---
def start_test():
    st.session_state.chosen_lines = random.sample(sentences, k=LINES_PER_TEST)
    st.session_state.current_sentence_idx = 0
    st.session_state.all_scores = []
    st.session_state.page = "test"

def restart_test():
    st.session_state.page = "home"
    # Reset all relevant state variables
    start_test()

def create_progress_indicator(current, total):
    """Create a visual progress indicator"""
    progress = current / total
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress * 100}%"></div>
    </div>
    <p style="text-align: center; color: white; margin-top: 0.5rem;">
        चरण {current} का {total} | {int(progress * 100)}% पूर्ण
    </p>
    """, unsafe_allow_html=True)

# --- Main App Logic using Pages ---

# PAGE 1: HOME SCREEN
if st.session_state.page == "home":
    st.title("📖 Dyslexia Reading Aid")
    
    st.markdown("""
    <div class="modern-card">
        <h3 style="color: var(--accent-color); margin-bottom: 1.5rem;">स्वागत है! 🙏</h3>
        <p style="font-size: 1.2rem; line-height: 1.8; color: var(--text-secondary); text-align: center;">
            यह ऐप आपको अपनी पढ़ने की सटीकता का आकलन करने में मदद करता है। 
            आपको कुछ हिंदी वाक्य पढ़ने के लिए दिए जाएंगे और हम आपकी उच्चारण शुद्धता को मापेंगे।
        </p>
        <div style="text-align: center; margin: 2rem 0;">
            <p style="font-size: 1rem; color: var(--text-secondary);">
                📝 कुल वाक्य: <strong>3</strong> | ⏱️ अनुमानित समय: <strong>2-3 मिनट</strong>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 परीक्षण शुरू करें"):
            start_test()
            st.rerun()

# PAGE 2: TEST SCREEN
elif st.session_state.page == "test":
    idx = st.session_state.current_sentence_idx
    
    if idx < LINES_PER_TEST:
        hindi_text = st.session_state.chosen_lines[idx]

        # Progress indicator
        create_progress_indicator(idx + 1, LINES_PER_TEST)
        
        st.markdown(f"<h2>पंक्ति {idx + 1}</h2>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="modern-card">
            <h3 style="color: var(--accent-color);">कृपया निम्नलिखित वाक्य स्पष्ट रूप से पढ़ें:</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced sentence display
        st.markdown(f"""
        <div class="sentence-display">
            {hindi_text}
        </div>
        """, unsafe_allow_html=True)

        # Use a placeholder for messages and results
        result_placeholder = st.empty()

        # Recording instructions
        st.markdown("""
        <div class="modern-card" style="text-align: center;">
            <p style="color: var(--text-secondary); margin-bottom: 1rem;">
                🎤 रिकॉर्डिंग बटन दबाएं और साफ़ आवाज़ में वाक्य पढ़ें
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎤 रिकॉर्डिंग शुरू करें", key=f"rec_{idx}"):
                # Show loading animation
                result_placeholder.markdown("""
                <div style="text-align: center; padding: 2rem;">
                    <div class="loading-spinner"></div>
                    <p style="color: white; margin-top: 1rem; font-size: 1.1rem;">
                        🎤 रिकॉर्डिंग हो रही है... अब बोलें!
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                try:
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
                    
                    result_placeholder.markdown("""
                    <div style="text-align: center; padding: 2rem;">
                        <div class="loading-spinner"></div>
                        <p style="color: white; margin-top: 1rem; font-size: 1.1rem;">
                            ⚙️ विश्लेषण हो रहा है... कृपया प्रतीक्षा करें...
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Speech to text
                    user_speech = recognizer.recognize_google(audio, language="hi-IN")
                    
                    # Calculate accuracy
                    accuracy = fuzz.token_sort_ratio(hindi_text, user_speech)
                    st.session_state.all_scores.append(accuracy)

                    # Enhanced result display
                    if accuracy >= 85:
                        result_class = "status-success"
                        icon = "✅"
                        message = "बहुत बढ़िया!"
                    elif accuracy >= 70:
                        result_class = "status-warning"
                        icon = "⚠️"
                        message = "अच्छा प्रयास!"
                    else:
                        result_class = "status-error"
                        icon = "❌"
                        message = "पुनः प्रयास करें"

                    result_placeholder.markdown(f"""
                    <div class="{result_class}">
                        <h4 style="margin: 0 0 1rem 0;">{icon} {message}</h4>
                        <p style="margin: 0.5rem 0;"><strong>आपने कहा:</strong> "{user_speech}"</p>
                        <div class="metric-container" style="margin: 1rem 0; background: rgba(255,255,255,0.2);">
                            <div class="metric-value" style="color: white;">{accuracy}%</div>
                            <div class="metric-label" style="color: rgba(255,255,255,0.8);">शुद्धता स्कोर</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Move to the next sentence after a short delay
                    st.session_state.current_sentence_idx += 1
                    time.sleep(3)
                    st.rerun()

                except sr.WaitTimeoutError:
                    result_placeholder.markdown("""
                    <div class="status-warning">
                        <h4>⏰ समय समाप्त</h4>
                        <p>कृपया फिर से प्रयास करें और तुरंत बोलना शुरू करें।</p>
                    </div>
                    """, unsafe_allow_html=True)
                except sr.UnknownValueError:
                    result_placeholder.markdown("""
                    <div class="status-error">
                        <h4>🔊 आवाज़ स्पष्ट नहीं</h4>
                        <p>कृपया साफ़ और स्पष्ट आवाज़ में बोलने का प्रयास करें।</p>
                    </div>
                    """, unsafe_allow_html=True)
                except sr.RequestError:
                    result_placeholder.markdown("""
                    <div class="status-error">
                        <h4>🌐 कनेक्शन समस्या</h4>
                        <p>इंटरनेट कनेक्शन जांचें और पुनः प्रयास करें।</p>
                    </div>
                    """, unsafe_allow_html=True)

    else:
        st.session_state.page = "summary"
        st.rerun()

# PAGE 3: SUMMARY SCREEN
elif st.session_state.page == "summary":
    st.title("📊 परीक्षण सारांश")
    
    if st.session_state.all_scores:
        avg_score = round(statistics.mean(st.session_state.all_scores), 1)
        
        # Enhanced metric display
        st.markdown(f"""
        <div class="modern-card">
            <div class="metric-container">
                <div class="metric-value">{avg_score}%</div>
                <div class="metric-label">औसत शुद्धता स्कोर</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Visual progress bar
        st.progress(int(avg_score))
        
        # Enhanced result interpretation
        if avg_score < 70:
            st.markdown("""
            <div class="status-error">
                <h4>📋 विस्तृत मूल्यांकन</h4>
                <p><strong>स्थिति:</strong> पढ़ने में गंभीर कठिनाई देखी गई है।</p>
                <p><strong>सुझाव:</strong> Dyslexia की उच्च संभावना है। कृपया किसी विशेषज्ञ से सलाह लें।</p>
                <p><strong>अगले कदम:</strong> व्यापक न्यूरोसाइकोलॉजिकल परीक्षण कराएं।</p>
            </div>
            """, unsafe_allow_html=True)
        elif avg_score < 85:
            st.markdown("""
            <div class="status-warning">
                <h4>📋 विस्तृत मूल्यांकन</h4>
                <p><strong>स्थिति:</strong> हल्की से मध्यम पढ़ने की कठिनाई दिखाई दी है।</p>
                <p><strong>सुझाव:</strong> आगे जांच करवाना उचित होगा।</p>
                <p><strong>अगले कदम:</strong> नियमित अभ्यास और विशेषज्ञ की सलाह लें।</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-success">
                <h4>📋 विस्तृत मूल्यांकन</h4>
                <p><strong>स्थिति:</strong> पढ़ने की क्षमता सामान्य और स्वस्थ है।</p>
                <p><strong>सुझाव:</strong> Dyslexia की संभावना बहुत कम है।</p>
                <p><strong>अगले कदम:</strong> नियमित पठन-पाठन जारी रखें।</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Score breakdown
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: var(--accent-color); text-align: center;">व्यक्तिगत स्कोर विवरण</h4>
        """, unsafe_allow_html=True)
        
        for i, score in enumerate(st.session_state.all_scores, 1):
            color = "#059669" if score >= 85 else "#d97706" if score >= 70 else "#dc2626"
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; 
                        padding: 0.8rem; margin: 0.5rem 0; background: rgba(0,0,0,0.05); 
                        border-radius: 8px; border-left: 4px solid {color};">
                <span><strong>वाक्य {i}:</strong></span>
                <span style="color: {color}; font-weight: 600;">{score}%</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="status-warning">
            <h4>⚠️ डेटा उपलब्ध नहीं</h4>
            <p>कोई मान्य रिकॉर्डिंग प्राप्त नहीं हुई। कृपया पुनः प्रयास करें।</p>
        </div>
        """, unsafe_allow_html=True)

    # Action buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 पुनः परीक्षण करें"):
            restart_test()
            st.rerun()

    # Additional information
    st.markdown("""
    <div class="modern-card" style="margin-top: 2rem;">
        <h4 style="color: var(--text-secondary); text-align: center;">📚 महत्वपूर्ण सूचना</h4>
        <p style="font-size: 0.9rem; color: var(--text-secondary); text-align: center; line-height: 1.6;">
            यह परीक्षण केवल प्रारंभिक स्क्रीनिंग के लिए है। यदि आपको कोई चिंता है, 
            तो कृपया किसी योग्य स्वास्थ्य विशेषज्ञ से सलाह लें। 
            यह परीक्षण चिकित्सा निदान का विकल्प नहीं है।
        </p>
    </div>
    """, unsafe_allow_html=True)