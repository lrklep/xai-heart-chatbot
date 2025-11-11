# ❤️ Heart Disease Risk Assessment System (XAI)

> **An interactive, user-friendly chatbot for heart disease risk prediction powered by Explainable AI (SHAP & LIME)**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36.0-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

### 🎯 **User-Friendly Interface**
- **Two Input Modes**: Interactive form or conversational chat interface
- **Real-time Validation**: Instant feedback on input correctness with helpful error messages
- **Smart Field Helpers**: Contextual help text, examples, and range information for each field
- **Progress Tracking**: Visual progress indicator showing completion status

### 🔬 **Advanced Analytics**
- **Risk Prediction**: ML-powered heart disease risk assessment with confidence scores
- **Interactive Visualizations**: Beautiful Plotly gauges, charts, and graphs
- **Explainable AI**: 
  - SHAP (SHapley Additive exPlanations) for global feature importance
  - LIME (Local Interpretable Model-agnostic Explanations) for local predictions
- **Educational Content**: Learn about XAI and compare with Black Box AI

### 🎨 **Modern Design**
- **Glass Morphism UI**: Modern, aesthetic interface with gradient backgrounds
- **Responsive Layout**: Works on desktop and tablet devices
- **Animated Elements**: Smooth transitions and hover effects
- **Color-Coded Risk Levels**: Intuitive visual feedback (green, yellow, orange, red)

### 📊 **Data Management**
- **Sample Data Loading**: Quick testing with pre-filled examples
- **Export Capabilities**: Download results as TXT or CSV
- **Input Summary**: Review all entered information before analysis

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager
- Virtual environment (recommended)

### Installation & Setup

#### **Option 1: Local Development (Windows)**

```powershell
# 1. Clone/Navigate to project directory
cd C:\path\to\xai-heart-chatbot

# 2. Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train the model (creates model files and SHAP explainer cache)
python train/train.py

# 5. Start the API server (Terminal 1)
uvicorn api.api:app --host 0.0.0.0 --port 8000

# 6. Start the Streamlit UI (Terminal 2)
$env:API_URL='http://localhost:8000'
streamlit run app/streamlit_app.py
```

#### **Option 2: Docker (API Only)**

```bash
docker build -t xai-heart-api .
docker run -p 8000:8000 xai-heart-api
```

#### **Option 3: Docker Compose (Full Stack)**

```bash
docker compose up --build
```

---

## 🌐 Access the Application

Once both servers are running:

| Service | URL | Description |
|---------|-----|-------------|
| 🎨 **Main App** | http://localhost:8501 | Interactive chatbot interface |
| 📊 **Research Summary** | Sidebar → "Research Summary" | Paper analysis and metrics |
| ⚖️ **XAI Comparison** | Sidebar → "Black Box Comparison" | Demo showing XAI impact |
| 🔧 **API Docs** | http://localhost:8000/docs | FastAPI interactive documentation |
| ❤️ **Health Check** | http://localhost:8000/health | API status endpoint |

---

## 📖 User Guide

### **Input Methods**

#### **1. Interactive Form Mode** (Recommended for New Users)
- Select all fields at once with dropdowns and text inputs
- Real-time validation shows green checkmarks or red warnings
- Submit all data together for instant analysis

#### **2. Chat Interface Mode** (Conversational Experience)
- Answer questions one at a time
- AI validates each response before proceeding
- More engaging, tutorial-like experience

### **Input Fields & Validation**

| Field | Type | Valid Range | Example |
|-------|------|-------------|---------|
| 👤 **Age** | Number | 18-120 years | 45 |
| ⚧ **Sex** | Binary | 0=Female, 1=Male | 1 |
| ⚖️ **BMI** | Decimal | 10.0-60.0 | 27.5 |
| 🚬 **Smoker** | Binary | 0=No, 1=Yes | 0 |
| 💉 **Diabetes** | Binary | 0=No, 1=Yes | 1 |
| 🏃 **Physical Activity** | Binary | 0=No, 1=Yes | 1 |
| 😴 **Sleep Hours** | Number | 0-24 hours | 7 |
| ❤️ **General Health** | Scale | 1=Poor to 5=Excellent | 3 |

