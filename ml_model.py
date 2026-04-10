import pandas as pd
from sklearn.ensemble import RandomForestClassifier

model = None


def create_features(df):
    df = df.copy()

    df["cpu_trend"] = df["cpu"].diff()
    df["memory_trend"] = df["memory"].diff()
    df["temp_trend"] = df["temperature"].diff()
    df["power_trend"] = df["power"].diff()

    df["cpu_avg"] = df["cpu"].rolling(5).mean()
    df["memory_avg"] = df["memory"].rolling(5).mean()

    df["cpu_std"] = df["cpu"].rolling(5).std()
    df["memory_std"] = df["memory"].rolling(5).std()

    df = df.fillna(0)

    return df


def label_data(df):
    # Simple labeling (you can improve later)
    df["label"] = 0

    df.loc[(df["cpu"] > 85) & (df["memory"] > 85), "label"] = 1
    df.loc[df["temperature"] > 80, "label"] = 1

    return df


def train_model(df):
    global model

    df = create_features(df)
    df = label_data(df)

    features = [
        "cpu", "memory", "temperature", "power",
        "cpu_trend", "memory_trend", "temp_trend", "power_trend",
        "cpu_avg", "memory_avg",
        "cpu_std", "memory_std"
    ]

    X = df[features]
    y = df["label"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)


def predict(data, df):
    global model

    if model is None:
        return False, "Model not trained"

    df = create_features(df)
    latest = df.iloc[-1]

    features = [
        "cpu", "memory", "temperature", "power",
        "cpu_trend", "memory_trend", "temp_trend", "power_trend",
        "cpu_avg", "memory_avg",
        "cpu_std", "memory_std"
    ]

    X = latest[features].values.reshape(1, -1)

    prediction = model.predict(X)[0]
    prob = model.predict_proba(X)[0][1]

    return prediction == 1, prob