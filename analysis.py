import pandas as pd


# ----------------------------
# Basic aggregations
# ----------------------------
def detect_trends(df: pd.DataFrame):
    return df["category"].value_counts()


def detect_drift(df: pd.DataFrame, recent_window=10):
    recent = df.head(recent_window)
    return recent["category"].value_counts()


# ----------------------------
# Advanced analytics
# ----------------------------
def ticket_volume_over_time(df: pd.DataFrame, freq="D"):
    return (
        df.set_index("timestamp")
          .resample(freq)
          .size()
    )


def urgency_distribution(df: pd.DataFrame):
    return df["urgency"].value_counts(normalize=True)


def category_shift(df: pd.DataFrame, split_days=2):
    cutoff = df["timestamp"].max() - pd.Timedelta(days=split_days)

    recent = df[df["timestamp"] > cutoff]
    past = df[df["timestamp"] <= cutoff]

    return (
        recent["category"].value_counts()
        .subtract(past["category"].value_counts(), fill_value=0)
        .sort_values(ascending=False)
    )


def new_categories_detected(df: pd.DataFrame):
    return (
        df.groupby("category")["timestamp"]
          .min()
          .sort_values(ascending=False)
    )


def confidence_trend(df: pd.DataFrame, freq="D"):
    return (
        df.set_index("timestamp")["confidence"]
          .resample(freq)
          .mean()
    )


def issue_complexity_trend(df: pd.DataFrame, freq="D"):
    df = df.copy()
    df["explanation_length"] = df["explanation"].str.len()

    return (
        df.set_index("timestamp")["explanation_length"]
          .resample(freq)
          .mean()
    )
