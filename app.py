import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SmishGuard | AI Detector",
    page_icon="🛡️",
    layout="wide", # Changed to wide for better use of space
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS FOR BETTER UI ---
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MODEL LOADING & TRAINING ---
@st.cache_data
def load_and_train_model():
    # Load Original Data
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    col_names = ['label', 'message']
    data = pd.read_csv(url, sep='\t', header=None, names=col_names)

    # Inject New Data (Edge Cases)
    new_data = pd.DataFrame([
        {'label': 'ham', 'message': 'Hey, are you free tomorrow? I won tickets to the game!'},
        {'label': 'spam', 'message': 'Hello friend, I have a business proposal for you. Please email me.'},
        {'label': 'ham', 'message': 'Your package is waiting at the front desk.'},
        {'label': 'spam', 'message': 'Hi, please update your banking details using the following link. URGENT'},
        {'label': 'spam', 'message': 'Hey buddy, share OTP, so I can transfer money. ITS URGENT'}
    ])
    data = pd.concat([data, new_data], ignore_index=True)

    # Train Model
    X = data['message']
    y = data['label']
    
    vect = CountVectorizer()
    X_dtm = vect.fit_transform(X)
    nb = MultinomialNB()
    nb.fit(X_dtm, y)
    
    return vect, nb

# Initialize Model
with st.spinner("Initializing AI Defense Systems..."):
    vect, model = load_and_train_model()

# --- 4. SIDEBAR INFO ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.title("SmishGuard 🛡️")
    st.markdown("### How it works")
    st.info("This tool uses a **Naive Bayes** machine learning model trained on thousands of SMS logs to detect patterns common in phishing attacks.")
    
    st.markdown("---")
    st.markdown("**Developer Group:**")
    st.markdown("* - Osama Saeed*")
    st.markdown("* - Areeba Waheed*")
    st.markdown("* - Mohsin Bin Aftab*")
    st.markdown("**Project:** AI Capstone")
    st.markdown("**Github:**@pro-osama-saeed")
    st.markdown("Feedback & Suggestion: 📧 [osamas.bizz@gmail.com](mailto:osamas.bizz@gmail.com)")
    st.caption("v2.1 | Updated 3rd Feb, 2026")

# --- 5. MAIN INTERFACE ---
st.title("🛡️ AI Smishing Detector")
st.markdown("##### Analyze suspicious text messages instantly.")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Input Message")
    # Using a form so the page doesn't reload on every keystroke
    with st.form("analysis_form"):
        user_message = st.text_area("Paste the SMS text here:", height=150, placeholder="e.g. You have won a lottery! Click here to claim...")
        submit_button = st.form_submit_button("🔍 Analyze Message", type="primary")

with col2:
    st.subheader("📊 Analysis Results")
    if submit_button and user_message:
        # Transform and Predict
        input_dtm = vect.transform([user_message])
        prediction = model.predict(input_dtm)[0]
        
        # Get Probability (Confidence Score)
        # returns [[prob_ham, prob_spam]]
        proba = model.predict_proba(input_dtm)[0] 
        spam_score = proba[1]
        
        if prediction == 'spam':
            st.error("🚨 **POTENTIAL THREAT DETECTED**")
            st.metric(label="Spam Confidence", value=f"{spam_score*100:.1f}%", delta="High Risk", delta_color="inverse")
            st.progress(spam_score, text="Threat Level")
            st.write("This message contains patterns highly typical of malicious phishing.")
        else:
            st.success("✅ **SAFE MESSAGE**")
            st.metric(label="Safety Score", value=f"{(1-spam_score)*100:.1f}%", delta="Safe")
            st.progress(spam_score, text="Threat Level")
            st.write("This message appears to be a standard communication.")
            
    elif submit_button and not user_message:
        st.warning("Please enter some text to analyze.")
    else:
        st.info("Awaiting input...")

# --- 6. HISTORY LOG (Optional UX Feature) ---
if "history" not in st.session_state:
    st.session_state.history = []

if submit_button and user_message:
    st.session_state.history.insert(0, {"msg": user_message[:50] + "...", "type": prediction})

if st.session_state.history:
    st.divider()
    st.caption("🕒 Recent Session Checks")
    for item in st.session_state.history[:3]: # Show last 3
        if item['type'] == 'spam':
            st.markdown(f"🔴 **Spam:** {item['msg']}")
        else:
            st.markdown(f"🟢 **Safe:** {item['msg']}")

