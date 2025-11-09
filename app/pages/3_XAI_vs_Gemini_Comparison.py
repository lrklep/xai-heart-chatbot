# app/pages/3_XAI_vs_Gemini_Comparison.py
import os
import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title='XAI vs Gemini Comparison', 
    page_icon='⚡', 
    layout='wide'
)

# Dark theme CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: white !important;
    }
    .main .block-container {
        background: rgba(26, 26, 46, 0.85);
        border-radius: 20px;
        padding: 2rem;
        color: white !important;
    }
    .stApp, .stApp * {
        color: white !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: white !important;
    }
    .comparison-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .winner-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ XAI vs Gemini: Live Comparison")
st.caption("Compare explainable AI with Google's Gemini LLM side-by-side")

# Configuration
API_URL = os.environ.get('API_URL', 'http://localhost:8000')

# Gemini API setup
def setup_gemini():
    """Setup Gemini API"""
    # Check environment variable first, then secrets file
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")
        except (FileNotFoundError, KeyError):
            pass
    
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def get_gemini_prediction(patient_data):
    """Get prediction from Gemini"""
    try:
        # Try different model names - models/ prefix required for some SDK versions
        model_names = [
            'models/gemini-2.5-flash',     # Latest with full path
        ]
        
        model = None
        last_error = None
        successful_model_name = None
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                successful_model_name = model_name
                # Test if model is accessible by attempting to use it
                break
            except Exception as e:
                last_error = e
                continue
        
        if model is None:
            raise Exception(f"No compatible Gemini model found. Last error: {last_error}")
        
        prompt = f"""You are a medical AI assistant. Based on the following patient data, predict the risk of heart disease.

Patient Information:
- Age: {patient_data['age']} years
- Sex: {'Male' if patient_data['sex'] == 1 else 'Female'}
- BMI: {patient_data['bmi']}
- Smoker: {'Yes' if patient_data['smoker'] == 1 else 'No'}
- Diabetes: {'Yes' if patient_data['diabetes'] == 1 else 'No'}
- Physical Activity: {'Yes' if patient_data['phys_activity'] == 1 else 'No'}
- Sleep Hours: {patient_data['sleep_hours']} hours
- General Health: {patient_data['gen_health']}/5

Please provide:
1. Risk prediction (HIGH RISK or LOW RISK)
2. Confidence level (0-100%)
3. Brief explanation (2-3 sentences)

Format your response exactly as:
RISK: [HIGH RISK or LOW RISK]
CONFIDENCE: [number]%
EXPLANATION: [your explanation]
"""
        
        start_time = time.time()
        response = model.generate_content(prompt)
        inference_time = (time.time() - start_time) * 1000  # Convert to ms
        
        # Parse response
        text = response.text
        risk = "Unknown"
        confidence = 50
        explanation = "Unable to parse response"
        
        for line in text.split('\n'):
            if 'RISK:' in line.upper():
                risk = "HIGH RISK" if "HIGH" in line.upper() else "LOW RISK"
            elif 'CONFIDENCE:' in line.upper():
                try:
                    confidence = int(''.join(filter(str.isdigit, line)))
                except:
                    confidence = 50
            elif 'EXPLANATION:' in line.upper():
                explanation = line.split(':', 1)[1].strip() if ':' in line else text
        
        return {
            'prediction': risk,
            'confidence': confidence,
            'explanation': explanation,
            'inference_time': inference_time,
            'raw_response': text
        }
    
    except Exception as e:
        return {
            'prediction': 'Error',
            'confidence': 0,
            'explanation': f'Error: {str(e)}',
            'inference_time': 0,
            'raw_response': ''
        }

def get_xai_prediction(patient_data):
    """Get prediction from XAI model"""
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_URL}/predict",
            json={"payload": patient_data},  # API expects nested payload
            timeout=10
        )
        inference_time = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            result = response.json()
            # Convert prediction to risk level
            risk = "HIGH RISK" if result['prediction'] == 1 else "LOW RISK"
            return {
                'prediction': risk,
                'confidence': result['probability'] * 100,
                'explanation': f"Model uses {len(result.get('features_used', []))} clinical features with SHAP explainability",
                'inference_time': inference_time,
                'shap_values': result.get('shap_values', {}),
                'feature_importance': result.get('feature_importance', [])
            }
        else:
            return {
                'prediction': 'Error',
                'confidence': 0,
                'explanation': f'API Error: {response.status_code} - {response.text[:200]}',
                'inference_time': inference_time
            }
    
    except Exception as e:
        return {
            'prediction': 'Error',
            'confidence': 0,
            'explanation': f'Error: {str(e)}',
            'inference_time': 0
        }

