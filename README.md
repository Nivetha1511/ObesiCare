drive link: https://drive.google.com/drive/folders/1Yg0DAD-32aJ-cHlAXvhbPrEP85EnRgzq?usp=drive_link

# ObesiCare 🏥

**AI-Powered Obesity Risk Prediction System**

A complete full-stack web application for predicting obesity risk using machine learning and user lifestyle data. The system combines a sophisticated artificial neural network backend with an intuitive, responsive frontend interface.

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Model Information](#model-information)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

---

## ✨ Features

### 🤖 Machine Learning
- **Trained ANN Model**: 7-layer neural network with batch normalization and dropout
- **High Accuracy**: >90% accuracy on test dataset
- **16 Health Parameters**: Comprehensive assessment of obesity risk
- **7 Risk Categories**: From "Insufficient Weight" to "Obese III"
- **Confidence Scores**: Transparency in prediction reliability

### 🔐 Authentication
- Secure user registration and login system
- Password hashing with SHA256
- Excel-based user database (user_data.xlsx)
- Session management with localStorage

### 🎨 Frontend
- **Modern UI**: Card-based layout with glassmorphism effects
- **Responsive Design**: Mobile-optimized for all devices
- **Progressive Web App (PWA)**: Install as standalone app
- **Smooth Animations**: Professional transitions and interactions
- **Color Theme**: Health-focused blue/green gradient

### 📱 Responsive Pages
- **Landing Page**: Information about obesity with smooth navigation
- **Login/Signup**: Secure authentication
- **Assessment Form**: 16-parameter health data collection
- **Results Page**: Detailed predictions with confidence scores

### 🌐 Backend API
- **Flask Framework**: Lightweight and efficient
- **RESTful API**: Clean endpoint structure
- **CORS Support**: Cross-origin resource sharing enabled
- **Error Handling**: Comprehensive error messages

---

## 📁 Project Structure

```
ObesiCare/
├── api/
│   └── app.py                          # Flask application entry point
│
├── training/
│   └── train_model.py                  # Model training script
│
├── models/                             # Saved ML artifacts
│   ├── obesity_ann.keras               # Trained ANN model
│   ├── scaler.pkl                      # StandardScaler for feature normalization
│   ├── target_encoder.pkl              # LabelEncoder for target classes
│   └── feature_columns.pkl             # Feature column names
│
├── data/
│   ├── processed/                      # Processed datasets
│   │   ├── X_train.csv
│   │   ├── X_test.csv
│   │   ├── y_train.csv
│   │   └── y_test.csv
│   ├── obesity_dataset.csv             # Raw dataset
│   └── obesity_dataset_preprocessed.csv # Preprocessed dataset
│
├── frontend/                           # Frontend application
│   ├── index.html                      # Landing page
│   ├── login.html                      # Login page
│   ├── signup.html                     # Sign up page
│   ├── form.html                       # Assessment form
│   ├── result.html                     # Results page
│   ├── manifest.json                   # PWA manifest
│   │
│   ├── css/
│   │   └── style.css                   # Global styles (comprehensive)
│   │
│   ├── js/
│   │   └── main.js                     # Main JavaScript logic
│   │
│   └── images/                         # UI images and backgrounds
│
├── user_data/
│   └── users.xlsx                      # User authentication database
│
├── requirements.txt                    # Python dependencies
├── Procfile                            # Render deployment configuration
├── .gitignore                          # Git ignore rules
├── README.md                           # This file
└── LICENSE                             # Project license (optional)
```

---

## 🏗️ Architecture

### System Flow

```
User Opens Website
        ↓
Reads Information About Obesity
        ↓
Clicks "Start Assessment"
        ↓
Login / Sign Up
        ↓
Assessment Form (16 Parameters)
        ↓
Frontend Sends POST Request to /predict
        ↓
Backend: Features → Scaler → Model → Prediction
        ↓
Result Displayed with:
  - Risk Level
  - Confidence Score (%)
  - Recommendations
  - Risk Breakdown Chart
```

### Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend** | Flask (Python) |
| **ML/AI** | TensorFlow, Keras, scikit-learn |
| **Database** | Excel (openpyxl, pandas) |
| **Deployment** | Render, Gunicorn |
| **PWA** | Service Workers, Web App Manifest |

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone/Download Project
```bash
cd ObesiCare
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Model Artifacts
Ensure these files exist in `models/`:
- `obesity_ann.keras`
- `scaler.pkl`
- `target_encoder.pkl`
- `feature_columns.pkl`

If not, train the model first:
```bash
cd training
python train_model.py
cd ..
```

### Step 5: Run Application
```bash
cd api
python app.py
```

The application will start on `http://localhost:5000`

---

## ⚙️ Configuration

### Flask Configuration
Edit `api/app.py` to modify:
- Debug mode
- Port number
- CORS settings
- Model paths

### Model Configuration
Modify `training/train_model.py` for:
- Network architecture
- Hyperparameters
- Training epochs
- Batch size

### Feature Configuration
Available health parameters:
1. **Gender** (0=Female, 1=Male)
2. **Age** (in years)
3. **Height** (in meters)
4. **Weight** (in kg)
5. **Family History** (0=No, 1=Yes)
6. **FAVC** - High calorie food (0-1)
7. **FCVC** - Vegetable consumption (0-4)
8. **NCP** - Number of meals (1-4)
9. **CAEC** - Eating between meals (0-3)
10. **SMOKE** (0=No, 1=Yes)
11. **CH2O** - Water intake liters (0-4)
12. **SCC** - Calorie monitoring (0=No, 1=Yes)
13. **FAF** - Physical activity hours (0-3)
14. **TUE** - Screen time hours (0-4)
15. **CALC** - Alcohol consumption (0-3)
16. **MTRANS** - Transportation mode (0-4)

---

## 📖 Usage

### For Users

1. **Visit Website**: Open `http://localhost:5000` in your browser
2. **Create Account**: Click "Start Assessment" → "Create Account"
3. **Fill Form**: Enter your health and lifestyle information
4. **Get Prediction**: Click "Get Prediction"
5. **View Results**: See your obesity risk level and recommendations

### For Developers

```python
# Example API call
import requests

data = {
    'Gender': 1,
    'Age': 25,
    'Height': 1.75,
    'Weight': 80,
    'family_history_with_overweight': 1,
    'FAVC': 0,
    'FCVC': 2.5,
    'NCP': 3,
    'CAEC': 1,
    'SMOKE': 0,
    'CH2O': 2.0,
    'SCC': 1,
    'FAF': 1.5,
    'TUE': 2.0,
    'CALC': 1,
    'MTRANS': 2
}

response = requests.post('http://localhost:5000/predict', json=data)
result = response.json()

print(f"Risk Level: {result['risk_level']}")
print(f"Confidence: {result['confidence']}%")
```

---

## 📡 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/signup
Content-Type: application/json

{
    "username": "john_doe",
    "password": "secure_password_123"
}
```

**Response (201 Created)**:
```json
{
    "success": true,
    "message": "Account created successfully",
    "username": "john_doe"
}
```

#### Login User
```http
POST /api/login
Content-Type: application/json

{
    "username": "john_doe",
    "password": "secure_password_123"
}
```

**Response (200 OK)**:
```json
{
    "success": true,
    "message": "Login successful",
    "username": "john_doe"
}
```

### Prediction Endpoint

#### Make Prediction
```http
POST /predict
Content-Type: application/json

{
    "Gender": 1,
    "Age": 25,
    "Height": 1.75,
    "Weight": 80,
    "family_history_with_overweight": 1,
    "FAVC": 0,
    "FCVC": 2.5,
    "NCP": 3,
    "CAEC": 1,
    "SMOKE": 0,
    "CH2O": 2.0,
    "SCC": 1,
    "FAF": 1.5,
    "TUE": 2.0,
    "CALC": 1,
    "MTRANS": 2
}
```

**Response (200 OK)**:
```json
{
    "success": true,
    "prediction": "Normal Weight",
    "prediction_index": 1,
    "confidence": 87.35,
    "risk_level": "Normal Weight",
    "icon": "✅",
    "color": "#2ecc71",
    "all_predictions": {
        "0": 2.14,
        "1": 87.35,
        "2": 8.92,
        "3": 1.23,
        "4": 0.28,
        "5": 0.06,
        "6": 0.02
    }
}
```

### Error Responses

**Missing Required Fields (400 Bad Request)**:
```json
{
    "success": false,
    "message": "Missing feature: Height"
}
```

**Authentication Failed (401 Unauthorized)**:
```json
{
    "success": false,
    "message": "Invalid password",
    "action": "retry"
}
```

**User Not Found (404 Not Found)**:
```json
{
    "success": false,
    "message": "User not found",
    "action": "signup"
}
```

---

## 🧠 Model Information

### Architecture

```
Input Layer (16 neurons)
    ↓
Dense(128) + BatchNorm + ReLU + Dropout(0.3)
    ↓
Dense(64) + BatchNorm + ReLU + Dropout(0.3)
    ↓
Dense(32) + BatchNorm + ReLU + Dropout(0.2)
    ↓
Dense(16) + ReLU + Dropout(0.1)
    ↓
Dense(7 classes) + Softmax
```

### Model Statistics
- **Total Parameters**: 14,055
- **Trainable Parameters**: 13,607
- **Training Samples**: 1,669
- **Test Samples**: 418
- **Test Accuracy**: ~95%

### Obesity Classes
0. Insufficient Weight
1. Normal Weight
2. Overweight I
3. Overweight II
4. Obese I
5. Obese II
6. Obese III

### Training Details
- **Optimizer**: Adam (lr=0.001)
- **Loss Function**: Sparse Categorical Crossentropy
- **Early Stopping**: Monitor val_loss, patience=15
- **Learning Rate Reduction**: Factor=0.5, patience=5

---

## 🌐 Deployment

### Deploy to Render

1. **Prepare Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Create new Web Service
   - Connect your GitHub repository
   - Select "Python" as runtime
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn -w 4 -b 0.0.0.0:$PORT api.app:app`

3. **Environment Variables**
   - `FLASK_ENV`: production
   - `FLASK_DEBUG`: 0

4. **Deploy**
   - Click "Deploy Web Service"
   - Wait for deployment to complete
   - Your API will be live at `https://your-app.onrender.com`

### Deploy to Other Platforms

#### Heroku
```bash
heroku create your-app-name
git push heroku main
```

#### AWS / GCP / Azure
Use similar container-based deployment with Gunicorn

---

## 🐛 Troubleshooting

### Model Not Found
**Error**: `FileNotFoundError: ../models/obesity_ann.keras`

**Solution**:
```bash
cd training
python train_model.py
```

### Port Already in Use
**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

### CORS Error
**Error**: `Access to XMLHttpRequest blocked by CORS policy`

**Solution**: Ensure Flask-CORS is installed and app is configured:
```python
from flask_cors import CORS
CORS(app)
```

### User Data File Issues
**Error**: `Permission denied` or file not found

**Solution**:
- Ensure `user_data/` directory exists
- Check file permissions
- Run: `python -c "from api.app import ensure_user_file; ensure_user_file()"`

### TensorFlow/CUDA Issues
**Error**: `Failed to load DLL` or GPU not recognized

**Solution**:
- Use CPU-only version: `pip install tensorflow-cpu`
- Or install CUDA compatibility: Check TensorFlow documentation

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Areas for Contribution
- Model improvement and retraining
- UI/UX enhancements
- Additional health parameters
- Mobile app development
- Documentation improvements
- Internationalization (i18n)
- Performance optimization

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## ⚠️ Important Disclaimer

**THIS APPLICATION IS FOR EDUCATIONAL AND INFORMATIONAL PURPOSES ONLY**

This system:
- Is NOT a medical diagnosis tool
- Should NOT replace professional medical advice
- Requires consultation with qualified healthcare providers
- Is trained on specific datasets and may not be universally applicable

**Always consult with healthcare professionals for:**
- Medical diagnosis
- Treatment recommendations
- Personalized health plans
- Any health concerns

The creators are NOT responsible for any misuse or incorrect interpretation of results.

---

## 📞 Support

For issues, questions, or feedback:
- Open an issue on GitHub
- Email: support@obesicare.com
- Documentation: Check README.md and code comments

---

## 🙏 Acknowledgments

- TensorFlow/Keras team for excellent ML libraries
- Flask community for web framework
- All contributors and testers

---

**Last Updated**: March 2024  
**Version**: 1.0.0  
**Status**: Production Ready ✅

---

Made with ❤️ for better health awareness
