import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
from datetime import datetime
import joblib
import time

# Load model and scaler
rf_model = joblib.load('random_forest_air_quality.pkl')
scaler = joblib.load('scaler_air_quality.pkl')

# Calibration R0 values
mq3_r0 = 17200
mq9_r0 = 21940

# Rs/R0 calculation
def rs_r0(adc, r0, vcc=5.0, rl=5000, adc_vmax=3.3):
    vout = (adc / 4095) * adc_vmax
    if vout == 0:
        return float('inf')
    rs = rl * ((vcc / vout) - 1)
    return rs / r0

# Firebase setup
cred = credentials.Certificate('smell-42bf5-firebase-adminsdk-fbsvc-06651f2cef.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smell-42bf5-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

seen_keys = set()

def infer_from_firebase():
    global seen_keys

    ref = db.reference('/sensor_data')
    all_data = ref.get()

    if not all_data:
        print("No data in Firebase.")
        return

    for key, value in sorted(all_data.items()):
        if key in seen_keys:
            continue  # Skip already processed entries

        try:
            mq3_value = int(value['mq3_value'])
            mq9_value = int(value['mq9_value'])
            timestamp = value['timestamp']
        except (KeyError, ValueError) as e:
            print(f"Skipping invalid entry {key}: {e}")
            continue

        # 🔁 Inference logic (your exact code)
        timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        hour = timestamp_obj.hour

        mq3_rs = rs_r0(mq3_value, mq3_r0)
        mq9_rs = rs_r0(mq9_value, mq9_r0)

        new_data = pd.DataFrame([{
            'mq3_rs_r0': mq3_rs,
            'mq9_rs_r0': mq9_rs,
            'hour': hour
        }])

        new_data_scaled = scaler.transform(new_data)
        prediction = rf_model.predict(new_data_scaled)[0]

        print(f"🕒 {timestamp} | MQ3={mq3_value}, MQ9={mq9_value} => Prediction: {prediction}")

        # Mark as seen
        seen_keys.add(key)

if __name__ == "__main__":
    print("🚀 Listening to Firebase every 10 seconds...")
    while True:
        infer_from_firebase()
        time.sleep(10)  # Match the ESP delay in milliseconds
