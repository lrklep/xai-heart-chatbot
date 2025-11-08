# 🎯 Quick Reference Card - Heart Disease Risk Assessment

## 🚀 Quick Start

```powershell
# Start API (Terminal 1)
.\.venv\Scripts\activate
uvicorn api.api:app --host 0.0.0.0 --port 8000

# Start UI (Terminal 2)
.\.venv\Scripts\activate
$env:API_URL='http://localhost:8000'
streamlit run app/streamlit_app.py
```

**Access**: http://localhost:8501

---

## 📝 Input Fields Quick Reference

| Field | Values | Example |
|-------|--------|---------|
| Age | 18-120 | 45 |
| Sex | 0=F, 1=M | 1 |
| BMI | 10-60 | 27.5 |
| Smoker | 0=No, 1=Yes | 0 |
| Diabetes | 0=No, 1=Yes | 1 |
| Activity | 0=No, 1=Yes | 1 |
| Sleep | 0-24 hrs | 7 |
| Health | 1-5 scale | 3 |

---

## 🎨 Risk Levels

| Range | Color | Meaning |
|-------|-------|---------|
| 0-30% | 🟢 Green | Low Risk |
| 30-50% | 🟡 Yellow | Moderate-Low |
| 50-70% | 🟠 Orange | Moderate-High |
| 70-100% | 🔴 Red | High Risk |

---

## 🔬 Understanding XAI

### SHAP
- Shows **how each feature contributes** globally
- Red bars = increases risk
- Blue bars = decreases risk

### LIME
- Explains **this specific prediction** locally
- Red bars = increases risk for YOU
- Green bars = decreases risk for YOU

---

## 💡 Quick Tips

### Input Mode
- **Form** = Fast, see all fields
- **Chat** = Guided, one-by-one

### Validation Colors
- ✅ Green = Valid
- ⚠️ Yellow = Warning
- ❌ Red = Error

### Downloads
- 📄 TXT = Full report
- 📊 CSV = Data only

---

## 🎓 Key Pages

| Page | Purpose |
|------|---------|
| Main | Risk assessment |
| Research | Paper analysis |
| Comparison | Black Box vs XAI demo |

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| API error | Start backend: `uvicorn api.api:app` |
| No model | Run: `python train/train.py` |
| Timeout | Normal, prediction still works |
| Validation | Read error message, fix field |

---

## 📞 Quick Help

- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs
- **User Guide**: `docs/USER_GUIDE.md`
- **Full README**: `README.md`

---

## ⚠️ Remember

- 🚫 NOT medical advice
- 🚫 NOT for diagnosis
- ✅ Educational only
- ✅ Always consult doctors

---

<div align="center">
  <p><strong>Quick Reference • Keep Handy • Share with Users</strong></p>
</div>
