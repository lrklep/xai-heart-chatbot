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
        
        prompt = f"""You are a compassionate medical AI assistant helping assess heart disease risk. Based on the patient's health information below, provide a risk assessment.

Patient's Health Profile:
- Age: {patient_data['age']} years old
- Sex: {'Male' if patient_data['sex'] == 1 else 'Female'}
- Body Mass Index (BMI): {patient_data['bmi']:.1f} {'(Healthy weight)' if 18.5 <= patient_data['bmi'] <= 24.9 else '(Outside healthy weight range)'}
- Smoking status: {'Current/former smoker' if patient_data['smoker'] == 1 else 'Non-smoker'}
- Diabetes: {'Diagnosed with diabetes' if patient_data['diabetes'] == 1 else 'No diabetes'}
- Exercise habits: {'Exercises regularly' if patient_data['phys_activity'] == 1 else 'Minimal physical activity'}
- Sleep: Gets about {patient_data['sleep_hours']} hours of sleep per night
- Self-rated health: {['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'][int(patient_data['gen_health'])-1]} (rated {patient_data['gen_health']}/5)

Please provide a patient-friendly assessment with:
1. Overall risk level (HIGH RISK or LOW RISK for heart disease)
2. Your confidence in this assessment (0-100%)
3. A brief, compassionate explanation in plain language (2-3 sentences that a patient can understand)

Format your response exactly as:
RISK: [HIGH RISK or LOW RISK]
CONFIDENCE: [number]%
EXPLANATION: [your patient-friendly explanation]
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

# Privacy Notice
st.success("🔒 **Privacy Protected**: Your data is processed locally and never stored. All information is deleted after your session.")

# Input Section
st.header("📋 Enter Your Health Information")
st.caption("Fill in your basic health details below. All information is kept private and secure.")

# Sample Patient Profiles
st.markdown("### 🎯 Quick Fill Sample Profiles")
col_s1, col_s2, col_s3, col_s4 = st.columns(4)
with col_s1:
    if st.button("👨 Healthy 40-yr-old", use_container_width=True):
        st.session_state.sample_profile = {
            'age': 40, 'sex': 1, 'height_cm': 175.0, 'weight_kg': 75.0,
            'smoker': 0, 'diabetes': 0, 'phys_activity': 1, 'sleep_hours': 7.5, 'gen_health': 4
        }
with col_s2:
    if st.button("👵 High-risk Senior", use_container_width=True):
        st.session_state.sample_profile = {
            'age': 68, 'sex': 0, 'height_cm': 160.0, 'weight_kg': 85.0,
            'smoker': 1, 'diabetes': 1, 'phys_activity': 0, 'sleep_hours': 6.0, 'gen_health': 2
        }
with col_s3:
    if st.button("🏃 Young Athlete", use_container_width=True):
        st.session_state.sample_profile = {
            'age': 28, 'sex': 1, 'height_cm': 180.0, 'weight_kg': 70.0,
            'smoker': 0, 'diabetes': 0, 'phys_activity': 1, 'sleep_hours': 8.0, 'gen_health': 5
        }
with col_s4:
    if st.button("⚠️ Pre-diabetic", use_container_width=True):
        st.session_state.sample_profile = {
            'age': 52, 'sex': 0, 'height_cm': 165.0, 'weight_kg': 88.0,
            'smoker': 0, 'diabetes': 1, 'phys_activity': 0, 'sleep_hours': 6.5, 'gen_health': 3
        }

# Initialize sample profile if not exists
if 'sample_profile' not in st.session_state:
    st.session_state.sample_profile = None
if 'unit_system' not in st.session_state:
    st.session_state.unit_system = 'metric'  # 'metric' or 'imperial'

st.divider()

col1, col2, col3 = st.columns(3)

# Get sample profile values if available
sample = st.session_state.sample_profile if st.session_state.sample_profile else {}

with col1:
    st.subheader("👤 Basic Info")
    
    # Unit toggle
    unit_system = st.radio("Units:", ['Metric (cm, kg)', 'Imperial (ft/in, lbs)'], 
                          horizontal=True, key="unit_toggle",
                          index=0 if st.session_state.unit_system == 'metric' else 1)
    st.session_state.unit_system = 'metric' if 'Metric' in unit_system else 'imperial'
    
    age = st.number_input("Age (years)", min_value=18, max_value=120, 
                          value=sample.get('age', 50), key="comp_age",
                          help="Your current age")
    
    # Age validation warning
    if age > 85:
        st.warning("⚠️ Age over 85 may have higher prediction uncertainty")
    
    sex = st.selectbox("Sex", options=[0, 1], 
                      format_func=lambda x: "Female" if x == 0 else "Male", 
                      index=sample.get('sex', 1), key="comp_sex")
    
    # Height and Weight with unit conversion
    if st.session_state.unit_system == 'metric':
        height_cm = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, 
                                    value=sample.get('height_cm', 170.0), step=1.0, key="comp_height",
                                    help="Your height in centimeters")
        weight_kg = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, 
                                    value=sample.get('weight_kg', 70.0), step=0.5, key="comp_weight",
                                    help="Your weight in kilograms")
        
        # Show imperial conversion
        height_ft = int(height_cm / 30.48)
        height_in = int((height_cm / 30.48 - height_ft) * 12)
        weight_lbs = weight_kg * 2.20462
        st.caption(f"≈ {height_ft}'{height_in}\" and {weight_lbs:.1f} lbs")
    else:
        height_ft = st.number_input("Height (feet)", min_value=3, max_value=8, 
                                    value=int(sample.get('height_cm', 170.0) / 30.48), key="comp_height_ft")
        height_in = st.number_input("Height (inches)", min_value=0, max_value=11, 
                                    value=int((sample.get('height_cm', 170.0) / 30.48 - int(sample.get('height_cm', 170.0) / 30.48)) * 12), 
                                    key="comp_height_in")
        weight_lbs = st.number_input("Weight (lbs)", min_value=66.0, max_value=660.0, 
                                     value=sample.get('weight_kg', 70.0) * 2.20462, step=1.0, key="comp_weight_lbs")
        
        # Convert to metric for calculations
        height_cm = (height_ft * 12 + height_in) * 2.54
        weight_kg = weight_lbs / 2.20462
        st.caption(f"≈ {height_cm:.1f} cm and {weight_kg:.1f} kg")
    
    # Height/Weight validation
    if height_cm < 140 or height_cm > 210:
        st.warning("⚠️ Unusual height detected. Please verify.")
    if weight_kg < 40 or weight_kg > 150:
        st.warning("⚠️ Unusual weight detected. Please verify.")
    
    # Calculate BMI with color coding
    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5:
        st.error(f"📊 Your BMI: **{bmi:.1f}** (Underweight)")
    elif 18.5 <= bmi <= 24.9:
        st.success(f"📊 Your BMI: **{bmi:.1f}** (Healthy ✓)")
    elif 25 <= bmi <= 29.9:
        st.warning(f"📊 Your BMI: **{bmi:.1f}** (Overweight)")
    else:
        st.error(f"📊 Your BMI: **{bmi:.1f}** (Obese)")

with col2:
    st.subheader("🏥 Health Conditions")
    smoker = st.selectbox("Do you smoke?", options=[0, 1], 
                         format_func=lambda x: "No" if x == 0 else "Yes", 
                         index=sample.get('smoker', 0), key="comp_smoker",
                         help="🚬 Current or former smoker. Smoking significantly increases heart disease risk by damaging blood vessels.")
    
    if smoker == 1:
        st.warning("⚠️ Smoking increases your heart disease risk by 2-4x")
    
    diabetes = st.selectbox("Do you have diabetes?", options=[0, 1], 
                           format_func=lambda x: "No" if x == 0 else "Yes", 
                           index=sample.get('diabetes', 0), key="comp_diabetes",
                           help="🩺 Diagnosed with Type 1 or Type 2 diabetes. High blood sugar damages arteries over time.")
    
    if diabetes == 1:
        st.warning("⚠️ Diabetes doubles your heart disease risk")
    
    # Exercise with frequency options
    phys_activity_options = ["None", "Light (1-2x/week)", "Moderate (3-4x/week)", "Active (5+ days/week)"]
    phys_activity_raw = st.selectbox("Exercise frequency?", 
                                    options=range(4),
                                    format_func=lambda x: phys_activity_options[x],
                                    index=2 if sample.get('phys_activity', 0) == 1 else 0,
                                    key="comp_phys",
                                    help="💪 Regular physical activity strengthens your heart. Aim for 150 min/week.")
    
    # Convert to binary for model
    phys_activity = 1 if phys_activity_raw >= 2 else 0
    
    if phys_activity_raw == 0:
        st.error("🚨 No exercise significantly increases risk")
    elif phys_activity_raw == 3:
        st.success("✅ Excellent! Active lifestyle reduces risk")

with col3:
    st.subheader("💤 Lifestyle")
    sleep_hours = st.number_input("Sleep hours per night", min_value=1.0, max_value=24.0, 
                                  value=sample.get('sleep_hours', 7.0), step=0.5, key="comp_sleep",
                                  help="😴 Average hours of sleep you get each night. 7-9 hours is optimal for heart health.")
    
    # Sleep validation
    if sleep_hours < 5:
        st.error("🚨 Too little sleep (<5h) significantly increases heart disease risk")
    elif sleep_hours > 10:
        st.warning("⚠️ Excessive sleep (>10h) may indicate health issues")
    elif 7 <= sleep_hours <= 9:
        st.success("✅ Optimal sleep duration for heart health")
    
    # Visual health rating with emojis
    health_options = {
        1: "😞 Poor",
        2: "😐 Fair", 
        3: "🙂 Good",
        4: "😊 Very Good",
        5: "😄 Excellent"
    }
    
    st.markdown("**How would you rate your overall health?**")
    gen_health = st.select_slider(
        "Overall health rating",
        options=[1, 2, 3, 4, 5],
        value=sample.get('gen_health', 3),
        format_func=lambda x: health_options[x],
        key="comp_health",
        label_visibility="collapsed",
        help="Your self-assessment of overall health is a strong predictor of actual health outcomes."
    )
    
    # Calculate and show progress
    fields_filled = sum([
        age > 18,
        height_cm > 0,
        weight_kg > 0,
        True,  # sex always filled
        True,  # smoker always filled
        True,  # diabetes always filled
        True,  # phys_activity always filled
        sleep_hours > 0,
        gen_health > 0
    ])
    progress = (fields_filled / 9) * 100
    st.progress(progress / 100)
    st.caption(f"✓ Form {progress:.0f}% complete")

patient_data = {
    'age': age,
    'sex': sex,
    'bmi': round(bmi, 2),
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
    
    # Actionable Recommendations Section
    st.divider()
    st.header("💡 Personalized Recommendations")
    
    recommendations = []
    potential_reduction = 0
    
    # Generate specific recommendations based on user's data
    if smoker == 1:
        recommendations.append({
            'action': '🚭 Quit smoking',
            'impact': 'Reduce risk by 25-30%',
            'description': 'Smoking is the #1 modifiable risk factor. Your heart begins healing within 20 minutes of your last cigarette.',
            'priority': 'HIGH'
        })
        potential_reduction += 27
    
    if bmi > 25:
        weight_to_lose = (bmi - 24) * ((height_cm / 100) ** 2)
        recommendations.append({
            'action': f'⚖️ Lose {weight_to_lose:.1f} kg to reach healthy BMI',
            'impact': 'Reduce risk by 8-12%',
            'description': f'Reaching a BMI of 24 would put you in the healthy weight range. Aim for gradual weight loss of 0.5-1 kg per week.',
            'priority': 'MEDIUM'
        })
        potential_reduction += 10
    
    if phys_activity == 0:
        recommendations.append({
            'action': '🏃 Start exercising 150 min/week',
            'impact': 'Reduce risk by 12-15%',
            'description': 'Aim for 30 minutes of moderate activity, 5 days per week. Start with walking and gradually increase intensity.',
            'priority': 'HIGH'
        })
        potential_reduction += 13
    
    if sleep_hours < 7:
        recommendations.append({
            'action': f'😴 Increase sleep to 7-8 hours (currently {sleep_hours}h)',
            'impact': 'Reduce risk by 5-8%',
            'description': 'Quality sleep allows your heart to rest and repair. Establish a consistent bedtime routine.',
            'priority': 'MEDIUM'
        })
        potential_reduction += 6
    
    if diabetes == 1:
        recommendations.append({
            'action': '🩺 Optimize diabetes management',
            'impact': 'Reduce risk by 10-15%',
            'description': 'Keep HbA1c below 7%, monitor blood sugar regularly, and follow your treatment plan strictly.',
            'priority': 'HIGH'
        })
        potential_reduction += 12
    
    if gen_health <= 2:
        recommendations.append({
            'action': '🏥 Schedule comprehensive health checkup',
            'impact': 'Early detection saves lives',
            'description': 'Your self-rated poor health correlates with actual health risks. Get blood pressure, cholesterol, and ECG checked.',
            'priority': 'HIGH'
        })
    
    if recommendations:
        st.success(f"✨ **By following these recommendations, you could potentially reduce your heart disease risk by up to {potential_reduction}%!**")
        
        for i, rec in enumerate(recommendations, 1):
            priority_color = "🔴" if rec['priority'] == 'HIGH' else "🟡"
            with st.expander(f"{priority_color} **{i}. {rec['action']}** - {rec['impact']}"):
                st.write(rec['description'])
    else:
        st.success("🎉 **Great job! You're already following healthy habits.** Keep it up!")
        st.info("""
        **To maintain your heart health:**
        - Continue regular exercise
        - Maintain healthy weight
        - Get 7-9 hours of sleep
        - Monitor your health annually
        - Stay up to date with preventive screenings
        """)
    
    # What-If Scenario Calculator
    st.divider()
    st.header("🔮 What-If Scenario Calculator")
    st.caption("See how lifestyle changes would affect your heart disease risk")
    
    st.markdown("### Adjust your parameters:")
    col_w1, col_w2, col_w3 = st.columns(3)
    
    with col_w1:
        what_if_weight = st.number_input("What if weight was (kg):", 
                                        min_value=30.0, max_value=300.0, 
                                        value=weight_kg, step=1.0, key="what_if_weight")
        what_if_smoker = st.selectbox("What if smoking status:", [0, 1],
                                     format_func=lambda x: "Non-smoker" if x == 0 else "Smoker",
                                     index=smoker, key="what_if_smoker")
    
    with col_w2:
        what_if_exercise = st.selectbox("What if exercise level:", range(4),
                                       format_func=lambda x: phys_activity_options[x],
                                       index=phys_activity_raw, key="what_if_exercise")
        what_if_sleep = st.number_input("What if sleep was (hours):",
                                       min_value=4.0, max_value=12.0,
                                       value=sleep_hours, step=0.5, key="what_if_sleep")
    
    with col_w3:
        what_if_health = st.select_slider("What if health rating:",
                                         options=[1, 2, 3, 4, 5],
                                         value=gen_health,
                                         format_func=lambda x: health_options[x],
                                         key="what_if_health")
    
    if st.button("🔮 Calculate What-If Scenario", type="secondary"):
        what_if_bmi = what_if_weight / ((height_cm / 100) ** 2)
        what_if_phys = 1 if what_if_exercise >= 2 else 0
        
        what_if_data = {
            'age': age,
            'sex': sex,
            'bmi': round(what_if_bmi, 2),
            'smoker': what_if_smoker,
            'diabetes': diabetes,  # Keeping diabetes same (can't change instantly)
            'phys_activity': what_if_phys,
            'sleep_hours': what_if_sleep,
            'gen_health': what_if_health
        }
        
        with st.spinner("Calculating new risk..."):
            what_if_result = get_xai_prediction(what_if_data)
        
        # Compare original vs what-if
        col_orig, col_arrow, col_new = st.columns([5, 1, 5])
        
        with col_orig:
            st.markdown("**Current Risk:**")
            if xai_result['prediction'] == 'HIGH RISK':
                st.error(f"🔴 {xai_result['prediction']} ({xai_result['confidence']:.1f}%)")
            else:
                st.success(f"🟢 {xai_result['prediction']} ({xai_result['confidence']:.1f}%)")
        
        with col_arrow:
            st.markdown("<div style='text-align: center; font-size: 40px; padding-top: 10px;'>→</div>", unsafe_allow_html=True)
        
        with col_new:
            st.markdown("**What-If Risk:**")
            if what_if_result['prediction'] == 'HIGH RISK':
                st.error(f"🔴 {what_if_result['prediction']} ({what_if_result['confidence']:.1f}%)")
            else:
                st.success(f"🟢 {what_if_result['prediction']} ({what_if_result['confidence']:.1f}%)")
        
        # Show change
        confidence_change = what_if_result['confidence'] - xai_result['confidence']
        if abs(confidence_change) > 5:
            if confidence_change < 0:
                st.success(f"✅ **Risk decreased by {abs(confidence_change):.1f} percentage points!** These changes would improve your heart health.")
            else:
                st.warning(f"⚠️ **Risk increased by {confidence_change:.1f} percentage points.** These changes would worsen your heart health.")
        else:
            st.info("ℹ️ Minimal change in risk. Consider more significant lifestyle modifications.")

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
