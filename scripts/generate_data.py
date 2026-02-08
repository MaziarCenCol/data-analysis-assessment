import pandas as pd
import numpy as np
import json
import random
import uuid
from datetime import datetime, timedelta

# Configuration
NUM_USERS = 120
NUM_DEVICES = 450
NUM_EVENTS = 15000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 2, 8)

# Constants
COUNTRIES = ['CA', 'Canada', 'can', 'US', 'USA', 'United States', 'KR', 'JP']
SOURCES = ['iOS', 'Android', 'Web', '3rdParty']
DEVICE_TYPES = {
    'tuya': ['smart_plug', 'smart_bulb', 'heater', 'fan'],
    'ayla': ['thermostat', 'door_sensor', 'window_sensor', 'legrand_switch']
}
FIRMWARE_VERSIONS = ['1.0.0', '1.0.3', '2.1.0', '3.5.beta']

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))

def generate_users():
    users = []
    print(f"Generating {NUM_USERS} users...")
    for _ in range(NUM_USERS):
        users.append({
            'user_id': str(uuid.uuid4())[:8],
            'signup_date': random_date(START_DATE - timedelta(days=365), START_DATE).strftime('%Y-%m-%d'),
            'region': random.choice(COUNTRIES),
            'platform': random.choice(SOURCES)
        })
    # Inject anomalies: Duplicate User
    users.append(users[0])
    return pd.DataFrame(users)

def generate_devices(users_df):
    devices = []
    print(f"Generating {NUM_DEVICES} devices...")
    user_ids = users_df['user_id'].tolist()
    
    for _ in range(NUM_DEVICES):
        network = random.choice(['tuya', 'ayla'])
        device_type = random.choice(DEVICE_TYPES[network])
        
        devices.append({
            'device_id': f"d_{str(uuid.uuid4())[:8]}",
            'user_id': random.choice(user_ids) if random.random() > 0.05 else None, # 5% orphan devices
            'network': network,
            'device_type': device_type,
            'firmware_version': random.choice(FIRMWARE_VERSIONS),
            'location': random.choice(['Home', 'Office', 'Cottage', None])
        })
    return pd.DataFrame(devices)

def generate_tuya_payload(device_type):
    # Tuya typically uses a list of "dps" (data points) or status codes
    if device_type == 'smart_plug':
        return {
            "status": [
                {"code": "switch_1", "value": random.choice([True, False])},
                {"code": "countdown_1", "value": random.randint(0, 100)},
                {"code": "cur_current", "value": random.randint(0, 2000)}, # mA
                {"code": "cur_power", "value": random.randint(0, 300) * 10}, # 0.1W units often
                {"code": "cur_voltage", "value": random.randint(1100, 1250)} # 0.1V units
            ]
        }
    elif device_type == 'smart_bulb':
        return {
             "status": [
                {"code": "switch_led", "value": random.choice([True, False])},
                {"code": "bright_value", "value": random.randint(10, 1000)},
                {"code": "temp_value", "value": random.randint(0, 1000)}
            ]
        }
    else:
         return {"status": [{"code": "generic_state", "value": "online"}]}

def generate_ayla_payload(device_type):
    # Ayla typically uses a property/value structure or metadata wrapper
    dsn = f"AC{str(uuid.uuid4())[:10]}".upper()
    if 'sensor' in device_type:
        return {
            "metadata": {"oem_model": device_type, "dsn": dsn},
            "datapoint": {
                "property": "contact_state",
                "value": random.choice([0, 1]), # 0=closed, 1=open
                "echo": False
            }
        }
    elif 'thermostat' in device_type:
        return {
            "metadata": {"oem_model": "honeywell_t6", "dsn": dsn},
            "datapoint": {
                "property": "local_temperature",
                "value": round(random.uniform(18.0, 26.0), 1),
                "scale": "C"
            }
        }
    else:
        return {
            "metadata": {"dsn": dsn},
            "datapoint": {"property": "connectivity", "value": "connected"}
        }

def generate_events(devices_df):
    events = []
    print(f"Generating {NUM_EVENTS} events...")
    
    # Intentionally picking a few devices to be "spammy" or "broken"
    spam_device = devices_df.iloc[0]['device_id']
    broken_device = devices_df.iloc[1]['device_id'] # Will have voltage spikes
    
    for i in range(NUM_EVENTS):
        # Weighted random choice to simulate spammy device
        if random.random() < 0.1: 
            device = devices_df[devices_df['device_id'] == spam_device].iloc[0]
        else:
            device = devices_df.sample(1).iloc[0]
            
        ts = random_date(START_DATE, END_DATE)
        
        # Generate Payload
        if device['network'] == 'tuya':
            payload = generate_tuya_payload(device['device_type'])
            # Anomaly: Voltage spike for broken device
            if device['device_id'] == broken_device and 'cur_voltage' in str(payload):
                 for item in payload['status']:
                     if item['code'] == 'cur_voltage':
                         item['value'] = 2400 # Spike to 240V!
        else:
            payload = generate_ayla_payload(device['device_type'])
            
        # JSON Formatting anomaly: sometimes it's double-serialized or malformed? 
        # For this exercise, we keep it valid JSON but maybe add some "nulls" in keys in pure random cases
        
        events.append({
            'event_id': f"e_{i}",
            'device_id': device['device_id'],
            'event_type': 'telemetry',
            'event_value': 'see_payload', # Valid legacy field, now useless
            'event_ts': ts.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            'payload': json.dumps(payload)
        })
        
    return pd.DataFrame(events)

# Main Execution
if __name__ == "__main__":
    users_df = generate_users()
    devices_df = generate_devices(users_df)
    events_df = generate_events(devices_df)
    
    # Save to CSV
    print("Saving to CSV...")
    users_df.to_csv('../data/users.csv', index=False)
    devices_df.to_csv('../data/devices.csv', index=False)
    events_df.to_csv('../data/events.csv', index=False)
    
    print("Done! Messy data generated.")