### **Understanding Results**

#### **Risk Levels**
- 🟢 **Low Risk (0-30%)**: Continue healthy habits, annual checkups
- 🟡 **Moderate-Low (30-50%)**: Discuss prevention with doctor
- 🟠 **Moderate-High (50-70%)**: Medical consultation recommended
- 🔴 **High Risk (70-100%)**: Comprehensive evaluation needed

#### **Explanation Tabs**
- **SHAP Analysis**: Shows which features contribute most to risk globally
- **LIME Analysis**: Explains this specific prediction locally
- **Learn More**: Educational content about XAI methodology

### **Actions Available**
- 📄 **Download Report**: Save results as text file with timestamp
- 📊 **Download Data**: Export input data as CSV
- 🔄 **New Assessment**: Reset and start fresh analysis
- 📥 **Load Sample**: Fill with example patient data

---

## 🏗️ Architecture

### **Technology Stack**

```
┌─────────────────────────────────────────────────────────┐
│                  Frontend (Streamlit)                    │
│  • Interactive Forms & Chat UI                           │
│  • Plotly Visualizations (Gauges, Charts)               │
│  • Real-time Input Validation                            │
│  • Responsive Design with CSS3                           │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP REST API
┌────────────────▼────────────────────────────────────────┐
│                  Backend (FastAPI)                       │
│  • /predict - Risk prediction endpoint                   │
│  • /explain - SHAP & LIME explanations                   │
│  • /health - Server status                               │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│               ML Pipeline (scikit-learn)                 │
│  • RandomForestClassifier (400 trees)                    │
│  • Preprocessing Pipeline                                │
│  • SHAP TreeExplainer (cached)                           │
│  • LIME TabularExplainer                                 │
└─────────────────────────────────────────────────────────┘
```

### **Key Components**

- **`app/streamlit_app.py`**: Main chatbot interface with dual input modes
- **`api/api.py`**: FastAPI backend with prediction and explanation endpoints
- **`train/train.py`**: Model training pipeline with SHAP caching
- **`models/`**: Trained model artifacts (model.joblib, preproc.joblib, shap_explainer.joblib)
- **`data/heart.csv`**: Training dataset
- **`tests/smoke_test.py`**: API integration tests

---

## 🎓 Educational Resources

### **Pages Available**

1. **Research Summary** (`app/pages/1_Research_Summary.py`)
   - Analysis of Muneer et al. (IJACSA 2024) paper
   - Comparison with local model metrics
   - Interactive sections with expandable details

2. **Black Box Comparison** (`app/pages/2_Black_Box_Comparison.py`)
   - Side-by-side comparison of Black Box vs XAI
   - Interactive SHAP demonstrations
   - Real-world scenario examples
   - Trust metrics visualization
   - Perfect for presentations and demos

### **Documentation**

- **`docs/ARCHITECTURE.md`**: Detailed system architecture and design decisions
- **`docs/slides.md`**: PowerPoint-ready presentation content

---

## 🔧 Technical Details

### **Input Validation System**

The application includes comprehensive client-side validation:

- **Age Validator**: Checks range 18-120, provides feedback
- **BMI Validator**: Validates 10-60 range, categorizes (underweight/normal/overweight/obese)
- **Binary Validators**: Ensures 0/1 values with Yes/No labels
- **Health Rating**: Validates 1-5 scale with descriptive labels
- **Sleep Hours**: Checks 0-24 range with health feedback

### **Model Performance**

- **Algorithm**: Random Forest Classifier
- **Trees**: 400 estimators
- **Class Balancing**: Weighted to handle imbalanced data
- **Metrics**: ROC AUC, Accuracy, Precision, Recall (see `models/metrics.json`)

### **XAI Implementation**

#### **SHAP (TreeExplainer)**
- Cached with background data for performance
- Returns feature contributions for each prediction
- Positive values increase risk, negative values decrease risk
- Based on game theory (Shapley values)

#### **LIME (TabularExplainer)**
- Generates local linear approximations
- 100 samples for neighborhood exploration
- 50 background samples for stability
- Feature weights specific to individual prediction

