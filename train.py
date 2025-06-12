import numpy as np 
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
import joblib

# Load dataset
df = pd.read_csv("dataset.csv")

# Check if all necessary columns are present
assert all(col in df.columns for col in ['mq3_rs_r0', 'mq9_rs_r0', 'hour', 'label']), "Missing columns in dataset"

# Features and target
X = df[['mq3_rs_r0', 'mq9_rs_r0', 'hour']]
y = df['label']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest
rf = RandomForestClassifier(
    n_estimators=300,        
    max_depth=None,          
    min_samples_split=2,     
    random_state=42,
    n_jobs=-1,              
    oob_score=True           
)
rf.fit(X_train_scaled, y_train)

# Evaluate
print("OOB Score (like validation accuracy):", rf.oob_score_)
y_pred = rf.predict(X_test_scaled)
print("Test Set Performance:\n", classification_report(y_test, y_pred))

# Save the model and scaler
joblib.dump(rf, 'random_forest_air_quality.pkl')
joblib.dump(scaler, 'scaler_air_quality.pkl')
