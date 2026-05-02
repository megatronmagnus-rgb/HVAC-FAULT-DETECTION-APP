import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.preprocessing import LabelEncoder

# ---------- LOAD DATA (FIXED PATH SAFETY) ----------
df = pd.read_csv("data/ac_fault_dataset_10000.csv")

# ---------- FEATURES & TARGET ----------
X = df.drop("Fault", axis=1)
y = df["Fault"]

# ---------- ENCODER (FIX ADDED) ----------
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# ---------- SPLIT ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# ---------- MODEL ----------
model = RandomForestClassifier(n_estimators=120, random_state=42)
model.fit(X_train, y_train)

# ---------- PREDICTIONS ----------
y_pred = model.predict(X_test)

# ---------- METRICS ----------
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ---------- CONFUSION MATRIX ----------
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6,4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=encoder.classes_,
            yticklabels=encoder.classes_)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.savefig("confusion_matrix.png")

# ---------- SAVE MODEL (FIXED STRUCTURE) ----------
os.makedirs("model", exist_ok=True)

joblib.dump(model, "model/ac_fault_model.pkl")
joblib.dump(encoder, "model/label_encoder.pkl")
joblib.dump(X.columns.tolist(), "model/features.pkl")

print("✅ Model saved as model/ac_fault_model.pkl")
print("✅ Encoder saved as model/label_encoder.pkl")
print("✅ Features saved as model/features.pkl")