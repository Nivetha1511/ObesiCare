import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pickle
import os

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Load dataset
print("Loading dataset...")
try:
    df = pd.read_csv('../obesity_dataset_preprocessed.csv')
except FileNotFoundError:
    df = pd.read_csv('../obesity_dataset.csv')

print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Separate features and target
X = df.drop('NObeyesdad', axis=1)
y = df['NObeyesdad']

# Normalize target labels to human class names if preprocessed target is numeric.
if pd.api.types.is_numeric_dtype(y):
    raw_path = '../obesity_dataset.csv'
    if os.path.exists(raw_path):
        raw_df = pd.read_csv(raw_path)
        sorted_labels = sorted(raw_df['NObeyesdad'].unique().tolist())
        id_to_label = {idx: label for idx, label in enumerate(sorted_labels)}
        y = y.astype(int).map(id_to_label)
    else:
        fallback = {
            0: 'Insufficient_Weight',
            1: 'Normal_Weight',
            2: 'Obesity_Type_I',
            3: 'Obesity_Type_II',
            4: 'Obesity_Type_III',
            5: 'Overweight_Level_I',
            6: 'Overweight_Level_II'
        }
        y = y.astype(int).map(fallback)

y = y.astype(str)

# Store feature columns for later use
feature_columns = X.columns.tolist()
print(f"\nFeature columns: {feature_columns}")
print(f"Target classes: {sorted(y.unique().tolist())}")

# Encode target variable
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print(f"\nEncoded classes: {label_encoder.classes_}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\nTraining set size: {X_train_scaled.shape}")
print(f"Test set size: {X_test_scaled.shape}")

# Build ANN model
print("\nBuilding ANN model...")
model = keras.Sequential([
    keras.Input(shape=(X_train_scaled.shape[1],)),
    layers.Dense(128, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    
    layers.Dense(64, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    
    layers.Dense(32, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.2),
    
    layers.Dense(16, activation='relu'),
    layers.Dropout(0.1),
    
    layers.Dense(len(label_encoder.classes_), activation='softmax')
])

# Compile model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print(model.summary())

# Train model
print("\nTraining model...")
history = model.fit(
    X_train_scaled, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    verbose=1,
    callbacks=[
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=0.00001
        )
    ]
)

# Evaluate model
print("\nEvaluating model...")
test_loss, test_accuracy = model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Test Loss: {test_loss:.4f}")

# Save model and preprocessing objects
print("\nSaving model artifacts...")
os.makedirs('../models', exist_ok=True)

# Save model
model.save('../models/obesity_ann.keras')
print("✓ Model saved to models/obesity_ann.keras")

# Save scaler
with open('../models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("✓ Scaler saved to models/scaler.pkl")

# Save label encoder
with open('../models/target_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)
print("✓ Label encoder saved to models/target_encoder.pkl")

# Save feature columns
with open('../models/feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_columns, f)
print("✓ Feature columns saved to models/feature_columns.pkl")

# Save processed datasets
print("\nSaving processed datasets...")
os.makedirs('../data/processed', exist_ok=True)

pd.DataFrame(X_train_scaled, columns=feature_columns).to_csv('../data/processed/X_train.csv', index=False)
pd.DataFrame(X_test_scaled, columns=feature_columns).to_csv('../data/processed/X_test.csv', index=False)
pd.Series(y_train, name='target').to_csv('../data/processed/y_train.csv', index=False)
pd.Series(y_test, name='target').to_csv('../data/processed/y_test.csv', index=False)

print("✓ Processed datasets saved to data/processed/")

print("\n✅ Model training complete!")
print(f"Model accuracy: {test_accuracy*100:.2f}%")
