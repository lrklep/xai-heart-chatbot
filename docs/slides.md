---
title: Explainable AI-Driven Chatbot for Heart Disease
subtitle: SHAP + LIME • Random Forest • Chat UI
---

## 1. Introduction
- Problem: ML can predict risk but rarely explains “why”.
- Need: Doctors and patients require transparent, reasoned outputs.
- Solution: XAI adds human-understandable rationale.

## 2. Aim of Research
- Build a chatbot that predicts heart-disease risk and explains decisions (SHAP & LIME).
- Human-friendly conversational interface.

## 3. Algorithms
- Random Forest (best), Decision Tree, Bagging-QSVC.

## 4. Results (paper)
- Accuracy: 92% • Sensitivity: 91.97% • Specificity: 56.81%
- Miss Rate: 8% • Precision: 99.93%

## 5. Explainable AI
- SHAP: feature contributions to prediction.
- LIME: local explanation per individual.

## 6. Workflow
1. Data collection → EDA → Preprocess
2. Train/test split (e.g., 80/20)
3. Train RF → Predict → Explain (SHAP/LIME)
4. Return chatbot-friendly response

## 7. Dataset
- 308,855 records • 19 features (general health, exercise, smoking, diabetes, age/sex, BMI, etc.)

## 8. Comparison with Previous Work
- Prior works often had XAI or Chatbot — not both.
- This approach combines both in one system.

## 9. Limitations
- Dataset/population bias, feature reliance.
- Scale to multilingual, IoT/wearables, more conditions.

## 10. Conclusion
"This XAI-driven chatbot predicts and explains heart-disease risk, building trust with transparent ML."

---
Reference: Salman Muneer et al., IJACSA, Vol. 15, No. 12, 2024.
