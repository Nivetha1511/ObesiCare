import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

print("=" * 80)
print("COMPREHENSIVE MODEL TRAINING WITH CLASS BALANCING")
print("=" * 80)

# Load dataset
print("\n[1] Loading dataset...")
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(os.path.dirname(script_dir), 'obesity_dataset_preprocessed.csv')
df = pd.read_csv(dataset_path)
print(f"[OK] Loaded {len(df)} samples with {len(df.columns)} columns")

# Separate features and target
X = df.drop('NObeyesdad', axis=1)
y = df['NObeyesdad'].astype(int)

# Get feature columns for later
feature_columns = X.columns.tolist()
print(f"[OK] Features: {len(feature_columns)} columns")

# Encode target
print("\n[2] Encoding target variable...")
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
print(f"[OK] Classes: {label_encoder.classes_.tolist()}")

# Calculate class weights for balanced training
class_weights = {}
unique_classes = np.unique(y_encoded)
for cls in unique_classes:
    class_weights[cls] = len(y_encoded) / (len(unique_classes) * np.sum(y_encoded == cls))
print(f"\n[3] Class weights for balancing:")
for cls_idx, weight in sorted(class_weights.items()):
    cls_name = label_encoder.classes_[cls_idx]
    print(f"  {cls_name:25} -> {weight:.4f}")

# Split data with stratification
print("\n[4] Splitting data (80/20 train/test)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, 
    test_size=0.2, 
    random_state=42, 
    stratify=y_encoded
)
print(f"[OK] Training set: {X_train.shape[0]} samples")
print(f"[OK] Test set: {X_test.shape[0]} samples")

# Scale features
print("\n[5] Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(f"[OK] Features scaled using StandardScaler")

# Build a more robust ANN model
print("\n[6] Building ANN model...")
n_features = X_train_scaled.shape[1]
n_classes = len(np.unique(y_encoded))

model = keras.Sequential([
    keras.Input(shape=(n_features,)),
    
    # Layer 1
    layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
    layers.BatchNormalization(),
    layers.Dropout(0.4),
    
    # Layer 2
    layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    
    # Layer 3
    layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    
    # Layer 4
    layers.Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.0005)),
    layers.Dropout(0.2),
    
    # Output layer
    layers.Dense(n_classes, activation='softmax')
])

# Compile
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print(model.summary())

# Training with callbacks
print("\n[7] Training model...")
history = model.fit(
    X_train_scaled, y_train,
    epochs=150,
    batch_size=16,
    validation_split=0.2,
    class_weight=class_weights,  # CRITICAL: Use class weights for balanced learning
    verbose=1,
    callbacks=[
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=20,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.7,
            patience=8,
            min_lr=0.00001,
            verbose=1
        )
    ]
)

# Evaluate model
print("\n[8] Evaluating model on test set...")
test_loss, test_accuracy = model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"[OK] Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"[OK] Test Loss: {test_loss:.4f}")

# Per-class evaluation
print("\n[9] Per-class evaluation on test set:")
y_pred_raw = model.predict(X_test_scaled, verbose=0)
y_pred = np.argmax(y_pred_raw, axis=1)

from sklearn.metrics import classification_report, confusion_matrix
target_names = [str(c) for c in label_encoder.classes_]
print(classification_report(y_test, y_pred, target_names=target_names))

# Verify all classes are predicted
print("\n[10] Verifying predictions cover all 7 classes on FULL dataset:")
y_pred_full_raw = model.predict(scaler.transform(X.values), verbose=0)
y_pred_full = np.argmax(y_pred_full_raw, axis=1)
pred_counts = np.bincount(y_pred_full, minlength=n_classes)
print("Prediction distribution across all samples:")
for i, count in enumerate(pred_counts):
    pct = 100 * count / len(y)
    print(f"  {label_encoder.classes_[i]:25} {count:4d} samples ({pct:5.1f}%)")

# Save model and preprocessing objects
print("\n[11] Saving model artifacts...")
model_dir = os.path.join(os.path.dirname(script_dir), 'models')
os.makedirs(model_dir, exist_ok=True)

model.save(os.path.join(model_dir, 'obesity_ann.keras'))
print("[OK] Model saved to models/obesity_ann.keras")

with open(os.path.join(model_dir, 'scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)
print("[OK] Scaler saved to models/scaler.pkl")

with open(os.path.join(model_dir, 'target_encoder.pkl'), 'wb') as f:
    pickle.dump(label_encoder, f)
print("[OK] Target encoder saved to models/target_encoder.pkl")

with open(os.path.join(model_dir, 'feature_columns.pkl'), 'wb') as f:
    pickle.dump(feature_columns, f)
print("[OK] Feature columns saved to models/feature_columns.pkl")

print("\n" + "=" * 80)
print("[DONE] TRAINING COMPLETE - Model ready for production!")
print("=" * 80)
