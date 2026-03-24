from api.app import app

client = app.test_client()
ages = [10, 11, 12, 13, 14, 15]

# Low-BMI child profile to exercise pediatric handling.
base = {
    'Gender': 0,
    'Height': 1.50,
    'Weight': 39,
    'family_history_with_overweight': 0,
    'FAVC': 0,
    'FCVC': 3,
    'NCP': 3,
    'CAEC': 2,
    'SMOKE': 0,
    'CH2O': 2,
    'SCC': 1,
    'FAF': 2,
    'TUE': 1,
    'CALC': 3,
    'MTRANS': 4
}

print('Age | Prediction            | Confidence | Method               | Note')
print('-' * 110)
for age in ages:
    payload = dict(base)
    payload['Age'] = age
    result = client.post('/predict', json=payload).get_json()
    prediction = result.get('prediction', '-')
    confidence = float(result.get('confidence', 0.0))
    method = result.get('prediction_method', '-')
    note = result.get('note', '')
    print(f"{age:>3} | {prediction:<21} | {confidence:>9.2f}% | {method:<20} | {note}")
