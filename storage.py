import pandas as pd

FILE = "tickets.csv"

def save_ticket(data):
    df = pd.DataFrame([data])
    try:
        df_existing = pd.read_csv(FILE)
        df = pd.concat([df, df_existing], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_csv(FILE, index=False)

def load_tickets():
    try:
        df = pd.read_csv(FILE)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df.sort_values(by="timestamp", ascending=False)
    except FileNotFoundError:
        return pd.DataFrame()
