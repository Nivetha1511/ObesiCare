import pandas as pd

# Check base dataset age range
df = pd.read_csv('obesity_dataset.csv')
print(f'Age range in base dataset: {df["Age"].min():.1f} - {df["Age"].max():.1f}')
print(f'Total rows: {len(df)}')

# Check preprocessed dataset
df_prep = pd.read_csv('obesity_dataset_preprocessed.csv')
print(f'Age range in preprocessed dataset: {df_prep["Age"].min():.1f} - {df_prep["Age"].max():.1f}')
print(f'Total rows: {len(df_prep)}')
