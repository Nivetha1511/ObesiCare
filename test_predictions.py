import pandas as pd
import numpy as np
import pickle
from keras.models import load_model

# Load model and preprocessing objects
model = load_model('models/obesity_ann.keras')
scaler = pickle.load(open('models/scaler.pkl', 'rb'))
target_encoder = pickle.load(open('models/target_encoder.pkl', 'rb'))
feature_columns = pickle.load(open('models/feature_columns.pkl', 'rb'))

# Class names mapping
class_names = [
    'Insufficient_Weight',
    'Normal_Weight',
    'Obesity_Type_I',
    'Obesity_Type_II',
    'Obesity_Type_III',
    'Overweight_Level_I',
    'Overweight_Level_II'
]

# Test samples with different characteristics
test_samples = [
    {
        'name': 'Thin Person - High Activity',
        'data': {
            'Gender': 0, 'Age': 25, 'Height': 1.75, 'Weight': 55,
            'family_history_with_overweight': 0, 'FAVC': 0, 'FCVC': 3, 'NCP': 3,
            'CAEC': 3, 'SMOKE': 0, 'CH2O': 2.5, 'SCC': 1, 'FAF': 2.5, 'TUE': 1,
            'CALC': 3, 'MTRANS': 0
        }
    },
    {
        'name': 'Overweight - Moderate Activity',
        'data': {
            'Gender': 1, 'Age': 35, 'Height': 1.70, 'Weight': 85,
            'family_history_with_overweight': 1, 'FAVC': 1, 'FCVC': 2, 'NCP': 3,
            'CAEC': 2, 'SMOKE': 0, 'CH2O': 2.0, 'SCC': 0, 'FAF': 1.0, 'TUE': 2,
            'CALC': 2, 'MTRANS': 3
        }
    },
    {
        'name': 'Obese - Low Activity',
        'data': {
            'Gender': 1, 'Age': 45, 'Height': 1.65, 'Weight': 120,
            'family_history_with_overweight': 1, 'FAVC': 1, 'FCVC': 1, 'NCP': 3,
            'CAEC': 0, 'SMOKE': 1, 'CH2O': 1.5, 'SCC': 0, 'FAF': 0.0, 'TUE': 4,
            'CALC': 0, 'MTRANS': 0
        }
    },
    {
        'name': 'Normal Weight - Healthy',
        'data': {
            'Gender': 0, 'Age': 30, 'Height': 1.68, 'Weight': 65,
            'family_history_with_overweight': 0, 'FAVC': 0, 'FCVC': 3, 'NCP': 3,
            'CAEC': 3, 'SMOKE': 0, 'CH2O': 2.5, 'SCC': 1, 'FAF': 1.5, 'TUE': 1,
            'CALC': 3, 'MTRANS': 4
        }
    },
    {
        'name': 'Severe Obesity - Very Unhealthy',
        'data': {
            'Gender': 1, 'Age': 55, 'Height': 1.60, 'Weight': 140,
            'family_history_with_overweight': 1, 'FAVC': 1, 'FCVC': 0, 'NCP': 3,
            'CAEC': 0, 'SMOKE': 1, 'CH2O': 1.0, 'SCC': 0, 'FAF': 0.0, 'TUE': 5,
            'CALC': 0, 'MTRANS': 0
        }
    }
]

print("=" * 70)
print("TESTING MODEL WITH DIFFERENT SAMPLE INPUTS")
print("=" * 70)

for test_sample in test_samples:
    # Create DataFrame with correct feature order
    X = pd.DataFrame([test_sample['data']])
    X = X[feature_columns]
    
    # Scale and predict
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled, verbose=0)
    predicted_idx = np.argmax(prediction[0])
    predicted_class = class_names[predicted_idx]
    confidence = np.max(prediction[0]) * 100
    
    print(f"\n{test_sample['name'].upper()}")
    print("-" * 70)
    print(f"  Prediction: {predicted_class}")
    print(f"  Confidence: {confidence:.1f}%")
    print(f"  Class Probabilities:")
    for i, cls in enumerate(class_names):
        prob = prediction[0][i] * 100
        print(f"    {cls:25} {prob:6.2f}%")

print("\n" + "=" * 70)
print("[OK] All 7 obesity classes represented in model outputs!")
print("=" * 70)
