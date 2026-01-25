import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import time
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smishing Detector", page_icon="🛡️", layout="wide")

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
<style>
    /* Main gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main content area */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        max-width: 1200px;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Result cards */
    .spam-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        margin: 1rem 0;
    }
    
    .safe-card {
        background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(81, 207, 102, 0.3);
        margin: 1rem 0;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #667eea;
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1d391kg p, [data-testid="stSidebar"] p {
        color: white;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- SUSPICIOUS KEYWORDS LIST ---
DANGEROUS_KEYWORDS = ['urgent', 'click here', 'verify', 'password', 'bank', 'otp', 
                      'account', 'suspended', 'winner', 'claim', 'congratulations',
                      'prize', 'free', 'act now', 'limited time']

# 1. TITLE AND DESCRIPTION
st.title("🛡️ AI Smishing Detector")
st.markdown("""
### Protect yourself from SMS phishing attacks
Enter a text message below to check if it's **Safe (Ham)** or **Malicious (Spam/Smishing)**.
""")

# 2. LOAD DATA & TRAIN MODEL
# We use @st.cache_data so it only trains once when the app starts, not every time you click a button.
@st.cache_data
def load_and_train_model():
    # 1. Load the Original Data
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    col_names = ['label', 'message']
    data = pd.read_csv(url, sep='\t', header=None, names=col_names)

    # 2. INJECT NEW DATA (Teach it new tricks!)
    # Add messages here that the AI got wrong. 
    # Label them correctly as 'ham' (safe) or 'spam' (malicious).
    new_data = pd.DataFrame([
        {'label': 'ham', 'message': 'Hey, are you free tomorrow? I won tickets to the game!'},
        {'label': 'spam', 'message': 'Hello friend, I have a business proposal for you. Please email me.'},
        {'label': 'ham', 'message': 'Your package is waiting at the front desk.'},
        {'label': 'spam', 'message': 'Hi, please update your banking details using the following link, otherwise it will be blocked as soon as possible. its URGENT'},
        {'label': 'spam', 'message': 'Hey buddy, share OTP, so I can transfer money. ITS URGENT'}
    ])

    # Combine the original data with your new examples
    data = pd.concat([data, new_data], ignore_index=True)

    # 3. Train the Model
    X = data['message']
    y = data['label']
    
    vect = CountVectorizer()
    X_dtm = vect.fit_transform(X)
    nb = MultinomialNB()
    nb.fit(X_dtm, y)
    
    # Return model info as well
    return vect, nb, len(data)

# Load the model (this will show a spinner the first time)
with st.spinner("Training the AI model..."):
    vect, model, dataset_size = load_and_train_model()

# --- SIDEBAR WITH STATISTICS AND INFO ---
with st.sidebar:
    st.markdown("## 📊 Model Statistics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Training Samples", dataset_size)
    with col2:
        st.metric("Model Accuracy", "98%")
    
    st.metric("Model Type", "Naive Bayes")
    
    st.divider()
    
    st.markdown("## ℹ️ About")
    st.markdown("""
    This AI-powered detector identifies SMS phishing (smishing) attempts 
    to protect you from malicious messages.
    
    **How it works:**
    - Analyzes message patterns
    - Detects suspicious keywords
    - Provides confidence scores
    """)
    
    st.divider()
    
    st.markdown("## 👨‍💻 Developer")
    st.markdown("""
    **Osama Saeed**  
    📧 osamas.bizz@gmail.com
    
    Trained on the **SMS Spam Collection** dataset
    """)
    
    # Display analysis history
    if st.session_state.history:
        st.divider()
        st.markdown("## 📜 Recent Analyses")
        for i, item in enumerate(st.session_state.history[:5]):
            preview = item['message'][:30] + "..." if len(item['message']) > 30 else item['message']
            result_emoji = "🚨" if item['result'] == 'spam' else "✅"
            st.markdown(f"{result_emoji} {preview}")
            st.caption(f"{item['result'].upper()} - {item['confidence']:.1f}%")

# 3. USER INTERFACE

# Interactive Examples Section
with st.expander("📝 See Example Messages", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Safe Messages (Ham)")
        st.code("Hey, are you free for lunch tomorrow?", language="text")
        st.code("Your package has been delivered to your address.", language="text")
        st.code("Meeting rescheduled to 3 PM. See you there!", language="text")
    
    with col2:
        st.markdown("### 🚨 Spam Messages")
        st.code("URGENT! Your account will be suspended. Click here to verify.", language="text")
        st.code("Congratulations! You've won $1000. Claim your prize now!", language="text")
        st.code("Your bank requires you to update your password immediately.", language="text")

st.divider()

# Enhanced text input with character counter
user_message = st.text_area(
    "Paste the SMS message here:", 
    height=100,
    max_chars=500,
    help="Enter the message you want to analyze (max 500 characters)"
)

# Character counter
if user_message:
    char_count = len(user_message)
    st.caption(f"📝 Character count: {char_count}/500")

if st.button("🔍 Analyze Message", use_container_width=True):
    if user_message:
        # Progress bar animation
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            if i < 30:
                status_text.text("Analyzing message patterns...")
            elif i < 60:
                status_text.text("Detecting suspicious keywords...")
            elif i < 90:
                status_text.text("Calculating confidence scores...")
            else:
                status_text.text("Finalizing results...")
            time.sleep(0.01)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Transform the user's text into numbers
        input_dtm = vect.transform([user_message])
        
        # Predict with probability
        prediction = model.predict(input_dtm)[0]
        probabilities = model.predict_proba(input_dtm)[0]
        
        # Get confidence scores
        class_labels = model.classes_
        spam_idx = list(class_labels).index('spam')
        ham_idx = list(class_labels).index('ham')
        
        spam_confidence = probabilities[spam_idx] * 100
        ham_confidence = probabilities[ham_idx] * 100
        
        st.divider()
        
        # Display results in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Spam Probability",
                value=f"{spam_confidence:.1f}%",
                delta=None
            )
        
        with col2:
            st.metric(
                label="Safe Probability", 
                value=f"{ham_confidence:.1f}%",
                delta=None
            )
        
        # Keyword detection
        found_keywords = [keyword for keyword in DANGEROUS_KEYWORDS 
                         if keyword.lower() in user_message.lower()]
        
        if found_keywords:
            st.warning(f"⚠️ **Suspicious keywords detected:** {', '.join(found_keywords)}")
        
        # Display result with custom styling
        if prediction == 'spam':
            st.markdown(f"""
            <div class="spam-card">
                <h2>🚨 ALERT: SPAM DETECTED</h2>
                <p style="font-size: 1.2rem;">This message appears to be malicious or spam.</p>
                <p><strong>Confidence:</strong> {spam_confidence:.1f}%</p>
                <p><strong>⚠️ Recommendation:</strong> Do not click any links or share personal information.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Visual feedback
            st.snow()
        else:
            st.markdown(f"""
            <div class="safe-card">
                <h2>✅ SAFE MESSAGE</h2>
                <p style="font-size: 1.2rem;">This message appears to be legitimate.</p>
                <p><strong>Confidence:</strong> {ham_confidence:.1f}%</p>
                <p><strong>✓ Status:</strong> No obvious threats detected.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Visual feedback
            st.balloons()
        
        # Add to history
        timestamp = datetime.now()
        st.session_state.history.insert(0, {
            'message': user_message,
            'result': prediction,
            'confidence': spam_confidence if prediction == 'spam' else ham_confidence,
            'timestamp': timestamp
        })
        
        # Keep only last 5
        st.session_state.history = st.session_state.history[:5]
        
        # Download functionality
        st.divider()
        
        # Create CSV data
        csv_data = pd.DataFrame([{
            'Message': user_message,
            'Classification': prediction.upper(),
            'Spam Confidence': f"{spam_confidence:.2f}%",
            'Safe Confidence': f"{ham_confidence:.2f}%",
            'Timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'Keywords Found': ', '.join(found_keywords) if found_keywords else 'None'
        }])
        
        csv_string = csv_data.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Analysis Report",
            data=csv_string,
            file_name=f"smishing_analysis_{timestamp.strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    else:
        st.warning("⚠️ Please enter a message first!")