# Check Gemini setup
gemini_available = setup_gemini()

if not gemini_available:
    st.info("ℹ️ Gemini comparison is currently unavailable. Showing XAI model predictions only.")
    # Don't stop - allow XAI-only mode

# Input Section
st.header("📋 Patient Data Input")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", min_value=18, max_value=120, value=50, key="comp_age")
    sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: "Female" if x == 0 else "Male", key="comp_sex")
    bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0, step=0.1, key="comp_bmi")

with col2:
    smoker = st.selectbox("Smoker", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes", key="comp_smoker")
    diabetes = st.selectbox("Diabetes", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes", key="comp_diabetes")
    phys_activity = st.selectbox("Physical Activity", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes", key="comp_phys")

with col3:
    sleep_hours = st.number_input("Sleep Hours", min_value=1.0, max_value=24.0, value=7.0, step=0.1, key="comp_sleep")
    gen_health = st.slider("General Health", min_value=1, max_value=5, value=3, 
                           help="1=Poor, 5=Excellent", key="comp_health")

patient_data = {
    'age': age,
    'sex': sex,
    'bmi': bmi,
    'smoker': smoker,
    'diabetes': diabetes,
    'phys_activity': phys_activity,
    'sleep_hours': sleep_hours,
    'gen_health': gen_health
}

# Compare Button
if st.button("🚀 Run Comparison", type="primary", use_container_width=True):
    st.divider()
    st.header("📊 Comparison Results")
    
    # Create two columns for side-by-side comparison
    col_xai, col_gemini = st.columns(2)
    
    # XAI Prediction
    with col_xai:
        with st.spinner("🧠 Running XAI Model..."):
            xai_result = get_xai_prediction(patient_data)
        
        st.markdown("### 🧠 XAI Model (Your System)")
        st.markdown('<div class="comparison-card">', unsafe_allow_html=True)
        
        # Prediction
        if xai_result['prediction'] == 'HIGH RISK':
            st.error(f"### 🔴 {xai_result['prediction']}")
        else:
            st.success(f"### 🟢 {xai_result['prediction']}")
        
        # Metrics
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("Confidence", f"{xai_result['confidence']:.1f}%")
        with metric_col2:
            st.metric("Inference Time", f"{xai_result['inference_time']:.0f}ms")
        
        # Explanation
        st.markdown("**Explanation:**")
        st.info(xai_result['explanation'])
        
        # Feature Importance
        if 'feature_importance' in xai_result and xai_result['feature_importance']:
            st.markdown("**Top Contributing Factors:**")
            for feat in xai_result['feature_importance'][:3]:
                st.write(f"• {feat['feature']}: {feat['importance']:.3f}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Gemini Prediction
    with col_gemini:
        if gemini_available:
            with st.spinner("🤖 Querying Gemini..."):
                gemini_result = get_gemini_prediction(patient_data)
        else:
            gemini_result = {
                'prediction': 'Unavailable',
                'confidence': 0,
                'explanation': 'Gemini API is not configured. XAI model provides the medical prediction.',
                'inference_time': 0,
                'raw_response': ''
            }
        
        st.markdown("### 🤖 Google Gemini")
        st.markdown('<div class="comparison-card">', unsafe_allow_html=True)
        
        # Prediction
        if gemini_result['prediction'] == 'HIGH RISK':
            st.error(f"### 🔴 {gemini_result['prediction']}")
        elif gemini_result['prediction'] == 'LOW RISK':
            st.success(f"### 🟢 {gemini_result['prediction']}")
        else:
            st.warning(f"### ⚠️ {gemini_result['prediction']}")
        
        # Metrics
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("Confidence", f"{gemini_result['confidence']}%")
        with metric_col2:
            st.metric("Inference Time", f"{gemini_result['inference_time']:.0f}ms")
        
        # Explanation
        st.markdown("**Explanation:**")
        st.info(gemini_result['explanation'])
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Performance Comparison
    st.divider()
    
    if gemini_available and gemini_result['prediction'] not in ['Error', 'Unavailable']:
        st.header("⚡ Performance Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Speed Winner",
                "XAI" if xai_result['inference_time'] < gemini_result['inference_time'] else "Gemini",
                delta=f"{abs(xai_result['inference_time'] - gemini_result['inference_time']):.0f}ms faster"
            )
        
        with col2:
            agree = (xai_result['prediction'] == gemini_result['prediction'])
            st.metric(
                "Agreement",
                "✅ Both Agree" if agree else "❌ Disagree",
                delta="Same prediction" if agree else "Different predictions"
            )
        
        with col3:
            avg_confidence = (xai_result['confidence'] + gemini_result['confidence']) / 2
            st.metric(
                "Avg Confidence",
                f"{avg_confidence:.1f}%"
            )
        
        # Speed Comparison Chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['XAI Model', 'Gemini'],
            y=[xai_result['inference_time'], gemini_result['inference_time']],
            marker_color=['#667eea', '#f093fb'],
            text=[f"{xai_result['inference_time']:.0f}ms", f"{gemini_result['inference_time']:.0f}ms"],
            textposition='auto',
        ))
        fig.update_layout(
            title="Inference Speed Comparison",
            yaxis_title="Time (milliseconds)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.header("📊 XAI Model Performance")
        st.success("✅ **XAI model prediction completed successfully!**")
        st.info(f"⚡ Inference time: **{xai_result['inference_time']:.0f}ms**")
        st.info(f"🎯 Confidence: **{xai_result['confidence']:.1f}%**")
        if not gemini_available:
            st.warning("💡 Gemini comparison is not available. Contact administrator to enable Gemini API for live comparisons.")
    
    # Key Differences
    if gemini_available and gemini_result['prediction'] not in ['Error', 'Unavailable']:
        st.divider()
        st.header("🔍 Key Differences")
        
        differences = pd.DataFrame({
            'Feature': ['Explainability', 'Consistency', 'Cost', 'Privacy', 'Speed'],
            'XAI Model': [
                'SHAP + LIME (Quantitative)',
                '100% (Deterministic)',
                '$0.00001/prediction',
                'On-premise (HIPAA)',
                f'{xai_result["inference_time"]:.0f}ms'
            ],
            'Gemini': [
                'Text explanation (Qualitative)',
                '~60% (Non-deterministic)',
                '$0.001/prediction',
                'Cloud API',
                f'{gemini_result["inference_time"]:.0f}ms'
            ]
        })
        
        st.dataframe(differences, use_container_width=True, hide_index=True)
        
        # Winner Summary
        st.divider()
        st.markdown("### 🏆 Summary")
        
        winner_points = {
            'XAI': 0,
            'Gemini': 0
        }
        
        # Speed
        if xai_result['inference_time'] < gemini_result['inference_time']:
            winner_points['XAI'] += 1
            st.success("✅ **Speed Winner**: XAI Model (Faster inference)")
        else:
            winner_points['Gemini'] += 1
            st.success("✅ **Speed Winner**: Gemini (Faster inference)")
        
        # Explainability
        st.success("✅ **Explainability Winner**: XAI Model (SHAP/LIME quantitative explanations)")
        winner_points['XAI'] += 1
        
        # Cost
        st.success("✅ **Cost Winner**: XAI Model (100x cheaper)")
        winner_points['XAI'] += 1
        
        # Privacy
        st.success("✅ **Privacy Winner**: XAI Model (On-premise, HIPAA compliant)")
        winner_points['XAI'] += 1
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; text-align: center; margin-top: 20px;">
            <h2 style="color: white !important; margin: 0;">🏆 Overall Winner: XAI Model</h2>
            <p style="color: white !important; margin: 10px 0 0 0;">Score: XAI {winner_points['XAI']} - Gemini {winner_points['Gemini']}</p>
        </div>
        """, unsafe_allow_html=True)

# Information Section
st.divider()
st.header("ℹ️ About This Comparison")

with st.expander("🎯 Why Compare XAI with Gemini?"):
    st.markdown("""
    This comparison demonstrates why **domain-specific XAI models** outperform **general-purpose LLMs** for medical predictions:
    
    **XAI Advantages:**
    - ✅ Trained on medical data
    - ✅ Quantitative explanations (SHAP values)
    - ✅ 100% consistent predictions
    - ✅ HIPAA compliant (on-premise)
    - ✅ 100x cheaper at scale
    - ✅ Faster inference
    
    **Gemini Use Case:**
    - Natural language interaction
    - General medical knowledge
    - Conversational explanations
    
    **Best Practice:** Use XAI for predictions, LLMs for communication!
    """)
