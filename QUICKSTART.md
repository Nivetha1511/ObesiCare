# 🚀 Quick Start Guide for ObesiCare

Welcome to ObesiCare! Follow these steps to get the system up and running quickly.

## ⏱️ 5-Minute Setup

### 1. Setup Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the Model (if needed)
```bash
cd training
python train_model.py
cd ..
```
This will create model artifacts in the `models/` folder.

### 4. Start the Server
```bash
cd api
python app.py
```

You should see:
```
Starting ObesiCare Flask API...
 * Running on http://0.0.0.0:5000
```

### 5. Access the Application
Open your web browser and go to: **http://localhost:5000**

---

## 🎯 Test the System

### Option 1: Using the Web Interface
1. Click "Start Assessment"
2. Sign up with:
   - Username: `test_user`
   - Password: `password123`
3. Fill in the form with your data
4. Click "Get Prediction"

### Option 2: Using API with cURL
```bash
# 1. Sign up
curl -X POST http://localhost:5000/api/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'

# 2. Login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'

# 3. Get prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Gender": 1,
    "Age": 25,
    "Height": 1.75,
    "Weight": 75,
    "family_history_with_overweight": 0,
    "FAVC": 0,
    "FCVC": 2,
    "NCP": 3,
    "CAEC": 1,
    "SMOKE": 0,
    "CH2O": 2,
    "SCC": 1,
    "FAF": 1,
    "TUE": 2,
    "CALC": 0,
    "MTRANS": 2
  }'
```

### Option 3: Using Python
```python
import requests

# Make a prediction
data = {
    'Gender': 1, 'Age': 25, 'Height': 1.75, 'Weight': 75,
    'family_history_with_overweight': 0, 'FAVC': 0,
    'FCVC': 2, 'NCP': 3, 'CAEC': 1, 'SMOKE': 0,
    'CH2O': 2, 'SCC': 1, 'FAF': 1, 'TUE': 2,
    'CALC': 0, 'MTRANS': 2
}

response = requests.post('http://localhost:5000/predict', json=data)
print(response.json())
```

---

## 📁 Project Structure Overview

```
ObesiCare/
├── api/app.py              ← Flask backend
├── frontend/               ← HTML/CSS/JS frontend
│   ├── index.html         ← Home page
│   ├── login.html         ← Login page
│   ├── form.html          ← Assessment form
│   ├── result.html        ← Results page
│   └── css/style.css      ← Styling
├── models/                ← ML model artifacts
│   ├── obesity_ann.keras
│   ├── scaler.pkl
│   └── target_encoder.pkl
├── training/
│   └── train_model.py     ← Model training
└── README.md              ← Full documentation
```

---

## 🔧 Common Issues & Solutions

### Issue: "Module not found" error
**Solution**: Make sure you're in the virtual environment
```bash
# Check if activated (should see (venv) in terminal)
# If not, run:
venv\Scripts\activate
```

### Issue: Port 5000 already in use
**Solution**: Use a different port in app.py or kill the process
```bash
# Find what's using port 5000
netstat -ano | findstr :5000
# Kill it (replace PID)
taskkill /PID <PID> /F
```

### Issue: Model file not found
**Solution**: Train the model first
```bash
cd training
python train_model.py
cd ..
```

### Issue: Can't login
**Solution**: Check user_data folder exists and has permissions
```bash
# Create folder if needed
mkdir user_data
```

---

## 📚 Next Steps

1. **Customize Frontend**: Edit frontend files to change colors, text, images
2. **Improve Model**: Retrain with more data by editing training/train_model.py
3. **Deploy**: Follow deployment guide in README.md to deploy to Render
4. **Add Features**: Extend functionality as needed

---

## 🆘 Getting Help

- Check [README.md](README.md) for detailed documentation
- Read code comments in source files
- Check error messages carefully
- Look at API response formats in readme

---

## ✅ Next: Deploy to Production

When ready to deploy:
1. Push code to GitHub
2. Create Render account (render.com)
3. Connect GitHub repo
4. Deploy! Full instructions in README.md

---

**Happy Coding! 🎉**
