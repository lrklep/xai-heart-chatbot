# tests/smoke_test.py
import json, joblib, numpy as np

def test_model_loads():
    m = joblib.load('models/model.joblib')
    assert hasattr(m, 'predict_proba')

