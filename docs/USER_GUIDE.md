# 📘 Heart Disease Risk Assessment - User Guide

## Welcome! 👋

This guide will help you get the most out of your Heart Disease Risk Assessment System powered by Explainable AI.

---

## 🚀 Getting Started

### Accessing the Application

1. **Ensure both servers are running:**
   - ✅ API Backend: http://localhost:8000
   - ✅ Streamlit UI: http://localhost:8501

2. **Open your web browser** and navigate to: **http://localhost:8501**

3. **You should see the main interface** with a beautiful gradient background and the heart disease assessment form.

---

## 🎯 Choosing Your Input Method

The application offers **two ways** to enter patient information:

### 📋 Option 1: Interactive Form Mode (Recommended)

**Best for:** Quick assessments, batch testing, users who prefer seeing all fields at once

**How to use:**
1. Look at the sidebar → Select "Interactive Form"
2. Fill in all 8 fields in the form
3. Each field shows:
   - 🎯 Field name with icon
   - ❓ Help text explaining what to enter
   - 💡 Example values
   - ✅ Real-time validation (green = good, yellow = warning)
4. Click the **"🔮 Analyze Risk"** button at the bottom
5. If all fields are valid → Analysis appears!
6. If errors exist → Yellow warnings show what to fix

**Pro Tips:**
- Use dropdown menus for binary fields (easier than typing)
- Green checkmarks mean your input is valid
- Red/yellow warnings tell you exactly what's wrong
- All fields must be valid before submission

---

### 💬 Option 2: Chat Interface Mode

**Best for:** Conversational experience, learning about each field, engaging presentations

**How to use:**
1. Look at the sidebar → Select "Chat Interface"
2. The AI asks one question at a time
3. Type your answer in the chat box at the bottom
4. Press Enter to submit
5. If valid → AI confirms and asks the next question
6. If invalid → AI explains the error and asks you to try again
7. After all 8 questions → Analysis appears!

**Pro Tips:**
- Read the help text shown with each question
- Look at the example values for guidance
- Invalid inputs are rejected immediately with helpful feedback
- Progress bar shows how many questions remain

---

## 📝 Understanding the Input Fields

### 👤 Age
- **What it is:** Your age in years
- **Valid range:** 18 to 120 years
- **Example:** 45
- **Why it matters:** Age is one of the strongest predictors of heart disease risk

### ⚧ Biological Sex
- **What it is:** Biological sex assigned at birth
- **Valid values:** 
  - `0` = Female
  - `1` = Male
- **Why it matters:** Males typically have higher heart disease risk at younger ages

### ⚖️ Body Mass Index (BMI)
- **What it is:** Weight-to-height ratio
- **Valid range:** 10.0 to 60.0
- **Example:** 27.5
- **How to calculate:** BMI = weight(kg) / height(m)²
- **Categories:**
  - < 18.5 = Underweight
  - 18.5-24.9 = Normal
  - 25-29.9 = Overweight
  - ≥ 30 = Obese
- **Why it matters:** Higher BMI correlates with increased cardiovascular risk

### 🚬 Smoking Status
- **What it is:** Current smoking habit
- **Valid values:**
  - `0` = Non-smoker
  - `1` = Current smoker
- **Why it matters:** Smoking is a major risk factor for heart disease

### 💉 Diabetes Status
- **What it is:** Whether you have diabetes (Type 1 or Type 2)
- **Valid values:**
  - `0` = No diabetes
  - `1` = Has diabetes
- **Why it matters:** Diabetes significantly increases heart disease risk

### 🏃 Physical Activity
- **What it is:** Any exercise, sports, or recreation in past 30 days
- **Valid values:**
  - `0` = No physical activity
  - `1` = Yes, some activity
- **Why it matters:** Regular physical activity protects against heart disease

### 😴 Sleep Duration
- **What it is:** Average hours of sleep per night
- **Valid range:** 0 to 24 hours
- **Example:** 7
- **Recommended:** 7-9 hours for adults
- **Categories:**
  - < 6 hours = Low sleep (increased risk)
  - 6-9 hours = Healthy sleep
  - > 9 hours = High sleep (may indicate other issues)
- **Why it matters:** Both too little and too much sleep affect heart health

### ❤️ General Health Rating
- **What it is:** Self-rated overall health status
- **Valid values:** 1 to 5
  - `1` = Poor
  - `2` = Fair
  - `3` = Good
  - `4` = Very Good
  - `5` = Excellent
- **Why it matters:** Self-rated health is surprisingly predictive of actual health outcomes

---

## 🎯 Understanding Your Results

### Risk Score Gauge

The **colorful gauge meter** shows your risk percentage:

- **🟢 Green Zone (0-30%)**: Low Risk
  - Continue healthy lifestyle
  - Annual wellness checkups recommended
  
