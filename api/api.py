# api/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib, json, traceback
import numpy as np
import pandas as pd
import numpy as np
from functools import lru_cache

app = FastAPI(title='XAI Heart Risk API', version='1.0')

model = joblib.load('models/model.joblib')
try:
    shap_cache = joblib.load('models/shap_explainer.joblib')
    shap_explainer = shap_cache.get('explainer')
    bg = shap_cache.get('background')
    feat_names = shap_cache.get('feature_names')
except Exception:
    shap_explainer = None; bg = None; feat_names = None

with open('models/features.json') as f:
    FEATURES = json.load(f)

class PatientInput(BaseModel):
    payload: dict

    def as_ordered_list(self):
        """Return feature values ordered according to training features list.
        Missing keys become np.nan to allow sklearn imputers to work."""
        return [self.payload.get(k, np.nan) for k in FEATURES]

    def as_dataframe(self):
        """Return a single-row pandas DataFrame with training feature names as columns."""
        row = {k: self.payload.get(k, np.nan) for k in FEATURES}
        return pd.DataFrame([row])

@app.get('/health')
def health():
    return {'status':'ok'}

@app.post('/predict')
def predict(inp: PatientInput):
    try:
        x_df = inp.as_dataframe()
        proba = model.predict_proba(x_df)[0, 1]
        pred = int(proba >= 0.5)
        return {
            'prediction': pred,
            'probability': float(proba),
            'threshold': 0.5,
            'features_used': FEATURES
        }
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail={'error': str(e), 'trace': tb})

@lru_cache(maxsize=1)
def _lime_explainer(bg_data, feature_names, class_names=('no','yes')):
    from lime.lime_tabular import LimeTabularExplainer
    return LimeTabularExplainer(
        bg_data,
        feature_names=feature_names,
        discretize_continuous=True,
        mode='classification',
        class_names=class_names
    )

@app.post('/explain')
def explain(inp: PatientInput):
    out = {'shap': None, 'lime': None}
    # SHAP
    try:
        import shap
        pre = model.named_steps['preproc']
        rf = model.named_steps['rf']
        x_pp = pre.transform(inp.as_dataframe())
        # ensure dense
        if hasattr(x_pp, 'toarray'):
            x_pp_dense = x_pp.toarray()
        else:
            x_pp_dense = np.asarray(x_pp)
        
        # Use default TreeExplainer (fastest and most stable)
        explainer = shap.TreeExplainer(rf)
        sv_all = explainer.shap_values(x_pp_dense)
        
        # Handle different return formats
        if isinstance(sv_all, list) and len(sv_all) == 2:
            # Binary classification: [class_0_shap, class_1_shap]
            sv = sv_all[1]  # positive class
        elif isinstance(sv_all, np.ndarray) and sv_all.ndim == 3:
            # Shape: (n_samples, n_features, n_classes)
            sv = sv_all[0, :, 1]  # first sample, all features, positive class
        elif isinstance(sv_all, np.ndarray) and sv_all.ndim == 2:
            # Shape: (n_samples, n_features) - single output
            sv = sv_all[0, :]
        else:
            sv = np.asarray(sv_all).flatten()
        
        # Safe conversion
        flat_values = np.asarray(sv).flatten().astype(float)
        names = list(pre.get_feature_names_out())
        
        # Defensive alignment
        m = min(len(names), len(flat_values))
        pairs = list(zip(names[:m], flat_values[:m]))
        top = sorted(pairs, key=lambda t: abs(t[1]), reverse=True)[:10]
        out['shap'] = [{'feature': n, 'contribution': float(v)} for n, v in top]
    except Exception as e:
        import traceback
        out['shap_error'] = f"{str(e)}\n{traceback.format_exc()}"

    # LIME
    try:
        pre = model.named_steps['preproc']
        rf = model.named_steps['rf']
        x0_sparse = pre.transform(inp.as_dataframe())
        if hasattr(x0_sparse, 'toarray'):
            x0 = x0_sparse.toarray()
        else:
            x0 = np.asarray(x0_sparse)
        
        # Ensure float type and 2D shape
        x0 = x0.astype(float)
        
        # Simplified background: use small sample
        bg_data = np.tile(x0, (50, 1))  # Reduced from 200 for speed
        feature_names = list(pre.get_feature_names_out())
        
        # Build LIME explainer with simpler settings
        from lime.lime_tabular import LimeTabularExplainer
        lime_exp = LimeTabularExplainer(
            bg_data,
            feature_names=feature_names,
            discretize_continuous=False,  # Faster
            mode='classification',
            class_names=['No Disease', 'Disease']
        )
        
        def predict_fn(z):
            proba = rf.predict_proba(z)[:, 1]
            return np.column_stack([1 - proba, proba])
        
        exp = lime_exp.explain_instance(
            x0[0], 
            predict_fn, 
            num_features=10,
            num_samples=100  # Reduced from default 5000 for speed
        )
        out['lime'] = [{'feature': str(f), 'weight': float(w)} for f, w in exp.as_list()]
    except Exception as e:
        import traceback
        out['lime_error'] = f"{str(e)}\n{traceback.format_exc()}"

    return out
