import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# -------------------------------
# LOAD DATASET
# -------------------------------
df = pd.read_excel("data/ac_fault_dataset_1500_updated.xlsx")

# -------------------------------
# FEATURES & TARGET
# -------------------------------
X = df[["T1","T2","T3","T4","T5","T6","T7","T8","Power"]]
y = df["Fault"]

# -------------------------------
# SPLIT
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# MODEL
# -------------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -------------------------------
# SAVE MODEL
# -------------------------------
pickle.dump(model, open("model.pkl", "wb"))

print("✅ Model trained and saved as model.pkl")