# app/streamlit_app.py
import os
import requests
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

API_URL = os.environ.get('API_URL', 'http://localhost:8000')

st.set_page_config(
    page_title='Heart Risk Assessment | XAI Chatbot', 
    page_icon='❤️', 
    layout='wide',
    initial_sidebar_state='expanded'
)

# Enhanced Custom CSS with DARK THEME and WHITE TEXT
st.markdown("""
<style>
    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        background-attachment: fixed;
        color: white !important;
    }
    
    /* Main content area with dark glass effect */
    .main .block-container {
        background: rgba(26, 26, 46, 0.85);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white !important;
    }
    
    /* All text white */
    .stApp, .stApp * {
        color: white !important;
    }
    
    /* Override Streamlit default text colors */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: white !important;
    }
    
    /* Input labels and text */
    .stTextInput label, .stSelectbox label, .stNumberInput label {
        color: white !important;
        font-weight: 600;
    }
    
    /* Input fields with dark background and white text */
    .stTextInput input, .stSelectbox select, .stNumberInput input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Chat messages with dark theme */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        color: white !important;
    }
    
    /* Chat input */
    .stChatInputContainer input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Enhanced risk cards with animations - WHITE TEXT */
    .risk-high {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 30px;
        border-radius: 20px;
        color: white !important;
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(245, 87, 108, 0.6);
        animation: pulse 2s infinite;
    }
    
    .risk-high * {
        color: white !important;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 30px;
        border-radius: 20px;
        color: white !important;
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(79, 172, 254, 0.6);
        animation: pulse 2s infinite;
    }
    
    .risk-low * {
        color: white !important;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Beautiful explanation boxes - DARK THEME */
    .explanation-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin: 15px 0;
        border-left: 5px solid #667eea;
        color: white !important;
    }
    
    .explanation-box * {
        color: white !important;
    }
    
    /* Info cards - DARK THEME */
    .info-card {
        background: rgba(102, 126, 234, 0.3);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        color: white !important;
        font-weight: 500;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .info-card * {
        color: white !important;
    }
    
    /* Progress indicator - WHITE TEXT */
    .progress-text {
        font-size: 1.2rem;
        color: #4facfe !important;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
    }
    
    /* Button styling - WHITE TEXT */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
        color: white !important;
        background: rgba(102, 126, 234, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.5);
        background: rgba(102, 126, 234, 0.8);
    }
    
    /* Input validation styling - DARK THEME */
    .validation-error {
        background: rgba(255, 193, 7, 0.2);
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: #ffd54f !important;
    }
    
    .validation-error * {
        color: #ffd54f !important;
    }
    
    .validation-success {
        background: rgba(76, 175, 80, 0.2);
        border-left: 4px solid #4caf50;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: #81c784 !important;
    }
    
    .validation-success * {
        color: #81c784 !important;
    }
    
    /* Sidebar styling - DARK */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Enhanced metrics - WHITE TEXT */
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4facfe !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600;
    }
    
    /* Expander styling - WHITE TEXT */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }
    
    /* Tab styling - WHITE TEXT */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: white !important;
        border-bottom-color: #4facfe !important;
    }
    
    /* Success/Error/Warning boxes - WHITE TEXT */
    .stSuccess, .stError, .stWarning, .stInfo {
        color: white !important;
    }
    
    .stSuccess *, .stError *, .stWarning *, .stInfo * {
        color: white !important;
    }
    
    /* Caption text */
    .stCaption {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    /* Radio buttons */
    .stRadio label {
        color: white !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #4facfe !important;
    }
</style>
""", unsafe_allow_html=True)

# Header with branding
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.markdown("# ⚕️")
with col_title:
    st.title('PANACEA XAI')
    st.markdown('🧠 **Powered by Explainable AI**')

st.markdown('---')

# Initialize session state
if 'payload' not in st.session_state:
    st.session_state.payload = {}
if 'validation_errors' not in st.session_state:
    st.session_state.validation_errors = {}
if 'mode' not in st.session_state:
    st.session_state.mode = 'form'  # 'form' or 'chat'
if 'show_tips' not in st.session_state:
    st.session_state.show_tips = True
