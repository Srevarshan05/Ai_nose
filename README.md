AI for Smell Detection – Smart Sanitation Monitoring System
Overview
This project develops an IoT-based solution to monitor restroom air quality in real-time, using MQ-3 and MQ-9 gas sensors interfaced with an ESP32 microcontroller. Sensor data is stored in Firebase Realtime Database and processed by a Random Forest Classifier to classify air quality into four categories: Clean, Mild, Foul, and Very Foul. The system triggers timely cleaning alerts, enhancing hygiene and user experience in public facilities. Developed as part of an AICTE internship, it leverages skills from Azure AI, generative AI, and responsible AI practices.
Features

Real-Time Monitoring: Captures MQ-3 (VOCs/alcohol) and MQ-9 (methane/CO) sensor data every second.
Cloud Integration: Stores data in Firebase Realtime Database for scalable access.
AI Classification: Random Forest model predicts air quality with ~92% accuracy on synthetic data.
IoT Deployment: ESP32 ensures low-latency data collection and transmission.
Scalable Design: Ready for Azure cloud deployment and smart city applications.

Project Structure
├── data/
│   ├── synthetic_sensor_data.json  # Synthetic dataset in Firebase format
│   ├── synthetic_sensor_data.csv   # Dataset with features and labels
├── scripts/
│   ├── generate_synthetic_dataset.py  # Generates synthetic dataset
│   ├── train_random_forest.py        # Trains Random Forest model
├── firmware/
│   ├── esp32_firebase.ino           # ESP32 sketch for sensor data collection
├── models/
│   ├── random_forest_air_quality.pkl # Trained Random Forest model
│   ├── scaler_air_quality.pkl        # Feature scaler
├── README.md                        # Project documentation

Requirements

Hardware:

ESP32 Dev Module
MQ-3 Gas Sensor (Alcohol/VOCs)
MQ-9 Gas Sensor (Methane/CO)
5V Power Supply
100nF Capacitor (for sensor stability)


Software:

Arduino IDE (for ESP32 firmware)
Python 3.8+ with libraries: numpy, pandas, scikit-learn, joblib
Firebase Realtime Database account


Dependencies:
pip install numpy pandas scikit-learn joblib



Installation

Clone the Repository:
git clone https://github.com/<your-username>/smart-sanitation-monitoring.git
cd smart-sanitation-monitoring


Set Up Firebase:

Create a Firebase project at console.firebase.google.com.
Enable Realtime Database and copy the database URL.
Generate a private key JSON file for authentication.


Configure ESP32:

Install Arduino IDE and ESP32 board support.

Open firmware/esp32_firebase.ino.

Update WiFi credentials and Firebase details:
#define WIFI_SSID "SREVARSHAN AIRTEL"
#define WIFI_PASSWORD "9600622497"
#define FIREBASE_HOST "<your-firebase-database-url>"
#define FIREBASE_AUTH "<your-firebase-auth-token>"


Connect MQ-3 (AOUT → GPIO 34) and MQ-9 (AOUT → GPIO 35), VCC to 5V, GND with 100nF capacitor.

Upload the sketch to ESP32.



Install Python Dependencies:
pip install -r requirements.txt

(Create requirements.txt with listed dependencies.)


Usage

Generate Synthetic Dataset:
python scripts/generate_synthetic_dataset.py


Outputs data/synthetic_sensor_data.json (Firebase format) and data/synthetic_sensor_data.csv (features: mq3_rs_r0, mq9_rs_r0, hour).


Train Random Forest Model:
python scripts/train_random_forest.py


Trains on synthetic_sensor_data.csv, saves random_forest_air_quality.pkl and scaler_air_quality.pkl in models/.
Reports ~92% accuracy on test set.


Run ESP32 for Data Collection:

Power ESP32 with sensors preheated (48 hours, 5V).
Data streams to Firebase every second.


Inference:

Use trained model for predictions:
import joblib
import pandas as pd
rf = joblib.load('models/random_forest_air_quality.pkl')
scaler = joblib.load('models/scaler_air_quality.pkl')
new_data = pd.DataFrame({'mq3_rs_r0': [0.3], 'mq9_rs_r0': [0.2], 'hour': [18]})
new_data_scaled = scaler.transform(new_data)
prediction = rf.predict(new_data_scaled)
print(prediction)  # e.g., 'Foul'





Dataset

Synthetic Dataset: 1000 samples (250 per class: Clean, Mild, Foul, Very Foul).
Features: mq3_rs_r0 (MQ-3 VOCs), mq9_rs_r0 (MQ-9 methane), hour (time-of-day).
Source: Generated via generate_synthetic_dataset.py, mimicking observed ADC ranges:
Clean: MQ-3: 1200–1600, MQ-9: 1000–1300
Very Foul: MQ-3: 1500–3000, MQ-9: 2500–3500


Real Data: 78 samples (2025-06-09, Firebase export) used for calibration (MQ-3 R0 ≈ 17.20kΩ, MQ-9 R0 ≈ 21.94kΩ).

Model Details

Algorithm: Random Forest Classifier (n_estimators=100, random_state=42).
Training: 80/20 stratified split, StandardScaler for feature normalization.
Performance: ~92% accuracy on synthetic test set.
Output: Classifies air quality (Clean, Mild, Foul, Very Foul) for sanitation alerts.

Challenges

Sensor Calibration: High clean air ADC (MQ-3: 1286–1601, MQ-9: 1063–1228) due to incomplete preheating (48 hours needed).
Alcohol Test Anomalies: MQ-3 max 1459 (expected >2000), MQ-9 max 2873 (unexpected), suggesting pin swap or diluted vapor.
Limited Real Data: Relied on synthetic data due to insufficient restroom samples.

Future Enhancements

Integrate MQ-137 sensor for ammonia detection.
Implement edge AI on ESP32 for offline predictions.
Develop predictive maintenance with time-series analysis.
Create IoT dashboard for real-time monitoring.
Expand to hospitals and schools for broader hygiene applications.

References

Hanwei Electronics. (2023). MQ-3 & MQ-9 Gas Sensor Datasheets.
Firebase. (2025). Firebase Realtime Database Documentation.
Breiman, L. (2001). Random Forests. Machine Learning Journal.
Microsoft Azure. (2024). Azure IoT Solutions Guide.
World Health Organization. (2023). Sanitation and Hygiene Guidelines.

License
MIT License. See LICENSE for details.
Acknowledgements

AICTE Internship for project support.
Mentors for guidance on IoT and AI integration.
Azure AI courses for cloud and ethical AI insights.

Contact

GitHub: https://github.com/Srevarshan05
Email:srevarshan9600622@gmail.com

