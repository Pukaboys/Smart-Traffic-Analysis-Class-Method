import csv, json, random
from datetime import datetime, timedelta


locations = ['Tirana Center','Ring Road','Student City','Blloku','Durres Road','Zogu i Zi','Airport Road','New Boulevard']
weather_opts = ['Clear','Cloudy','Rainy','Foggy']
event_types = ['Normal','Accident','Roadwork','Heavy Traffic']
rows = []
start = datetime(2026, 5, 1)

for i in range(12000):
    ts = start + timedelta(minutes=5*i)
    hour = ts.hour
    loc = random.choice(locations)
    peak = 1.7 if hour in [7,8,9,16,17,18] else 0.8
    count = int(max(20, random.gauss(130*peak, 35)))
    speed = max(8, min(80, random.gauss(58 - count/6, 9)))
    congestion = 'High' if count > 250 or speed < 22 else ('Medium' if count > 150 or speed < 38 else 'Low')
    event = random.choices(event_types, weights=[86,3,4,7])[0]
    rows.append([f'S{locations.index(loc)+1:03d}', loc, ts.strftime('%Y-%m-%d %H:%M:%S'), count, round(speed,1), congestion, random.choice(weather_opts), event])

with open('dataset/traffic_sensor_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['sensor_id','location','timestamp','vehicle_count','average_speed','congestion_level','weather','event_type'])
    writer.writerows(rows)

events = [{'sensor_id': r[0], 'location': r[1], 'event_type': r[7], 'severity': random.choice(['Low','Medium','High']), 'timestamp': r[2]} for r in rows if r[7] != 'Normal'][:12000]
with open('dataset/traffic_events.json', 'w', encoding='utf-8') as f:
    json.dump(events, f, indent=2)