- **🟡 Yellow Zone (30-50%)**: Moderate-Low Risk
  - Some risk factors present
  - Discuss prevention with your doctor
  
- **🟠 Orange Zone (50-70%)**: Moderate-High Risk
  - Notable risk factors detected
  - Medical consultation recommended
  
- **🔴 Red Zone (70-100%)**: High Risk
  - Multiple significant risk factors
  - Comprehensive medical evaluation needed

### Risk Interpretation Card

Below the gauge, you'll see a **colored card** with:
- 🩺 Clear prediction (High/Low Risk)
- 📊 Exact probability percentage
- 💡 Actionable interpretation
- 📋 Recommendations

---

## 🔬 Explainable AI Analysis

### What is Explainable AI (XAI)?

Traditional "black box" AI makes predictions without explaining **why**. Our system uses **XAI techniques** to show you exactly which factors influenced the prediction.

### Tab 1: 📊 SHAP Analysis

**What is SHAP?**
- Stands for SHapley Additive exPlanations
- Based on game theory from economics
- Shows how each feature contributed to the prediction

**How to read the SHAP chart:**
- **Red bars (positive)** → Feature INCREASES risk
- **Blue bars (negative)** → Feature DECREASES risk
- **Longer bars** → Stronger influence
- **Shorter bars** → Weaker influence

**Example:**
```
age: +0.245          ← Age increases risk significantly
diabetes: +0.189     ← Having diabetes increases risk
phys_activity: -0.156 ← Physical activity reduces risk
```

**Key Insights section** highlights the top 3 most important features.

### Tab 2: 🧩 LIME Analysis

**What is LIME?**
- Stands for Local Interpretable Model-agnostic Explanations
- Explains THIS specific prediction (not the model overall)
- Creates a simple, interpretable model around your data

**How to read the LIME chart:**
- **Red bars** → Feature increases risk for YOU
- **Green bars** → Feature decreases risk for YOU
- **Weight values** show importance

**Difference from SHAP:**
- SHAP = Global explanation (how features generally work)
- LIME = Local explanation (how features work for YOU specifically)

### Tab 3: 📖 Learn More

Educational content about:
- Why XAI matters in healthcare
- Differences between SHAP and LIME
- How to interpret results
- Tips for healthcare providers and patients

---

## 🎯 Next Steps & Recommendations

After seeing your results, the app provides:

### 👨‍⚕️ Medical Actions

Tailored recommendations based on your risk level:
- **High Risk:** Immediate medical consultation, comprehensive tests
- **Moderate Risk:** Doctor visit, routine screening
- **Low Risk:** Maintain habits, annual checkups

### 🏃 Lifestyle Improvements

Practical suggestions for:
- 🥗 Nutrition (heart-healthy diet)
- 💪 Exercise (150+ min/week)
- 😴 Sleep (7-9 hours)
- 🧘 Stress management
- 🚭 Smoking cessation
- 🍷 Alcohol moderation

---

## 💾 Saving Your Results

### 📄 Download Report (TXT)
- Complete text report with all details
- Includes patient info, risk assessment, interpretation
- Timestamped filename
- Can be printed or emailed

### 📊 Download Data (CSV)
- Your input data in spreadsheet format
- Easy to import into Excel or other tools
- Good for tracking multiple assessments over time

### 🔄 Start New Assessment
- Clears all data
- Returns to input mode
- Fresh start for new patient

---

## 🎓 Additional Features

### Sidebar Options

#### 📥 Load Sample Data
- Instantly fills form with example patient data
- Great for testing and demonstrations
- Shows a moderate-high risk scenario

#### 🔄 Start New Assessment
- Quick reset button
- Clears all previous data
- Starts fresh

#### 📊 Progress Indicator
- Shows how many fields completed (X/8)
- Visual progress bar
- Helps you see how much is left

#### ℹ️ About This Tool
- Quick reference information
- Lists key features
- Shows technology stack

### Additional Pages (Sidebar)

#### 📚 Research Summary
- Analysis of the scientific paper this is based on
- Comparison with local model metrics
- Educational content about the research

#### ⚖️ Black Box Comparison
- **Perfect for presentations!**
- Side-by-side comparison of Black Box AI vs XAI
- Interactive demonstrations
- Real-world scenarios showing why XAI matters
- Trust metrics and statistics
- Great for showing stakeholders the value of explainability

---

## 🐛 Common Issues & Solutions

### ❌ "Cannot connect to API"

**Problem:** Frontend can't reach backend server

**Solution:**
1. Check if API is running: http://localhost:8000/health
2. If not, start it:
   ```powershell
   uvicorn api.api:app --host 0.0.0.0 --port 8000
   ```

### ⚠️ "Please correct the following issues"

**Problem:** Some fields have invalid values

