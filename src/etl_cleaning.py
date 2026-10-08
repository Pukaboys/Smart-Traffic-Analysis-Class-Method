import pandas as pd

df = pd.read_csv('dataset/traffic_sensor_data.csv')
df = df.drop_duplicates()
df['vehicle_count'] = pd.to_numeric(df['vehicle_count'], errors='coerce').fillna(0).astype(int)
df['average_speed'] = pd.to_numeric(df['average_speed'], errors='coerce').fillna(df['average_speed'].median())
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df = df.dropna(subset=['timestamp'])
df.to_csv('results/traffic_sensor_cleaned.csv', index=False)
print('Cleaned rows:', len(df))
