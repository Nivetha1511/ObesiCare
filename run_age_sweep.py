from api.app import app

client = app.test_client()
ages = [10, 15, 20, 30, 40, 50]

base = {
    'Gender': 0,
    'Height': 1.60,
    'Weight': 68,
    'family_history_with_overweight': 1,
    'FAVC': 1,
    'FCVC': 2,
    'NCP': 3,
    'CAEC': 2,
    'SMOKE': 0,
    'CH2O': 2,
    'SCC': 0,
    'FAF': 1,
    'TUE': 2,
    'CALC': 2,
    'MTRANS': 3
}

print('Age | Prediction           | Confidence | Method')
print('-' * 68)
for age in ages:
    payload = dict(base)
    payload['Age'] = age
    result = client.post('/predict', json=payload).get_json()
    prediction = result.get('prediction', '-')
    confidence = float(result.get('confidence', 0.0))
    method = result.get('prediction_method', '-')
    print(f"{age:>3} | {prediction:<20} | {confidence:>9.2f}% | {method}")
