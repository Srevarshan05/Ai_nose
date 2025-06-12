Smart Sanitation Monitoring System 🌬️

A real-time IoT solution for monitoring restroom air quality using MQ-3 and MQ-9 sensors, ESP32, Firebase, and a Random Forest Classifier. 🚽
Description 📝
The Smart Sanitation Monitoring System uses IoT and AI to detect and classify restroom odors, ensuring timely cleaning for enhanced hygiene. MQ-3 (VOCs/alcohol) and MQ-9 (methane/CO) sensors connected to an ESP32 collect real-time quality air data, streamed to Firebase Realtime Database for analysis. A Random Forest Classifier, trained on a synthetic dataset, categorizes air quality as Clean, Mild, Foul, or VeryFoul** with ~95% accuracy, triggering maintenance alerts.Developed during an AICTE internship, the project applies Azure AI, generative AI, and responsible AI principles.
Features ✨

Real-Time Odor Detection: Monitors VOCs and methane in real-time with every second.  
Cloud Storage: Stores sensor data in Firebase for scalable analysis.  
AI-Powered: Predicts air quality with Random Forest Classifier (~92% accuracy).  
Scalable IoT Design: ESP32 enables low-cost, efficient deployment.  
Sanitation Alerts: Facilitates proactive restroom maintenance.

Installation 🛠️
Prerequisites

Hardware:
ESP32 Dev Module
MQ-3 and MQ-9 Gas Sensors
5V Power Supply
100nF Capacitor (for sensor stability)


Software:
Arduino IDE
Python 3.8+
Firebase Realtime Database account


Python Libraries:pip install numpy pandas scikit-learn joblib



Setup

Clone the Repository:git clone https://github.com/<your-username>/smart-sanitation-monitoring.git
cd smart-sanitation-monitoring


Configure Firebase:
Create a project at Firebase Console.
Enable Realtime Database and note the database URL.
Generate a private key JSON for authentication.


Set Up ESP32:
Install Arduino IDE and ESP32 board support.
Open firmware/esp32_firebase.ino.
Update credentials:#define WIFI_SSID "SREVARSHAN AIRTEL"
#define WIFI_PASSWORD "9600622497"
#define FIREBASE_HOST "<your-firebase-database-url>"
#define FIREBASE_AUTH "<your-firebase-auth-token>"


Connect MQ-3 (AOUT → GPIO 34), MQ-9 (AOUT → GPIO 35), VCC to 5V, GND with capacitor.
Upload the sketch.


Install Python Dependencies:pip install -r requirements.txt



Usage 🚀

Generate Synthetic Dataset:python scripts/generate_synthetic_dataset.py


Creates data/synthetic_sensor_data.json and data/synthetic_sensor_data.csv.


Train the Model:python scripts/train_random_forest.py


Outputs models/random_forest_air_quality.pkl and models/scaler_air_quality.pkl.


Collect Real-Time Data:
Run ESP32 with preheated sensors (48 hours, 5V).
Data streams to Firebase.


Predict Air Quality:import joblib, pandas as pd
rf = joblib.load('models/random_forest_air_quality.pkl')
scaler = joblib.load('models/scaler_air_quality.pkl')
data = pd.DataFrame({'mq3_rs_r0': [0.3], 'mq9_rs_r0': [0.2], 'hour': [18]})
prediction = rf.predict(scaler.transform(data))
print(prediction)  # e.g., 'Foul'



Project Structure 📂
smart-sanitation-monitoring/
├── data/
│   ├── synthetic_sensor_data.json  # Firebase-format dataset
│   └── synthetic_sensor_data.csv   # Features and labels
├── firmware/
│   └── esp32_firebase.ino          # ESP32 firmware
├── models/
│   ├── random_forest_air_quality.pkl  # Trained model
│   └── scaler_air_quality.pkl        # Feature scaler
├── scripts/
│   ├── generate_synthetic_dataset.py  # Dataset generation
│   └── train_random_forest.py      # Model training
├── requirements.txt               # Python dependencies
└── README.md                    # Project README

Dataset 📊

Synthetic Dataset: 1000 samples (250 per class: Clean, Mild, Foul, Very Foul).
Features: mq3_rs_r0 (VOCs), mq9_rs_r0 (methane), hour (time).
Purpose: Simulates restroom conditions due to limited real data.
Real Data: 78 samples (2025-06-09) informed calibration.

Model Details 🤖

Algorithm: Random Forest Classifier (n_estimators=100).
Training: 80/20 split, feature scaling.
Accuracy: ~95% on synthetic test set.
Classes: Clean, Mild, Foul, Very Foul.

Challenges ⚠️

Calibration: High clean air ADC required 48-hour sensor preheating.
Data Limitation: Relied on synthetic data due to sparse real samples.
Sensor Sensitivity: MQ-3/MQ-9 miss ammonia, limiting odor detection.

Future Scope 🔮

Add MQ-137 sensor for ammonia detection.
Implement edge AI on ESP32.
Develop predictive maintenance models.
Create real-time IoT dashboard.
Expand to hospitals and schools.

Contributing 🤝
Contributions are welcome! Please:

Fork the repository.
Create a feature branch (git checkout -b feature/YourFeature).
Commit changes (git commit -m 'Add YourFeature').
Push to the branch (git push origin feature/YourFeature).
Open a Pull Request.

License 📜
Distributed under the MIT License