if 'unit_system' not in st.session_state:
    st.session_state.unit_system = 'metric'  # 'metric' or 'imperial'
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# Sidebar controls
with st.sidebar:
    st.markdown("## 🎛️ Control Panel")
    
    # Mode selector
    mode = st.radio(
        "📝 Input Mode",
        ['Interactive Form', 'Chat Interface'],
        help="Choose how you want to enter patient data"
    )
    st.session_state.mode = 'form' if mode == 'Interactive Form' else 'chat'
    
    st.markdown("---")
    
    # Unit system toggle
    st.markdown("### ⚖️ Unit System")
    unit_system = st.radio(
        "Measurement Units",
        ['Metric (kg, cm)', 'Imperial (lbs, ft/in)'],
        horizontal=True,
        help="Choose your preferred measurement system"
    )
    st.session_state.unit_system = 'metric' if 'Metric' in unit_system else 'imperial'
    
    st.markdown("---")
    
    # Quick sample profiles
    st.markdown("### 👥 Sample Profiles")
    sample_profiles = {
        '🏃 Healthy Adult': {'age': 45, 'sex': 1, 'bmi': 23.5, 'smoker': 0, 'diabetes': 0, 'phys_activity': 1, 'sleep_hours': 8, 'gen_health': 4},
        '⚠️ High Risk': {'age': 68, 'sex': 1, 'bmi': 32.5, 'smoker': 1, 'diabetes': 1, 'phys_activity': 0, 'sleep_hours': 5, 'gen_health': 2},
        '💪 Athletic': {'age': 30, 'sex': 0, 'bmi': 21.0, 'smoker': 0, 'diabetes': 0, 'phys_activity': 1, 'sleep_hours': 8, 'gen_health': 5},
        '🩺 Pre-diabetic': {'age': 55, 'sex': 0, 'bmi': 27.5, 'smoker': 0, 'diabetes': 1, 'phys_activity': 0, 'sleep_hours': 6, 'gen_health': 3}
    }
    
    selected_profile = st.selectbox(
        'Quick Fill',
        ['Select a profile...'] + list(sample_profiles.keys()),
        help="Load pre-configured patient profiles for quick testing"
    )
    
    if selected_profile != 'Select a profile...' and st.button('Load Profile', use_container_width=True):
        st.session_state.payload = sample_profiles[selected_profile].copy()
        st.success(f"✅ Loaded: {selected_profile}")
        st.rerun()
    
    st.markdown("---")
    
    # Quick actions
    col_action1, col_action2 = st.columns(2)
    with col_action1:
        if st.button('🔄 Reset', use_container_width=True):
            st.session_state.payload = {}
            st.session_state.validation_errors = {}
            st.rerun()
    
    with col_action2:
        if st.button('� Random', use_container_width=True):
            import random
            st.session_state.payload = {
                'age': random.randint(25, 80),
                'sex': random.randint(0, 1),
                'bmi': round(random.uniform(18.5, 35), 1),
                'smoker': random.randint(0, 1),
                'diabetes': random.randint(0, 1),
                'phys_activity': random.randint(0, 1),
                'sleep_hours': random.randint(5, 9),
                'gen_health': random.randint(1, 5)
            }
            st.rerun()
    
    st.markdown("---")
    
    # Progress indicator with detailed stats
    progress = len(st.session_state.payload) / 8
    st.progress(progress)
    st.caption(f"📊 Progress: {len(st.session_state.payload)}/8 fields completed")
    
    if progress == 1.0:
        st.success("✨ All fields complete! Ready to analyze")
    elif progress > 0:
        remaining = 8 - len(st.session_state.payload)
        st.info(f"📝 {remaining} field{'s' if remaining > 1 else ''} remaining")
    
    st.markdown("---")
    
    # Settings
    st.markdown("### ⚙️ Settings")
    st.session_state.show_tips = st.checkbox("Show Health Tips", value=st.session_state.show_tips, help="Display educational tips throughout the form")
    
    # Prediction history
    if st.session_state.prediction_history:
        st.markdown("---")
        st.markdown("### 📜 Recent Assessments")
        st.caption(f"{len(st.session_state.prediction_history)} prediction(s) in history")
        if st.button('🗑️ Clear History', use_container_width=True):
            st.session_state.prediction_history = []
            st.rerun()
    
    st.markdown("---")

# Validation functions
def validate_age(value):
    try:
        age = float(value)
        if age < 18 or age > 120:
            return False, "⚠️ Age must be between 18 and 120 years"
        return True, "✓ Valid age"
    except:
        return False, "⚠️ Please enter a valid number"

def validate_sex(value):
    try:
        sex = int(value)
        if sex not in [0, 1]:
            return False, "⚠️ Please enter 0 (female) or 1 (male)"
        return True, f"✓ {'Male' if sex == 1 else 'Female'}"
    except:
        return False, "⚠️ Please enter 0 or 1"

def validate_bmi(value):
    try:
        bmi = float(value)
        if bmi < 10 or bmi > 60:
            return False, "⚠️ BMI must be between 10 and 60"
        if bmi < 18.5:
            return True, "✓ Valid BMI (Underweight)"
        elif bmi < 25:
            return True, "✓ Valid BMI (Normal)"
        elif bmi < 30:
            return True, "✓ Valid BMI (Overweight)"
        else:
            return True, "✓ Valid BMI (Obese)"
    except:
        return False, "⚠️ Please enter a valid number (e.g., 27.5)"

def validate_binary(value, field_name):
    try:
        val = int(value)
        if val not in [0, 1]:
            return False, f"⚠️ Please enter 0 (No) or 1 (Yes)"
        return True, f"✓ {'Yes' if val == 1 else 'No'}"
    except:
        return False, "⚠️ Please enter 0 or 1"

def validate_sleep(value):
    try:
        hours = float(value)
        if hours < 0 or hours > 24:
            return False, "⚠️ Sleep hours must be between 0 and 24"
        if hours < 6:
            return True, "✓ Valid (Low sleep)"
        elif hours <= 9:
            return True, "✓ Valid (Healthy sleep)"
        else:
            return True, "✓ Valid (High sleep)"
    except:
        return False, "⚠️ Please enter a valid number"

