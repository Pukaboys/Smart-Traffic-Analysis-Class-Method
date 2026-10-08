import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("dataset/traffic_sensor_data.csv")

df = df.rename(columns={
    "sensor_id": "Sensor_ID",
    "location": "Location",
    "timestamp": "Timestamp",
    "date": "Date",
    "hour": "Hour",
    "vehicle_count": "Vehicle_Count",
    "average_speed": "Average_Speed",
    "weather": "Weather",
    "event_type": "Event_Type",
    "congestion_level": "Congestion_Level"
})

print("Missing values per column:")
print(df.isnull().sum())

df = df.dropna(subset=["Sensor_ID", "Location"])

if "Timestamp" in df.columns:
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df["Date"] = df["Timestamp"].dt.date
    df["Hour"] = df["Timestamp"].dt.hour

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

df["Vehicle_Count"] = pd.to_numeric(df["Vehicle_Count"], errors="coerce")
df["Average_Speed"] = pd.to_numeric(df["Average_Speed"], errors="coerce")

df["Vehicle_Count"] = df["Vehicle_Count"].fillna(df["Vehicle_Count"].median())
df["Average_Speed"] = df["Average_Speed"].fillna(df["Average_Speed"].mean())
df["Weather"] = df["Weather"].fillna("Unknown")
df["Event_Type"] = df["Event_Type"].fillna("Normal")

df["Traffic_Intensity"] = df["Vehicle_Count"] / df["Average_Speed"]

df["Speed_Category"] = np.where(df["Average_Speed"] < 30, "Slow", "Normal")

df["Traffic_Status"] = np.where(
    df["Vehicle_Count"] > 200,
    "High Traffic",
    "Normal Traffic"
)

df["Accident_Flag"] = np.where(df["Event_Type"] == "Accident", 1, 0)

print("Transformed Data:")
print(df.head())

location_summary = df.groupby("Location").agg({
    "Vehicle_Count": "sum",
    "Average_Speed": "mean",
    "Accident_Flag": "sum"
})

congestion_summary = df.groupby("Congestion_Level").agg({
    "Sensor_ID": "count",
    "Vehicle_Count": "mean"
})

weather_summary = df.groupby("Weather").agg({
    "Average_Speed": "mean",
    "Vehicle_Count": "sum"
})

hourly_traffic_summary = df.groupby("Hour").agg({
    "Vehicle_Count": "sum"
})

location_summary = location_summary.rename(columns={
    "Vehicle_Count": "Total_Vehicle_Count",
    "Average_Speed": "Average_Speed",
    "Accident_Flag": "Total_Accidents"
})

congestion_summary = congestion_summary.rename(columns={
    "Sensor_ID": "Record_Count",
    "Vehicle_Count": "Average_Vehicle_Count"
})

weather_summary = weather_summary.rename(columns={
    "Average_Speed": "Average_Speed",
    "Vehicle_Count": "Total_Vehicle_Count"
})

hourly_traffic_summary = hourly_traffic_summary.rename(columns={
    "Vehicle_Count": "Total_Vehicle_Count"
})

print("\nTraffic Summary by Location:")
print(location_summary)

print("\nTraffic Summary by Congestion Level:")
print(congestion_summary)

print("\nTraffic Summary by Weather:")
print(weather_summary)

print("\nHourly Traffic Summary:")
print(hourly_traffic_summary)

location_summary.to_csv("results/location_summary.csv")
congestion_summary.to_csv("results/congestion_summary.csv")
weather_summary.to_csv("results/weather_summary.csv")
hourly_traffic_summary.to_csv("results/hourly_traffic_summary.csv")

plt.figure()
location_summary["Total_Vehicle_Count"].plot(kind="bar")
plt.title("Total Vehicles by Location")
plt.xlabel("Location")
plt.ylabel("Total Vehicles")
plt.tight_layout()
plt.savefig("dashboard/vehicles_by_location.png")
plt.show()

plt.figure()
location_summary["Average_Speed"].plot(kind="bar")
plt.title("Average Speed by Location")
plt.xlabel("Location")
plt.ylabel("Average Speed")
plt.tight_layout()
plt.savefig("dashboard/avg_speed_by_location.png")
plt.show()

plt.figure()
df["Congestion_Level"].value_counts().plot(kind="bar")
plt.title("Congestion Level Distribution")
plt.xlabel("Congestion Level")
plt.ylabel("Number of Records")
plt.tight_layout()
plt.savefig("dashboard/congestion_distribution.png")
plt.show()

plt.figure()
plt.plot(hourly_traffic_summary.index, hourly_traffic_summary["Total_Vehicle_Count"])
plt.title("Hourly Traffic Trend")
plt.xlabel("Hour")
plt.ylabel("Total Vehicles")
plt.tight_layout()
plt.savefig("dashboard/traffic_by_hour.png")
plt.show()

plt.figure()
plt.hist(df["Vehicle_Count"])
plt.title("Distribution of Vehicle Count")
plt.xlabel("Vehicle Count")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("dashboard/vehicle_count_distribution.png")
plt.show()

plt.figure()
plt.scatter(df["Average_Speed"], df["Vehicle_Count"])
plt.title("Average Speed vs Vehicle Count")
plt.xlabel("Average Speed")
plt.ylabel("Vehicle Count")
plt.tight_layout()
plt.savefig("dashboard/speed_vs_vehicle_count.png")
plt.show()