import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smishing Detector", page_icon="🛡️", layout="centered")

# 1. TITLE AND DESCRIPTION
st.title("🛡️ AI Smishing Detector")
st.markdown("""
This AI Model is developed by **Osama Saeed** and is trained on the **SMS Spam Collection** dataset.
For feedback and suggestion, please Email: osamas.bizz@gmail.com""")
("""Enter a text message below to check if it's **Safe (Ham)** or **Malicious (Spam/Smishing)**.
""")

# 2. LOAD DATA & TRAIN MODEL
# We use @st.cache_data so it only trains once when the app starts, not every time you click a button.
@st.cache_data
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
    
    return vect, nb

# Load the model (this will show a spinner the first time)
with st.spinner("Training the AI model..."):
    vect, model = load_and_train_model()

# 3. USER INTERFACE
user_message = st.text_area("Paste the SMS message here:", height=100)

if st.button("Analyze Message"):
    if user_message:
        # Transform the user's text into numbers
        input_dtm = vect.transform([user_message])
        # Predict
        prediction = model.predict(input_dtm)[0]

        st.divider() # Adds a visual line
        
        if prediction == 'spam':
            st.error(f"🚨 **ALERT: SPAM DETECTED**")
            st.write("The AI is 98% sure this is a malicious message.")
        else:
            st.success(f"✅ **SAFE MESSAGE**")
            st.write("The AI thinks this message is normal.")
    else:
        st.warning("Please type a message first!")