def validate_health(value):
    try:
        health = int(value)
        if health < 1 or health > 5:
            return False, "⚠️ Health rating must be between 1 and 5"
        labels = {1: "Poor", 2: "Fair", 3: "Good", 4: "Very Good", 5: "Excellent"}
        return True, f"✓ {labels[health]}"
    except:
        return False, "⚠️ Please enter a number between 1 and 5"

VALIDATORS = {
    'age': validate_age,
    'sex': validate_sex,
    'bmi': validate_bmi,
    'smoker': lambda v: validate_binary(v, 'smoker'),
    'diabetes': lambda v: validate_binary(v, 'diabetes'),
    'phys_activity': lambda v: validate_binary(v, 'phys_activity'),
    'sleep_hours': validate_sleep,
    'gen_health': validate_health
}

# Field definitions with enhanced descriptions
FIELD_INFO = {
    'age': {
        'label': '👤 Age',
        'question': 'What is your age?',
        'help': 'Enter age in years (18-120)',
        'example': 'e.g., 45',
        'icon': '🎂'
    },
    'sex': {
        'label': '⚧ Biological Sex',
        'question': 'What is your biological sex?',
        'help': 'Enter 0 for Female, 1 for Male',
        'example': '0 = Female, 1 = Male',
        'icon': '👥'
    },
    'bmi': {
        'label': '⚖️ Body Mass Index (BMI)',
        'question': 'What is your BMI?',
        'help': 'BMI = weight(kg) / height(m)². Normal: 18.5-24.9',
        'example': 'e.g., 27.5',
        'icon': '📊'
    },
    'smoker': {
        'label': '🚬 Smoking Status',
        'question': 'Do you currently smoke?',
        'help': '0 = No, 1 = Yes',
        'example': '0 or 1',
        'icon': '🚭'
    },
    'diabetes': {
        'label': '💉 Diabetes Status',
        'question': 'Do you have diabetes?',
        'help': '0 = No, 1 = Yes (Type 1 or Type 2)',
        'example': '0 or 1',
        'icon': '🩺'
    },
    'phys_activity': {
        'label': '🏃 Physical Activity',
        'question': 'Any physical activity in the past 30 days?',
        'help': '0 = No, 1 = Yes (any exercise, sports, or recreation)',
        'example': '0 or 1',
        'icon': '⚡'
    },
    'sleep_hours': {
        'label': '😴 Sleep Duration',
        'question': 'Average sleep hours per night?',
        'help': 'Recommended: 7-9 hours for adults',
        'example': 'e.g., 7',
        'icon': '🌙'
    },
    'gen_health': {
        'label': '❤️ General Health',
        'question': 'How would you rate your general health?',
        'help': '1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent',
        'example': 'Rate from 1 to 5',
        'icon': '🏥'
    }
}

FIELD_ORDER = ['age', 'sex', 'bmi', 'smoker', 'diabetes', 'phys_activity', 'sleep_hours', 'gen_health']

