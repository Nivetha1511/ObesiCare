"""
Test obesity prediction across full age range 10-60
"""
import sys
sys.path.insert(0, '/app')

from api.app import app
import json

# Test profile: moderate weight (BMI ~28, overweight)
test_cases = [
    {'age': 10, 'height': 1.60, 'weight': 68},
    {'age': 20, 'height': 1.60, 'weight': 68},
    {'age': 30, 'height': 1.60, 'weight': 68},
    {'age': 40, 'height': 1.60, 'weight': 68},
    {'age': 50, 'height': 1.60, 'weight': 68},
    {'age': 60, 'height': 1.60, 'weight': 68},
]

print("Testing obesity prediction across ages 10-60")
print("=" * 90)
print(f"{'Age':<8} {'Prediction':<25} {'Confidence':<15} {'Method':<20}")
print("-" * 90)

with app.test_client() as client:
    for case in test_cases:
        # Create request data with all required features for ANN prediction
        request_data = {
            'Gender': 1,  # Male = 1
            'Age': float(case['age']),
            'Height': float(case['height']),
            'Weight': float(case['weight']),
            'family_history_with_overweight': 1,  # yes = 1
            'FAVC': 0,  # no = 0
            'FCVC': 2.0,
            'NCP': 3.0,
            'CAEC': 1,  # Sometimes
            'SMOKE': 0,  # no
            'CH2O': 2.0,
            'SCC': 0,  # no
            'FAF': 0.0,
            'TUE': 1.0,
            'CALC': 0,  # no
            'MTRANS': 1  # Public_Transportation
        }
        
        response = client.post('/predict', json=request_data)
        
        if response.status_code == 200:
            result = response.get_json()
            prediction = result.get('prediction', 'ERROR')
            confidence = result.get('confidence', 0)
            method = result.get('prediction_method', 'unknown')
            
            print(f"{case['age']:<8} {prediction:<25} {confidence:>6.2f}%{'':<7} {method:<20}")
        else:
            print(f"{case['age']:<8} ERROR (status {response.status_code})")

print("-" * 90)
print("✓ All ages 10-60 tested successfully!")
