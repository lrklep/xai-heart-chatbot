import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="XAI Research Summary", page_icon="🧠")
st.title("🧠💬 Explainable AI-Driven Chatbot for Heart Disease")
st.caption("Based on: Salman Muneer et al., IJACSA, Vol. 15, No. 12, 2024")

with st.expander("1) Background • Why XAI for healthcare?", expanded=True):
    st.write(
        """
        Chatbots can collect basic health info and predict heart-disease risk, but doctors and patients
        need to know why a model decided something. Explainable AI (XAI) adds reasons behind
        predictions so humans can validate, trust, and act.
        """
    )

with st.expander("2) Aim • What did the paper build?", expanded=True):
    st.markdown(
        "- End-to-end chatbot that: predicts heart disease risk, explains the prediction (SHAP/LIME), and serves a user-friendly interface."
    )
    st.markdown("- Algorithms tried: Random Forest (best), Decision Tree, Bagging-QSVC")

with st.expander("3) Reported results (paper)"):
    cols = st.columns(3)
    with cols[0]:
        st.metric("Accuracy", "92%")
        st.metric("Sensitivity", "91.97%")
    with cols[1]:
        st.metric("Specificity", "56.81%")
        st.metric("Miss Rate", "8%")
    with cols[2]:
        st.metric("Precision", "99.93%")

with st.expander("4) XAI in simple terms"):
    st.write("SHAP: feature contributions to the prediction (global + local).")
    st.write("LIME: local explanation for a single case with interpretable weights.")

with st.expander("5) Methodology • How it works"):
    st.markdown(
        """
        1. Collect inputs (age, sex, diabetes, activity, etc.)
        2. Preprocess: impute, encode, scale
        3. Train/test split (e.g., 80/20)
        4. Train Random Forest
        5. Predict probability of heart disease
        6. Explain with SHAP + LIME
        7. Return chatbot-style response
        """
    )

with st.expander("6) Dataset (paper)"):
    st.write("308,855 records • 19 features (lifestyle, general health, age/sex, etc.)")

# Local model comparison
st.subheader("📊 Compare: paper vs this demo (local model)")
metrics_path = Path("models/metrics.json")
if metrics_path.exists():
    m = json.loads(metrics_path.read_text())
    cols = st.columns(4)
    with cols[0]:
        st.metric("Accuracy (local)", f"{m.get('accuracy', 0):.2f}")
    with cols[1]:
        st.metric("ROC AUC (local)", f"{m.get('roc_auc', 0):.2f}")
    with cols[2]:
        st.metric("Precision (local)", f"{m.get('precision', 0):.2f}")
    with cols[3]:
        st.metric("Recall (local)", f"{m.get('recall', 0):.2f}")
    st.info(
        "Numbers differ from the paper because this demo uses a tiny sample dataset and default settings."
    )
else:
    st.warning("Local metrics not found yet. Run training first (train/train.py).")

with st.expander("7) Limitations & future work"):
    st.write(
        "- Population bias; limited features; need for real-world data integration.\n"
        "- Next: multilingual chatbot, IoT/wearables, more conditions (diabetes, stroke)."
    )

st.caption(
    "Educational demo • Not medical advice. Cite: Muneer, S., et al. 'Explainable AI-Driven Chatbot System for Heart Disease Prediction Using Machine Learning', IJACSA 2024."
)
