import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os
import pickle

EXPECTED_COLUMNS = [
    'Gender', 'Age', 'Height', 'Weight', 'family_history_with_overweight',
    'FAVC', 'FCVC', 'NCP', 'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE',
    'CALC', 'MTRANS', 'NObeyesdad'
]


def load_and_clean_raw(path):
    df = pd.read_csv(path)
    if list(df.columns) != EXPECTED_COLUMNS:
        raise ValueError(f"Unexpected columns in {path}")

    # Remove accidental embedded header rows like: Gender,Age,... inside data.
    df = df[df['Gender'].astype(str).str.lower() != 'gender'].copy()

    # Coerce numeric columns and drop invalid rows.
    numeric_cols = ['Age', 'Height', 'Weight', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    before = len(df)
    df = df.dropna()
    removed = before - len(df)
    if removed:
        print(f"  Removed {removed} malformed rows from {path}")

    return df


print("Loading base raw dataset...")
base_df = load_and_clean_raw('obesity_dataset.csv')
print(f"Base shape: {base_df.shape}")

age_file = os.path.join('data', 'age_10_15_raw.csv')
if os.path.exists(age_file):
    print("Loading additional age 10-15 raw dataset...")
    age_df = load_and_clean_raw(age_file)
    print(f"Age 10-15 shape: {age_df.shape}")
    df = pd.concat([base_df, age_df], ignore_index=True)
    print(f"Combined shape: {df.shape}")
else:
    print("No additional age 10-15 dataset found; using base dataset only.")
    df = base_df

# Create a copy for processing
df_proc = df.copy()

# Apply LabelEncoder to categorical columns
categorical_cols = ['Gender', 'family_history_with_overweight', 'FAVC', 'SMOKE', 'SCC', 'CAEC', 'CALC', 'MTRANS']

label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df_proc[col] = le.fit_transform(df_proc[col])
    label_encoders[col] = le
    print(f"\n{col} Encoding:")
    for i, label in enumerate(le.classes_):
        print(f"  {label} -> {i}")

# Encode the target
le_target = LabelEncoder()
df_proc['NObeyesdad'] = le_target.fit_transform(df_proc['NObeyesdad'])
print(f"\nTarget (NObeyesdad) Encoding:")
for i, label in enumerate(le_target.classes_):
    print(f"  {label} -> {i}")

# Save the preprocessed dataset
output_path = 'obesity_dataset_preprocessed.csv'
df_proc.to_csv(output_path, index=False)
print(f"\n✓ Preprocessed dataset saved to {output_path}")
print(f"  Shape: {df_proc.shape}")

# Verify the encoding
print("\nVerifying encoded target distribution:")
print(df_proc['NObeyesdad'].value_counts().sort_index())

# Save encoder mapping for reference
# This will be loaded by the training script
os.makedirs('models', exist_ok=True)
with open('models/categorical_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)
print("\n✓ Categorical encoders saved to models/categorical_encoders.pkl")
