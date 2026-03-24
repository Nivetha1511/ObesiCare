import pandas as pd

raw = pd.read_csv('obesity_dataset.csv')
proc = pd.read_csv('obesity_dataset_preprocessed.csv')

print('CAEC Mapping (first 20 unique pairs):')
caec_pairs = pd.DataFrame({
    'raw': raw['CAEC'],
    'encoded': proc['CAEC']
}).drop_duplicates().sort_values('encoded').head(20)
print(caec_pairs)

print('\n\nCALC Mapping (first 20 unique pairs):')
calc_pairs = pd.DataFrame({
    'raw': raw['CALC'],
    'encoded': proc['CALC']
}).drop_duplicates().sort_values('encoded').head(20)
print(calc_pairs)

print('\n\nMTRANS Mapping (first 20 unique pairs):')
mtrans_pairs = pd.DataFrame({
    'raw': raw['MTRANS'],
    'encoded': proc['MTRANS']
}).drop_duplicates().sort_values('encoded').head(20)
print(mtrans_pairs)