### **Performance Optimizations**

- ✅ Dense matrix output (`sparse_output=False`) for SHAP/LIME compatibility
- ✅ SHAP explainer cached during training (faster inference)
- ✅ Reduced LIME samples (100 vs 5000) for speed
- ✅ DataFrame input for proper column selection
- ✅ 120-second timeout for explanation generation

### **Error Handling**

- Connection errors with helpful messages
- Timeout handling for long-running explanations
- Input validation with specific error messages
- Graceful degradation if explanations fail
- API health monitoring

---

## 📊 Sample Data

Use the "📥 Load Sample Data" button to test with:

```python
{
    'age': 63,              # 63 years old
    'sex': 1,               # Male
    'bmi': 28.5,            # Overweight
    'smoker': 0,            # Non-smoker
    'diabetes': 1,          # Has diabetes
    'phys_activity': 1,     # Physically active
    'sleep_hours': 7,       # Healthy sleep
    'gen_health': 3         # Good health
}
```

Expected result: ~85% risk probability (high risk)

---

## 🎨 UI/UX Features

### **Visual Design**
- 🌈 Modern gradient backgrounds with glass morphism
- 🎯 Color-coded risk levels (green → yellow → orange → red)
- ✨ Smooth animations and hover effects
- 📱 Responsive layout for different screen sizes
- 🎭 Consistent theming across all pages

### **User Experience**
- 🔄 Real-time validation feedback
- 📊 Progress tracking (X/8 fields completed)
- 💡 Contextual help text and examples
- 🎓 Educational tooltips and explanations
- ⚡ Fast response times with loading indicators

### **Accessibility**
- 🎨 High contrast color schemes
- 📝 Clear labels and descriptions
- 🔤 Readable font sizes
- 📊 Alternative text for visualizations
- ⌨️ Keyboard navigation support

---

## 🐛 Troubleshooting

### **API Connection Failed**
```
❌ Cannot connect to API at http://localhost:8000
```
**Solution**: Ensure API server is running:
```powershell
uvicorn api.api:app --host 0.0.0.0 --port 8000
```

### **Module Not Found**
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: Activate virtual environment and install dependencies:
```powershell
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### **Model Files Missing**
```
FileNotFoundError: models/model.joblib
```
**Solution**: Train the model first:
```powershell
python train/train.py
```

### **Explanation Timeout**
```
⏱️ Explanation generation timed out
```
**Solution**: This is normal for complex models. The prediction still works; explanations are optional.

### **Port Already in Use**
```
OSError: [WinError 10048] Only one usage of each socket address
```
**Solution**: Change ports or kill existing processes:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000
# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- 🌍 Multi-language support
- 📱 Mobile-responsive design
- 🔐 User authentication
- 💾 Database integration for history
- 📈 More ML models (comparison mode)
- 🎨 Additional visualization types
- 🧪 More comprehensive testing

---

## ⚠️ Disclaimer

**IMPORTANT MEDICAL DISCLAIMER:**

This application is an **educational demonstration** of explainable AI technology for research and learning purposes only.

- ❌ **NOT** a medical diagnostic tool
- ❌ **NOT** a substitute for professional medical advice
- ❌ **NOT** validated for clinical use
- ❌ **NOT** approved by regulatory agencies (FDA, etc.)

**Always consult qualified healthcare professionals for medical decisions, diagnosis, and treatment.**

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Authors & Acknowledgments

- **Development**: CODEBLOODED Team
- **Research**: Based on Muneer et al. (IJACSA 2024)
- **Technology**: Built with FastAPI, Streamlit, SHAP, LIME
- **Dataset**: Heart disease indicators from public health data

---

## 📞 Support

For issues, questions, or suggestions:
- 🐛 Report bugs via GitHub Issues
- 💡 Suggest features via Pull Requests
- 📧 Contact: **will update soon**

---

## 🌟 Star this Repository

If you found this project helpful, please consider giving it a ⭐!

---

<div align="center">
  <p><strong>Built with ❤️ for Healthcare AI Education</strong></p>
  <p><em>Making AI Transparent, Trustworthy, and Understandable</em></p>
</div>