# ============================================================================
# INTERACTIVE FORM MODE
# ============================================================================
if st.session_state.mode == 'form':
    # Interactive header with animation
    st.markdown("## 📋 Patient Information Form")
    st.markdown("Please fill in all fields below. Real-time validation will help ensure accuracy.")
    
    # Show health tips banner if enabled
    if st.session_state.show_tips:
        with st.expander("💡 Quick Health Tips", expanded=False):
            tip_cols = st.columns(3)
            with tip_cols[0]:
                st.markdown("### 🏃 Stay Active")
                st.caption("150 min/week of moderate exercise reduces heart disease risk by 30-40%")
            with tip_cols[1]:
                st.markdown("### 🚭 Don't Smoke")
                st.caption("Quitting smoking can reduce heart disease risk by 50% within 1 year")
            with tip_cols[2]:
                st.markdown("### 🥗 Eat Well")
                st.caption("Mediterranean diet can reduce cardiovascular events by 30%")
    
    # BMI Calculator (outside form)
    with st.expander("🧮 BMI Calculator - Calculate Before Filling Form", expanded=False):
        calc_col1, calc_col2, calc_col3 = st.columns(3)
        with calc_col1:
            if st.session_state.unit_system == 'metric':
                height_input = st.number_input("Height (cm)", min_value=100, max_value=250, value=170, key="calc_height")
                weight_input = st.number_input("Weight (kg)", min_value=30, max_value=300, value=70, key="calc_weight")
            else:
                height_ft = st.number_input("Height (feet)", min_value=4, max_value=8, value=5, key="calc_height_ft")
                height_in = st.number_input("Height (inches)", min_value=0, max_value=11, value=8, key="calc_height_in")
                weight_input = st.number_input("Weight (lbs)", min_value=70, max_value=600, value=154, key="calc_weight_lbs")
        
        with calc_col2:
            st.markdown("### ")  # Spacing
            if st.button("Calculate BMI", key="calc_bmi_btn", use_container_width=True):
                if st.session_state.unit_system == 'metric':
                    calculated_bmi = weight_input / ((height_input / 100) ** 2)
                else:
                    height_total_in = (height_ft * 12) + height_in
                    calculated_bmi = (weight_input * 703) / (height_total_in ** 2)
                
                st.session_state['calculated_bmi'] = round(calculated_bmi, 1)
        
        with calc_col3:
            if 'calculated_bmi' in st.session_state:
                st.markdown("### Your BMI")
                st.success(f"**{st.session_state['calculated_bmi']}**")
                
                # BMI category
                bmi_val = st.session_state['calculated_bmi']
                if bmi_val < 18.5:
                    st.caption("🔵 Underweight")
                elif bmi_val < 25:
                    st.caption("🟢 Normal weight")
                elif bmi_val < 30:
                    st.caption("🟡 Overweight")
                else:
                    st.caption("🔴 Obese")
    
    with st.form("patient_form", clear_on_submit=False):
        form_cols = st.columns(2)
        
        for idx, field_key in enumerate(FIELD_ORDER):
            info = FIELD_INFO[field_key]
            col = form_cols[idx % 2]
            
            with col:
                st.markdown(f"### {info['icon']} {info['label']}")
                
                current_value = st.session_state.payload.get(field_key, '')
                
                # Use calculated BMI if available
                if field_key == 'bmi' and 'calculated_bmi' in st.session_state and current_value == '':
                    current_value = st.session_state['calculated_bmi']
                
                # Input field with help text
                if field_key in ['age', 'bmi', 'sleep_hours']:
                    user_input = st.text_input(
                        info['question'],
                        value=str(current_value) if current_value != '' else '',
                        help=info['help'],
                        placeholder=info['example'],
                        key=f"form_{field_key}"
                    )
                elif field_key == 'sex':
                    user_input = st.selectbox(
                        info['question'],
                        options=['', '0', '1'],
                        index=0 if current_value == '' else (1 if str(current_value) == '0' else 2),
                        format_func=lambda x: 'Select...' if x == '' else ('Female' if x == '0' else 'Male'),
                        help=info['help'],
                        key=f"form_{field_key}"
                    )
                elif field_key in ['smoker', 'diabetes', 'phys_activity']:
                    user_input = st.selectbox(
                        info['question'],
                        options=['', '0', '1'],
                        index=0 if current_value == '' else (1 if str(current_value) == '0' else 2),
                        format_func=lambda x: 'Select...' if x == '' else ('No' if x == '0' else 'Yes'),
                        help=info['help'],
                        key=f"form_{field_key}"
                    )
                else:  # gen_health
                    user_input = st.selectbox(
                        info['question'],
                        options=['', '1', '2', '3', '4', '5'],
                        index=0 if current_value == '' else int(current_value),
                        format_func=lambda x: {
                            '': 'Select...',
                            '1': '1 - Poor',
                            '2': '2 - Fair',
                            '3': '3 - Good',
                            '4': '4 - Very Good',
                            '5': '5 - Excellent'
                        }.get(x, x),
                        help=info['help'],
                        key=f"form_{field_key}"
                    )
                
                # Show validation status if field has value
                if user_input and user_input != '':
                    validator = VALIDATORS[field_key]
                    is_valid, message = validator(user_input)
                    
                    if is_valid:
                        st.markdown(f'<div class="validation-success">{message}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="validation-error">{message}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        submit_col1, submit_col2, submit_col3 = st.columns([1, 1, 1])
        
        with submit_col2:
            submitted = st.form_submit_button("🔮 Analyze Risk", use_container_width=True, type="primary")
        
        if submitted:
            # Collect all form values
            temp_payload = {}
            all_valid = True
            validation_messages = []
            
            for field_key in FIELD_ORDER:
                value = st.session_state.get(f"form_{field_key}", '')
                
                if value == '' or value is None:
                    all_valid = False
                    validation_messages.append(f"❌ {FIELD_INFO[field_key]['label']}: Missing value")
                else:
                    validator = VALIDATORS[field_key]
                    is_valid, message = validator(value)
                    
                    if is_valid:
                        # Convert to appropriate type
                        if field_key in ['age', 'bmi', 'sleep_hours']:
                            temp_payload[field_key] = float(value)
                        else:
                            temp_payload[field_key] = int(value)
                        validation_messages.append(f"✅ {FIELD_INFO[field_key]['label']}: {message}")
                    else:
                        all_valid = False
                        validation_messages.append(f"❌ {FIELD_INFO[field_key]['label']}: {message}")
            
            if all_valid:
                st.session_state.payload = temp_payload
                st.success("✅ All fields validated successfully! Generating analysis...")
                st.rerun()
            else:
                st.error("⚠️ Please correct the following issues:")
                for msg in validation_messages:
                    if '❌' in msg:
                        st.warning(msg)

# ============================================================================
# CHAT INTERFACE MODE
# ============================================================================
elif st.session_state.mode == 'chat':
    st.markdown("## 💬 Conversational Assessment")
    st.markdown('<div class="progress-text">📊 Answer questions one by one</div>', unsafe_allow_html=True)
    
    # Display conversation history
    for field_key in FIELD_ORDER:
        if field_key in st.session_state.payload:
            info = FIELD_INFO[field_key]
            
            # Assistant question
            with st.chat_message('assistant', avatar='🤖'):
                st.markdown(f"**{info['icon']} {info['question']}**")
                st.caption(info['help'])
            
            # User answer
            with st.chat_message('user', avatar='👤'):
                value = st.session_state.payload[field_key]
                validator = VALIDATORS[field_key]
                _, message = validator(value)
                st.markdown(f"**{value}** — {message}")
    
    # Next question
    for field_key in FIELD_ORDER:
        if field_key not in st.session_state.payload:
            info = FIELD_INFO[field_key]
            
            with st.chat_message('assistant', avatar='🤖'):
                st.markdown(f"**{info['icon']} {info['question']}**")
                st.caption(f"{info['help']} | Example: {info['example']}")
            
            user_val = st.chat_input(f'💬 Type your answer for {info["label"]}...', key='chat_input')
            
            if user_val is None:
                st.stop()
            
            # Validate input
            validator = VALIDATORS[field_key]
            is_valid, message = validator(user_val)
            
            if not is_valid:
                with st.chat_message('user', avatar='👤'):
                    st.markdown(f"**{user_val}**")
                
                with st.chat_message('assistant', avatar='🤖'):
                    st.markdown(f'<div class="validation-error">{message}<br/>Please try again.</div>', unsafe_allow_html=True)
                
                st.stop()
            
            # Valid input - save and show
            with st.chat_message('user', avatar='👤'):
                st.markdown(f"**{user_val}** — {message}")
            
            # Convert and save
            if field_key in ['age', 'bmi', 'sleep_hours']:
                st.session_state.payload[field_key] = float(user_val)
            else:
                st.session_state.payload[field_key] = int(user_val)
            
            st.rerun()
            break

# ============================================================================
# PREDICTION AND ANALYSIS
# ============================================================================
payload = st.session_state.payload
if len(payload) == len(FIELD_ORDER):
    st.markdown("---")
    st.markdown("## 🎯 Risk Assessment Results")
    
    # Show input summary in expandable card
    with st.expander('📝 Review Your Information', expanded=False):
        summary_cols = st.columns(2)
        for idx, field_key in enumerate(FIELD_ORDER):
            col = summary_cols[idx % 2]
            info = FIELD_INFO[field_key]
            with col:
                st.metric(
                    label=f"{info['icon']} {info['label']}", 
                    value=payload[field_key]
                )
    
    try:
        with st.spinner('🔮 Computing risk prediction with AI...'):
            resp = requests.post(f'{API_URL}/predict', json={'payload': payload}, timeout=30)
            resp.raise_for_status()
            pred = resp.json()
        
        p = float(pred.get('probability', 0.0))
        risk_percentage = p * 100
        label = 'High Risk ⚠️' if p >= 0.5 else 'Low Risk ✅'
        risk_class = 'risk-high' if p >= 0.5 else 'risk-low'
        
        # Save to prediction history
        prediction_record = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'risk_percentage': risk_percentage,
            'label': label,
            'payload': payload.copy()
        }
        st.session_state.prediction_history.append(prediction_record)
        
        # Keep only last 10 predictions
        if len(st.session_state.prediction_history) > 10:
            st.session_state.prediction_history = st.session_state.prediction_history[-10:]
        
        # Animated prediction card with detailed interpretation
        st.markdown(f'<div class="{risk_class}">🩺 Prediction: {label}<br/>Risk Probability: {risk_percentage:.1f}%</div>', unsafe_allow_html=True)
        
        # Risk interpretation
        if risk_percentage < 30:
            interpretation = "🟢 **Low Risk**: The model indicates a low probability of heart disease. Continue maintaining healthy lifestyle habits."
            color_theme = "success"
        elif risk_percentage < 50:
            interpretation = "🟡 **Moderate-Low Risk**: Some risk factors present. Consider discussing prevention strategies with your healthcare provider."
            color_theme = "warning"
        elif risk_percentage < 70:
            interpretation = "🟠 **Moderate-High Risk**: Notable risk factors detected. Medical consultation recommended for risk assessment and prevention."
            color_theme = "warning"
        else:
            interpretation = "🔴 **High Risk**: Multiple significant risk factors present. Please consult a healthcare professional for comprehensive evaluation."
            color_theme = "error"
        
        st.markdown(f'<div class="info-card">{interpretation}</div>', unsafe_allow_html=True)
        
        # Interactive risk factors breakdown
        st.markdown("### 🔍 Your Risk Factors Breakdown")
        risk_factors_identified = []
        
        # Analyze each factor
        if payload['age'] > 60:
            risk_factors_identified.append(('🎂 Age', f"{payload['age']} years", "Age >60 significantly increases risk", "red"))
        elif payload['age'] > 45:
            risk_factors_identified.append(('🎂 Age', f"{payload['age']} years", "Age >45 moderately increases risk", "orange"))
        else:
            risk_factors_identified.append(('🎂 Age', f"{payload['age']} years", "Age is a protective factor", "green"))
        
        if payload['bmi'] >= 30:
            risk_factors_identified.append(('⚖️ BMI', f"{payload['bmi']}", "Obese range (≥30) - high risk", "red"))
        elif payload['bmi'] >= 25:
            risk_factors_identified.append(('⚖️ BMI', f"{payload['bmi']}", "Overweight range (25-30) - moderate risk", "orange"))
        else:
            risk_factors_identified.append(('⚖️ BMI', f"{payload['bmi']}", "Healthy weight range", "green"))
        
        if payload['smoker'] == 1:
            risk_factors_identified.append(('🚬 Smoking', "Yes", "Smoking increases risk by 2-4x", "red"))
        else:
            risk_factors_identified.append(('🚭 Smoking', "No", "Non-smoker - protective factor", "green"))
        
        if payload['diabetes'] == 1:
            risk_factors_identified.append(('💉 Diabetes', "Yes", "Diabetes doubles heart disease risk", "red"))
        else:
            risk_factors_identified.append(('💉 Diabetes', "No", "No diabetes - protective", "green"))
        
        if payload['phys_activity'] == 0:
            risk_factors_identified.append(('🏃 Exercise', "No", "Sedentary lifestyle increases risk", "red"))
        else:
            risk_factors_identified.append(('⚡ Exercise', "Yes", "Physical activity reduces risk", "green"))
        
        if payload['sleep_hours'] < 6:
            risk_factors_identified.append(('😴 Sleep', f"{payload['sleep_hours']}h", "Insufficient sleep (<6h) increases risk", "red"))
        elif payload['sleep_hours'] > 9:
            risk_factors_identified.append(('😴 Sleep', f"{payload['sleep_hours']}h", "Excessive sleep (>9h) may indicate issues", "orange"))
        else:
            risk_factors_identified.append(('😴 Sleep', f"{payload['sleep_hours']}h", "Healthy sleep duration (7-9h)", "green"))
        
        if payload['gen_health'] <= 2:
            risk_factors_identified.append(('❤️ Health', "Poor/Fair", "Self-rated poor health correlates with risk", "red"))
        elif payload['gen_health'] == 3:
            risk_factors_identified.append(('❤️ Health', "Good", "Average health rating", "orange"))
        else:
            risk_factors_identified.append(('❤️ Health', "Very Good/Excellent", "Good self-rated health", "green"))
        
        # Display in colored columns
        factor_cols = st.columns(4)
        for i, (icon_label, value, explanation, color) in enumerate(risk_factors_identified):
            with factor_cols[i % 4]:
                if color == "red":
                    st.error(f"**{icon_label}**\n\n{value}")
                    st.caption(explanation)
                elif color == "orange":
                    st.warning(f"**{icon_label}**\n\n{value}")
                    st.caption(explanation)
                else:
                    st.success(f"**{icon_label}**\n\n{value}")
                    st.caption(explanation)
        
        # Enhanced probability gauge with better visuals
        st.markdown("---")
        col_gauge, col_metrics = st.columns([2, 1])
        
        with col_gauge:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=risk_percentage,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Heart Disease Risk Score", 'font': {'size': 26, 'color': '#2c3e50'}},
                number={'suffix': "%", 'font': {'size': 50}},
                delta={
                    'reference': 50, 
                    'increasing': {'color': "#e74c3c"}, 
                    'decreasing': {'color': "#27ae60"},
                    'suffix': "%"
                },
                gauge={
                    'axis': {
                        'range': [None, 100], 
                        'tickwidth': 2, 
                        'tickcolor': "#34495e",
                        'tickmode': 'linear',
                        'tick0': 0,
                        'dtick': 10
                    },
                    'bar': {'color': "#e74c3c" if p >= 0.5 else "#27ae60", 'thickness': 0.75},
                    'bgcolor': "white",
                    'borderwidth': 3,
                    'bordercolor': "#34495e",
                    'steps': [
                        {'range': [0, 30], 'color': '#d4edda'},
                        {'range': [30, 50], 'color': '#fff3cd'},
                        {'range': [50, 70], 'color': '#ffc107'},
                        {'range': [70, 100], 'color': '#f8d7da'}
                    ],
                    'threshold': {
                        'line': {'color': "#c0392b", 'width': 4},
                        'thickness': 0.8,
                        'value': 50
                    }
                }
            ))
            fig_gauge.update_layout(
                height=400, 
                margin=dict(l=20, r=20, t=80, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                font={'family': 'Arial, sans-serif'}
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col_metrics:
            st.markdown("### 📊 Quick Stats")
            
            # Risk level indicator
            if risk_percentage < 30:
                st.success("🟢 Low Risk")
            elif risk_percentage < 50:
                st.warning("🟡 Moderate Low")
            elif risk_percentage < 70:
                st.warning("🟠 Moderate High")
            else:
                st.error("🔴 High Risk")
            
            st.metric("Confidence", f"{pred.get('probability', 0):.1%}")
            st.metric("Threshold", "50%")
            st.metric("Model", "Random Forest")
            
            # Timestamp
            st.caption(f"⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except requests.exceptions.Timeout:
        st.error('⏱️ Request timed out. The server might be busy. Please try again.')
        st.stop()
    except requests.exceptions.ConnectionError:
        st.error(f'❌ Cannot connect to API at {API_URL}. Please ensure the backend server is running.')
        st.info('💡 **Tip**: Start the API with: `uvicorn api.api:app --host 0.0.0.0 --port 8000`')
        st.stop()
    except Exception as e:
        st.error(f'❌ Prediction failed: {str(e)}')
        st.stop()

    # ============================================================================
    # EXPLAINABLE AI SECTION
    # ============================================================================
    st.markdown("---")
    st.markdown("## 🔬 AI Explanation")
    
    try:
        with st.spinner('🧠 Generating AI explanations with SHAP & LIME... This may take 30-60 seconds.'):
            resp = requests.post(f'{API_URL}/explain', json={'payload': payload}, timeout=120)
            resp.raise_for_status()
            exp = resp.json()
    except requests.exceptions.Timeout:
        exp = {'shap': None, 'lime': None, 'shap_error': 'Timeout - explanation took too long', 'lime_error': 'Timeout'}
        st.warning('⏱️ Explanation generation timed out. Try again or continue without detailed explanations.')
    except requests.exceptions.ConnectionError as e:
        exp = {'shap': None, 'lime': None, 'shap_error': f'Connection error: {str(e)}', 'lime_error': 'Connection error'}
        st.error('❌ Cannot connect to explanation service.')
    except Exception as e:
        exp = {'shap': None, 'lime': None, 'shap_error': str(e), 'lime_error': str(e)}
        st.error(f'❌ Error generating explanations: {str(e)}')

    # Explanation tabs
    tab1, tab2 = st.tabs(['📊 SHAP Analysis', '🧩 LIME Analysis'])
    
    with tab1:
        st.markdown('<div class="explanation-box">', unsafe_allow_html=True)
        
        if exp.get('shap'):
            df_shap = pd.DataFrame(exp['shap'])
            df_shap = df_shap.sort_values('contribution', key=abs, ascending=False)
            
            # Enhanced SHAP visualization
            fig_shap = px.bar(
                df_shap.head(10), 
                x='contribution', 
                y='feature',
                orientation='h',
                color='contribution',
                color_continuous_scale='RdBu_r',
                labels={'contribution': 'SHAP Value (Impact on Risk)', 'feature': 'Patient Feature'},
                title='🎯 Feature Importance - SHAP Values',
                text='contribution'
            )
            fig_shap.update_traces(texttemplate='%{text:.3f}', textposition='outside')
            fig_shap.update_layout(
                height=500, 
                showlegend=False,
                xaxis_title="Impact on Prediction",
                yaxis_title="",
                font=dict(size=12),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_shap, use_container_width=True)
            
            # Feature interpretation
            st.markdown("#### 💡 Key Insights:")
            top_features = df_shap.head(3)
            for idx, row in top_features.iterrows():
                impact = "increases" if row['contribution'] > 0 else "decreases"
                emoji = "🔴" if row['contribution'] > 0 else "🟢"
                st.markdown(f"{emoji} **{row['feature']}** {impact} risk by **{abs(row['contribution']):.3f}**")
            
            with st.expander('📋 View Complete SHAP Data'):
                st.dataframe(df_shap, use_container_width=True, height=300)
        else:
            st.warning(f'⚠️ SHAP analysis not available: {exp.get("shap_error", "Unknown error")}')
            st.info('💡 SHAP explanations provide the most accurate feature importance. If unavailable, check API logs.')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="explanation-box">', unsafe_allow_html=True)
        st.markdown("### What is LIME?")
        st.info("""
        **LIME (Local Interpretable Model-agnostic Explanations)** explains individual predictions.
        - Creates a simple model around this specific prediction
        - Shows which features were most important for THIS patient
        - Green = reduces risk, Red = increases risk
        """)
        
        if exp.get('lime'):
            df_lime = pd.DataFrame(exp['lime'])
            df_lime = df_lime.sort_values('weight', key=abs, ascending=False)
            
            # Enhanced LIME visualization
            fig_lime = px.bar(
                df_lime.head(10),
                x='weight',
                y='feature',
                orientation='h',
                color='weight',
                color_continuous_scale='RdYlGn_r',
                labels={'weight': 'LIME Weight (Feature Importance)', 'feature': 'Patient Feature'},
                title='🎯 Local Feature Importance - LIME Weights',
                text='weight'
            )
            fig_lime.update_traces(texttemplate='%{text:.3f}', textposition='outside')
            fig_lime.update_layout(
                height=500, 
                showlegend=False,
                xaxis_title="Feature Weight",
                yaxis_title="",
                font=dict(size=12),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_lime, use_container_width=True)
            
            # Feature interpretation
            st.markdown("#### 💡 Key Insights:")
            top_features = df_lime.head(3)
            for idx, row in top_features.iterrows():
                impact = "increases" if row['weight'] > 0 else "decreases"
                emoji = "🔴" if row['weight'] > 0 else "🟢"
                st.markdown(f"{emoji} **{row['feature']}** {impact} risk (weight: **{abs(row['weight']):.3f}**)")
            
            with st.expander('📋 View Complete LIME Data'):
                st.dataframe(df_lime, use_container_width=True, height=300)
        else:
            st.warning(f'⚠️ LIME analysis not available: {exp.get("lime_error", "Unknown error")}')
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================================================
    # ACTION RECOMMENDATIONS
    # ============================================================================
    st.markdown("---")
    st.markdown("## 🎯 Recommendations")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 👨‍⚕️ Medical Actions:")
        if risk_percentage >= 70:
            st.markdown("""
            - 🏥 **Schedule comprehensive cardiac evaluation**
            - 📋 Get cholesterol and blood pressure tested
            - 💊 Discuss medication options
            - 🔄 Plan regular follow-ups
            """)
        elif risk_percentage >= 50:
            st.markdown("""
            - 📅 **Consult with primary care physician**
            - 🩺 Get routine cardiac screening
            - 📊 Monitor key health metrics
            - 🔍 Evaluate modifiable risk factors
            """)
        else:
            st.markdown("""
            - ✅ **Continue current health practices**
            - 🔄 Annual wellness checkups
            - 📊 Monitor health trends
            - 🎯 Focus on prevention
            """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with rec_col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🏃 Lifestyle Tips:")
        st.markdown("""
        - 🥗 Heart-healthy diet
        - 💪 Regular exercise
        - 😴 Quality sleep (7-9 hrs)
        - 🧘 Stress management
        - 🚭 Avoid smoking
        - 🍷 Moderate alcohol
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================================================
    # PREDICTION HISTORY & COMPARISON
    # ============================================================================
    if len(st.session_state.prediction_history) > 1:
        st.markdown("---")
        st.markdown("## 📊 Prediction History & Comparison")
        
        # Timeline visualization
        history_df = pd.DataFrame(st.session_state.prediction_history)
        
        fig_timeline = go.Figure()
        
        # Add risk percentage line
        fig_timeline.add_trace(go.Scatter(
            x=list(range(len(history_df))),
            y=history_df['risk_percentage'],
            mode='lines+markers+text',
            name='Risk %',
            line=dict(color='#667eea', width=3),
            marker=dict(size=12, color=history_df['risk_percentage'],
                       colorscale='RdYlGn_r', showscale=True,
                       colorbar=dict(title="Risk %")),
            text=[f"{r:.1f}%" for r in history_df['risk_percentage']],
            textposition='top center',
            hovertemplate='<b>Assessment %{x}</b><br>Risk: %{y:.1f}%<extra></extra>'
        ))
        
        # Add reference line at 50%
        fig_timeline.add_hline(y=50, line_dash="dash", line_color="red", 
                              annotation_text="High Risk Threshold (50%)",
                              annotation_position="right")
        
        fig_timeline.update_layout(
            title='📈 Risk Assessment Timeline',
            xaxis_title='Assessment Number',
            yaxis_title='Risk Percentage (%)',
            height=400,
            showlegend=False,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Comparison table
        with st.expander("📋 View Detailed History", expanded=False):
            comparison_data = []
            for i, record in enumerate(st.session_state.prediction_history):
                comparison_data.append({
                    '#': i + 1,
                    'Time': record['timestamp'],
                    'Risk': f"{record['risk_percentage']:.1f}%",
                    'Label': record['label'],
                    'Age': record['payload']['age'],
                    'BMI': record['payload']['bmi'],
                    'Smoker': '✓' if record['payload']['smoker'] == 1 else '✗',
                    'Diabetes': '✓' if record['payload']['diabetes'] == 1 else '✗',
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
            
            # Show trends
            if len(st.session_state.prediction_history) >= 2:
                latest = st.session_state.prediction_history[-1]['risk_percentage']
                previous = st.session_state.prediction_history[-2]['risk_percentage']
                change = latest - previous
                
                if abs(change) > 5:
                    if change < 0:
                        st.success(f"✅ **Risk decreased by {abs(change):.1f} percentage points** compared to previous assessment!")
                    else:
                        st.error(f"⚠️ **Risk increased by {change:.1f} percentage points** compared to previous assessment.")
                else:
                    st.info("ℹ️ Risk level remained relatively stable compared to previous assessment.")
    
    # ============================================================================
    # DOWNLOAD AND SHARE
    # ============================================================================
    st.markdown("---")
    st.markdown("### 💾 Save Your Results")
    
    download_col1, download_col2, download_col3 = st.columns(3)
    
    with download_col1:
        # Create summary report
        report = f"""
HEART DISEASE RISK ASSESSMENT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

PATIENT INFORMATION:
{'-'*60}
"""
        for field_key in FIELD_ORDER:
            report += f"{FIELD_INFO[field_key]['label']}: {payload[field_key]}\n"
        
        report += f"""
{'='*60}

RISK ASSESSMENT:
{'-'*60}
Risk Level: {label}
Risk Probability: {risk_percentage:.1f}%
Model: Random Forest (400 trees)
Threshold: 50%
"""
        
        st.download_button(
            label="📄 Download Report (TXT)",
            data=report,
            file_name=f"heart_risk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with download_col2:
        # Download input data as CSV
        df_download = pd.DataFrame([payload])
        csv = df_download.to_csv(index=False)
        st.download_button(
            label="📊 Download Data (CSV)",
            data=csv,
            file_name=f"patient_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with download_col3:
        if st.button("🔄 New Assessment", use_container_width=True, type="primary"):
            st.session_state.payload = {}
            st.session_state.validation_errors = {}
            st.rerun()
