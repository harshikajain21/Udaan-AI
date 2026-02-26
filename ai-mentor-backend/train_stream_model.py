import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report


df = pd.read_csv("data/stream_training_data.csv")

X = df.drop("label", axis=1)
y = df["label"]

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=200)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "models/stream_model.pkl")
joblib.dump(encoder, "models/stream_encoder.pkl")