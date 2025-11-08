# train/train.py
import json, joblib
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score
import shap

DATA_PATH = Path('data/heart.csv')       # change to your CSV
TARGET = 'heart_disease'                  # binary 0/1
MODEL_DIR = Path('models'); MODEL_DIR.mkdir(exist_ok=True, parents=True)

df = pd.read_csv(DATA_PATH)
assert TARGET in df.columns, f"Target '{TARGET}' not found"

# Drop obvious IDs
for col in ['id','ID','patient_id']:
    if col in df.columns:
        df = df.drop(columns=[col])

y = df[TARGET].astype(int)
X = df.drop(columns=[TARGET])

num_cols = [c for c in X.columns if pd.api.types.is_numeric_dtype(X[c])]
cat_cols = [c for c in X.columns if c not in num_cols]
features = num_cols + cat_cols
(Path(MODEL_DIR/'features.json')).write_text(json.dumps(features))

numeric_pipe = Pipeline([
    ('impute', SimpleImputer(strategy='median')),
    ('scale', StandardScaler())
])

categorical_pipe = Pipeline([
    ('impute', SimpleImputer(strategy='most_frequent')),
    # Use dense output to simplify SHAP/LIME and downstream feature handling
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preproc = ColumnTransformer([
    ('num', numeric_pipe, num_cols),
    ('cat', categorical_pipe, cat_cols)
])

clf = RandomForestClassifier(
    n_estimators=400,
    n_jobs=-1,
    class_weight='balanced',
    random_state=42
)

pipe = Pipeline([('preproc', preproc), ('rf', clf)])

X_tr, X_va, y_tr, y_va = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
pipe.fit(X_tr, y_tr)

proba = pipe.predict_proba(X_va)[:,1]
y_hat = (proba >= 0.5).astype(int)
metrics = {
    'roc_auc': float(roc_auc_score(y_va, proba)),
    'accuracy': float(accuracy_score(y_va, y_hat)),
    'precision': float(precision_score(y_va, y_hat, zero_division=0)),
    'recall': float(recall_score(y_va, y_hat))
}
print('Validation metrics:', metrics)

joblib.dump(pipe, MODEL_DIR/'model.joblib')
joblib.dump(preproc, MODEL_DIR/'preproc.joblib')

try:
    rf = pipe.named_steps['rf']
    X_bg = pipe.named_steps['preproc'].fit_transform(X_tr)
    explainer = shap.TreeExplainer(rf)
    joblib.dump({'explainer': explainer, 'background': X_bg, 'feature_names': pipe.named_steps['preproc'].get_feature_names_out()}, MODEL_DIR/'shap_explainer.joblib')
except Exception as e:
    print('SHAP explainer not cached:', e)

(Path(MODEL_DIR/'metrics.json')).write_text(json.dumps(metrics, indent=2))