**Solution:**
- Look for red warning messages
- Each message tells you exactly what's wrong
- Fix those fields and try again
- Green checkmarks mean the field is valid

### ⏱️ "Explanation generation timed out"

**Problem:** SHAP/LIME taking too long

**Solution:**
- This is normal for complex models
- The **prediction still works!**
- Explanations are bonus information
- You can continue without them

### 🔄 Page won't update

**Problem:** Changes not appearing

**Solution:**
- Refresh your browser (F5)
- Or click "🔄 Start New Assessment" in sidebar
- Check console for any errors

---

## 💡 Pro Tips

### For Clinicians
- ✅ Use Form Mode for efficient data entry
- ✅ Compare SHAP and LIME results for confidence
- ✅ Show Black Box Comparison page to patients for education
- ✅ Use explanations to validate against clinical judgment
- ✅ Download reports for patient records

### For Patients
- ✅ Use Chat Mode for guided experience
- ✅ Read the help text for each field
- ✅ Review the "Learn More" tab to understand results
- ✅ Take screenshots or download report
- ✅ Discuss results with your doctor (not a substitute!)

### For Researchers
- ✅ Load sample data for quick testing
- ✅ Compare different scenarios
- ✅ Export data as CSV for analysis
- ✅ Use Research Summary page for context
- ✅ Review ARCHITECTURE.md for technical details

### For Presenters
- ✅ Use Black Box Comparison page for demos
- ✅ Load sample data for consistent results
- ✅ Show both SHAP and LIME side-by-side
- ✅ Explain the color-coded risk levels
- ✅ Demonstrate real-time validation

---

## 🎨 Interface Elements Guide

### Color Meanings
- 🟢 **Green**: Safe, good, low risk, valid input
- 🟡 **Yellow**: Caution, moderate risk, needs attention
- 🟠 **Orange**: Warning, elevated risk, action recommended
- 🔴 **Red**: Danger, high risk, immediate attention
- 🔵 **Blue**: Information, neutral, explanatory

### Icons Guide
- 👤 Person/Demographics
- ⚖️ Measurement/BMI
- 🚬 Smoking
- 💉 Medical condition
- 🏃 Activity/Exercise
- 😴 Sleep
- ❤️ Health/Heart
- 🔮 Prediction/Analysis
- 🧠 AI/Intelligence
- 📊 Data/Charts
- 🔬 Science/Research

---

## 📞 Getting Help

### In-App Help
- Hover over ℹ️ icons for tooltips
- Click "ℹ️ About This Tool" in sidebar
- Read field help text (shown with each input)
- Check "Learn More" tab in results

### Documentation
- **This file**: General user guide
- **README.md**: Installation and setup
- **ARCHITECTURE.md**: Technical details
- **slides.md**: Presentation material

### Troubleshooting
- See "Common Issues" section above
- Check browser console for errors (F12)
- Verify both servers are running
- Try refreshing the page

---

## ⚠️ Important Reminders

### This is NOT a Medical Device
- ❌ Not for clinical diagnosis
- ❌ Not a substitute for doctors
- ❌ Not FDA approved
- ✅ Educational demonstration only
- ✅ For learning about XAI
- ✅ Always consult healthcare professionals

### Privacy & Data
- 🔒 No data is stored permanently
- 🔒 No data is sent to external servers
- 🔒 All processing happens locally
- 🔒 Data clears when you refresh
- 💡 Use download feature to save results

### Best Practices
- ✅ Verify all inputs are accurate
- ✅ Review the interpretation carefully
- ✅ Understand this is a risk assessment (not diagnosis)
- ✅ Use as one tool among many
- ✅ Combine with clinical judgment

---

## 🌟 Making the Most of This Tool

### For Learning
1. Try different scenarios with sample data
2. Observe how changing one field affects risk
3. Compare SHAP vs LIME explanations
4. Understand which factors matter most
5. Explore the Research Summary page

### For Teaching
1. Use Black Box Comparison for demos
2. Show real-time validation in action
3. Explain XAI with live examples
4. Compare different patient profiles
5. Download reports for discussion

### For Research
1. Test model with various inputs
2. Analyze feature importance patterns
3. Compare with other models/papers
4. Export data for further analysis
5. Validate against domain knowledge

---

## 🎉 Enjoy Using the System!

Remember: This tool is designed to make AI **transparent**, **trustworthy**, and **understandable**. Take your time exploring all the features and learning how Explainable AI can improve healthcare decision-making!

**Questions? Feedback? Suggestions?**
We'd love to hear from you! This is an open-source educational project designed to promote understanding of XAI in healthcare.

---

<div align="center">
  <p><strong>Happy Analyzing! ❤️</strong></p>
  <p><em>Making AI decisions transparent, one prediction at a time</em></p>
</div>
