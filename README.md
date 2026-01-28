# 🛡️ SmishGuard - AI Smishing Detector

<div align="center">

![SmishGuard Logo](https://cdn-icons-png.flaticon.com/512/2092/2092663.png)

**An intelligent SMS phishing detection system powered by machine learning**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-FF4B4B.svg)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-latest-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [How It Works](#-how-it-works) • [Contributing](#-contributing)

</div>

---

## 📋 Overview

**SmishGuard** is an AI-powered web application designed to detect SMS phishing (smishing) attacks in real-time. Using a **Naive Bayes** classifier trained on thousands of SMS messages, SmishGuard helps users identify potentially malicious text messages before they become victims of fraud.

### 🎯 Project Purpose

This project serves as an **AI Capstone** demonstration, showcasing:
- Machine learning implementation for text classification
- Real-world application of Natural Language Processing (NLP)
- User-friendly web interface development with Streamlit
- Cybersecurity awareness through AI-driven solutions

---

## ✨ Features

### Core Functionality
- **🔍 Real-Time Analysis**: Instant detection of suspicious SMS patterns
- **📊 Confidence Scoring**: Displays spam probability with visual indicators
- **🎨 Intuitive UI**: Clean, modern interface built with Streamlit
- **📝 Session History**: Tracks recent message analyses during the session
- **🚀 Fast Performance**: Cached model for quick predictions

### Technical Highlights
- **Naive Bayes Classification**: Proven effective for text-based spam detection
- **CountVectorizer Feature Extraction**: Converts text into numerical features
- **Enhanced Training Dataset**: Includes edge cases for improved accuracy
- **Responsive Design**: Wide layout optimized for desktop and mobile

---

## 🎬 Demo

### User Interface Preview

**Main Analysis Screen:**
```
┌─────────────────────────────────────────────────┐
│  📝 Input Message      │  📊 Analysis Results   │
│                        │                        │
│  [Text Area]           │  ✅ SAFE MESSAGE       │
│                        │  Safety Score: 94.2%   │
│  🔍 Analyze Message    │  [Progress Bar]        │
└─────────────────────────────────────────────────┘
```

### Example Outputs

**Spam Detection:**
```
🚨 POTENTIAL THREAT DETECTED
Spam Confidence: 98.7%
Threat Level: High Risk
```

**Safe Message:**
```
✅ SAFE MESSAGE
Safety Score: 95.3%
Threat Level: Low
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection (for initial model training)

### Step-by-Step Guide

1. **Clone the Repository**
   ```bash
   git clone https://github.com/pro-osama-saeed/ai-capstone.git
   cd ai-capstone
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

5. **Access the App**
   - Open your browser and navigate to: `http://localhost:8501`

---

## 💻 Usage

### Basic Operation

1. **Launch the Application**
   ```bash
   streamlit run app.py
   ```

2. **Input SMS Message**
   - Paste or type the suspicious SMS text into the input area
   - Click the **🔍 Analyze Message** button

3. **Review Results**
   - **Green ✅**: Message is safe
   - **Red 🚨**: Potential phishing threat detected
   - Check the confidence score and threat level indicator

### Example Messages to Test

**Legitimate Messages:**
```
"Hey, are you free tomorrow? I won tickets to the game!"
"Your package is waiting at the front desk."
"Reminder: Your dentist appointment is tomorrow at 3 PM."
```

**Phishing Messages:**
```
"URGENT: Your account will be locked. Click here immediately!"
"Congratulations! You've won $10,000. Claim now: [link]"
"Hi, please update your banking details using the following link."
```

---

## 🧠 How It Works

### Architecture Overview

```
User Input → Text Preprocessing → Feature Extraction → ML Model → Prediction
                                       ↓
                                CountVectorizer → Naive Bayes Classifier
```

### Machine Learning Pipeline

1. **Data Loading**
   - Base dataset: 5,572 SMS messages from [PyConv 2016 Tutorial](https://github.com/justmarkham/pycon-2016-tutorial)
   - Enhanced with custom edge cases for improved detection

2. **Feature Extraction**
   - **CountVectorizer**: Converts text into numerical word count features
   - Creates a Document-Term Matrix (DTM)

3. **Model Training**
   - **Algorithm**: Multinomial Naive Bayes
   - **Training Data**: 5,577 labeled SMS messages (ham/spam)
   - **Caching**: Model is cached using `@st.cache_data` for performance

4. **Prediction**
   - Input message is vectorized
   - Model predicts: `spam` or `ham` (legitimate)
   - Confidence score calculated from probability distribution

### Training Data Enhancement

The model includes these custom edge cases:

| Label | Example Message |
|-------|----------------|
| Ham   | "Hey, are you free tomorrow? I won tickets to the game!" |
| Spam  | "Hello friend, I have a business proposal for you. Please email me." |
| Ham   | "Your package is waiting at the front desk." |
| Spam  | "Hi, please update your banking details using the following link. URGENT" |
| Spam  | "Hey buddy, share OTP, so I can transfer money. ITS URGENT" |

---

## 📂 Project Structure

```
ai-capstone/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
│
└── .streamlit/            # (Optional) Streamlit configuration
    └── config.toml
```

### File Descriptions

- **app.py**: Contains the entire application logic including:
  - Page configuration
  - Model training and caching
  - UI components
  - Prediction logic
  - Session history tracking

- **requirements.txt**: Lists all required Python packages:
  - `streamlit`: Web framework
  - `pandas`: Data manipulation
  - `scikit-learn`: Machine learning library

---

## 🔧 Technical Details

### Dependencies

```
streamlit       # Web application framework
pandas          # Data processing
scikit-learn    # Machine learning (CountVectorizer, MultinomialNB)
```

### Model Specifications

- **Algorithm**: Multinomial Naive Bayes
- **Vectorization**: Bag-of-Words (CountVectorizer)
- **Training Size**: ~5,577 messages
- **Classes**: Binary (spam/ham)
- **Performance**: Cached for instant predictions

### Key Functions

```python
@st.cache_data
def load_and_train_model():
    """Loads dataset, trains model, returns vectorizer and classifier"""
    # Returns: (CountVectorizer, MultinomialNB)
```

---

## 📊 Features Breakdown

### 1. Page Configuration
- Custom page title and icon
- Wide layout for better space utilization
- Expanded sidebar by default

### 2. Sidebar Information
- Project overview
- How it works explanation
- Developer information
- Contact details
- Version information

### 3. Main Interface
- Two-column layout (Input | Results)
- Form-based input (prevents constant reloading)
- Real-time prediction on submit

### 4. Analysis Results
- Color-coded threat indicators
- Confidence metrics
- Progress bar visualization
- Contextual messages

### 5. Session History
- Stores recent analyses
- Shows last 3 checked messages
- Color-coded markers (🔴 Spam / 🟢 Safe)

---

## 🎨 UI/UX Design

### Color Scheme
- **Safe Messages**: Green (✅)
- **Spam Messages**: Red (🚨)
- **Neutral**: Blue information boxes

### Custom CSS
- Enhanced background styling
- Bold, readable fonts
- Responsive layout

### User Flow
```
1. User lands on page → Model loads automatically
2. User enters message → Clicks analyze
3. Results display → Color-coded with metrics
4. History updates → Shows recent checks
```

---

## 🛠️ Customization

### Adding More Training Data

Edit the `load_and_train_model()` function in `app.py`:

```python
new_data = pd.DataFrame([
    {'label': 'ham', 'message': 'Your custom message'},
    {'label': 'spam', 'message': 'Your spam example'},
])
```

### Changing the Model

Replace `MultinomialNB()` with another classifier:

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
```

### UI Customization

Modify the custom CSS in the `st.markdown()` section:

```python
st.markdown("""
<style>
    /* Your custom styles here */
</style>
""", unsafe_allow_html=True)
```

---

## 📈 Future Enhancements

### Planned Features
- [ ] Export analysis reports (PDF/CSV)
- [ ] Batch message analysis
- [ ] Multi-language support
- [ ] Deep learning model option (LSTM/BERT)
- [ ] Database integration for persistent history
- [ ] User feedback loop for model improvement
- [ ] API endpoint for external integrations
- [ ] Mobile app version

### Potential Improvements
- Add TF-IDF vectorization option
- Implement cross-validation metrics display
- Include confusion matrix visualization
- Add model performance dashboard
- Support for URL extraction and analysis
- Phone number pattern detection

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Issues
1. Check existing issues first
2. Create a new issue with detailed description
3. Include steps to reproduce (if bug)

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add comments for complex logic
- Test thoroughly before submitting
- Update documentation as needed

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developer

**Osama Saeed**
- GitHub: [@pro-osama-saeed](https://github.com/pro-osama-saeed)
- Email: [osamas.bizz@gmail.com](mailto:osamas.bizz@gmail.com)

---

## 🙏 Acknowledgments

- **Dataset Source**: [PyConv 2016 Tutorial](https://github.com/justmarkham/pycon-2016-tutorial) by Justin Markham
- **Framework**: Streamlit for the amazing web framework
- **ML Library**: scikit-learn for robust machine learning tools
- **Icons**: Flaticon for the shield icon

---

## 📚 Resources

### Learn More About
- [Naive Bayes Classification](https://scikit-learn.org/stable/modules/naive_bayes.html)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SMS Spam Detection](https://en.wikipedia.org/wiki/SMS_spam)
- [Phishing Awareness](https://www.consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams)

### Related Projects
- [Spam Classifier Tutorial](https://github.com/justmarkham/pycon-2016-tutorial)
- [Text Classification with scikit-learn](https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)

---

## 📞 Support

Having issues? Try these steps:

1. **Check the Issues Tab**: Someone might have had the same problem
2. **Update Dependencies**: `pip install --upgrade -r requirements.txt`
3. **Clear Streamlit Cache**: `streamlit cache clear`
4. **Contact Developer**: Email [osamas.bizz@gmail.com](mailto:osamas.bizz@gmail.com)

---

## 🔖 Version History

- **v2.0** (January 26, 2026)
  - Enhanced UI with two-column layout
  - Added session history feature
  - Improved confidence scoring
  - Updated training dataset

- **v1.0** (Initial Release)
  - Basic spam detection functionality
  - Streamlit interface
  - Naive Bayes model

---

## ⚠️ Disclaimer

This tool is designed for **educational purposes** and basic phishing detection. While it provides helpful analysis, it should not be the sole method for determining message authenticity. Always exercise caution with:

- Messages requesting personal information
- Unexpected links or attachments
- Urgent action requests
- Messages from unknown senders

**Stay vigilant and verify suspicious messages through official channels.**

---

<div align="center">

**Made with ❤️ for AI Capstone Project**

⭐ Star this repo if you found it helpful!

[Report Bug](https://github.com/pro-osama-saeed/ai-capstone/issues) • [Request Feature](https://github.com/pro-osama-saeed/ai-capstone/issues)

</div>
