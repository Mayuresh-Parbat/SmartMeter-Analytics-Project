# scripts/step2_cleaning.py
import pandas as pd
import numpy as np
import sqlite3
import os

# Paths
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_IN = os.path.join(ROOT, "data", "Smart_Meter_Data.csv")
CLEAN_OUT = os.path.join(ROOT, "data", "Clean_Smart_Meter_Data.csv")
ANOM_OUT = os.path.join(ROOT, "data", "Anomalies.csv")
DB_PATH = os.path.join(ROOT, "data", "smart_meter.db")

# 1) Load
df = pd.read_csv(DATA_IN)
print("Loaded rows:", len(df))

# 2) Basic cleaning
df.drop_duplicates(inplace=True)
df = df[df["Consumption_kWh"].notnull()]            # drop rows missing consumption
df = df[df["Consumption_kWh"] >= 0]                  # remove negative values
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df[df['Date'].notnull()]

print("After cleaning rows:", len(df))

# 3) Z-score per meter + global spike method
df['mean_meter'] = df.groupby('Meter_ID')['Consumption_kWh'].transform('mean')
df['std_meter']  = df.groupby('Meter_ID')['Consumption_kWh'].transform('std').fillna(0.0)

# z-score (per-meter)
df['zscore'] = (df['Consumption_kWh'] - df['mean_meter']) / (df['std_meter'].replace(0, np.nan))
df['zscore'].fillna(0, inplace=True)

# global spike rule (2x overall mean)
global_mean = df['Consumption_kWh'].mean()
df['global_spike'] = (df['Consumption_kWh'] > 2 * global_mean).astype(int)

# mark anomalies: zscore abs > 3 or global spike
df['Anomaly_Flag'] = ((df['zscore'].abs() > 3) | (df['global_spike'] == 1)).astype(int)

# 4) Label anomaly type
def anomaly_type(r):
    if r['zscore'] and abs(r['zscore']) > 3:
        return 'per_meter_outlier'
    if r['global_spike'] == 1:
        return 'global_spike'
    return 'normal'

df['Anomaly_Type'] = df.apply(lambda r: anomaly_type(r), axis=1)

# 5) Save cleaned CSV & anomalies CSV
df.to_csv(CLEAN_OUT, index=False)
df[df['Anomaly_Flag'] == 1].to_csv(ANOM_OUT, index=False)

print("Cleaned file saved to:", CLEAN_OUT)
print("Anomalies saved to:", ANOM_OUT)
print("Total anomalies found:", int(df['Anomaly_Flag'].sum()))

# 6) Load into SQLite
conn = sqlite3.connect(DB_PATH)
df.to_sql('SmartMeter', conn, if_exists='replace', index=False)
conn.close()
print("SQLite DB created at:", DB_PATH)
