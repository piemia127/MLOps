import mlrun
import pandas as pd
import os
from datetime import datetime, timedelta
import mlrun.feature_store as fstore
from mlrun.feature_store.steps import OneHotEncoder, MapValues, DateExtractor
from mlrun.datastore.targets import RedisNoSqlTarget, ParquetTarget

# Cell 0: Initialize Project
print("=" * 50)
print("Cell 0: Initializing Project")
print("=" * 50)
project = mlrun.get_or_create_project(
    name="fraud-demo",
    context="./",
    user_project=True
)

my_redis_url = "redis://host.docker.internal:6379"
print(f"Using Redis URL: {my_redis_url}")

# Helper Function: Adjust Timestamps
def adjust_data_timespan(df, timestamp_col="timestamp", new_period="2d"):
    if new_period.endswith("d"):
        delta = timedelta(days=int(new_period[:-1]))
    elif new_period.endswith("h"):
        delta = timedelta(hours=int(new_period[:-1]))
    else:
        delta = timedelta(days=2)
    max_time = df[timestamp_col].max()
    now = datetime.now()
    shift = now - max_time - timedelta(minutes=5) 
    df[timestamp_col] = df[timestamp_col] + shift
    start_time = now - delta
    df = df[df[timestamp_col] >= start_time]
    return df

# Cell 1: Transactions Data Ingestion
print("\n" + "=" * 50)
print("Cell 1: Fetching and Ingesting Transactions Data")
print("=" * 50)
print("Fetching transactions data...")
transactions_data = pd.read_csv(
    "https://s3.wasabisys.com/iguazio/data/fraud-demo-mlrun-fs-docs/data.csv",
    parse_dates=["timestamp"]
)

# Preprocess Data (Sort and Adjust Time)
transactions_data = transactions_data.sort_values(by="source", axis=0)[:10000]
transactions_data = adjust_data_timespan(transactions_data, new_period="2d")
transactions_data = transactions_data.sort_values(by="timestamp", axis=0)

# Define FeatureSet
transaction_set = fstore.FeatureSet(
    "transactions",
    entities=[fstore.Entity("source")],
    timestamp_key="timestamp",
    description="transactions feature set"
)

# Define Transformation Graph
main_categories = ["es_transportation", "es_health", "es_otherservices",
       "es_food", "es_hotelservices", "es_barsandrestaurants",
       "es_tech", "es_sportsandtoys", "es_wellnessandbeauty",
       "es_hyper", "es_fashion", "es_home", "es_contents",
       "es_travel", "es_leisure"]

one_hot_encoder_mapping = {
    "category": main_categories,
    "gender": list(transactions_data.gender.unique())
}

transaction_set.graph\
    .to(DateExtractor(parts=["hour", "day_of_week"], timestamp_col="timestamp"))\
    .to(MapValues(mapping={"age": {"U": "0"}}, with_original_features=True))\
    .to(OneHotEncoder(mapping=one_hot_encoder_mapping))

# Add Aggregations
transaction_set.add_aggregation(
    name="amount",
    column="amount",
    operations=["avg", "sum", "count", "max"],
    windows=["2h", "12h", "24h"],
    period="1h"
)

for category in main_categories:
    transaction_set.add_aggregation(
        name=category,
        column=f"category_{category}",
        operations=["sum"],
        windows=["14d"],
        period="1d"
    )

# Ingest with Explicit Targets
print("Ingesting transactions to Redis and Parquet...")
transactions_df = transaction_set.ingest(
    transactions_data,
    infer_options=fstore.InferOptions.default(),
    targets=[
        ParquetTarget(name="parquet", path="./store/transactions"),
        RedisNoSqlTarget(path=my_redis_url)
    ]
)

print("Transactions ingestion done.")
print(f"Transactions DataFrame shape: {transactions_df.shape}")
print(transactions_df.head(3))

# Cell 2: User Events Data Ingestion
print("\n" + "=" * 50)
print("Cell 2: Fetching and Ingesting User Events Data")
print("=" * 50)
print("Fetching user events data...")
user_events_data = pd.read_csv(
    "https://s3.wasabisys.com/iguazio/data/fraud-demo-mlrun-fs-docs/events.csv",
    index_col=0,
    quotechar="'",
    parse_dates=["timestamp"]
)

# Adjust Time
user_events_data = adjust_data_timespan(user_events_data, new_period="2d")

# Define FeatureSet
user_events_set = fstore.FeatureSet(
    "events",
    entities=[fstore.Entity("source")],
    timestamp_key="timestamp",
    description="user events feature set"
)

# Define Graph (Simple OneHot)
events_mapping = {"event": list(user_events_data.event.unique())}
user_events_set.graph.to(OneHotEncoder(mapping=events_mapping))

# Ingest with Explicit Targets
print("Ingesting user events to Redis and Parquet...")
events_df = user_events_set.ingest(
    user_events_data,
    targets=[
        ParquetTarget(name="parquet", path="./store/events"),
        RedisNoSqlTarget(path=my_redis_url)
    ]
)

print("User events ingestion done.")
print(f"Events DataFrame shape: {events_df.shape}")
print(events_df.head(3))

# Cell 3: Labels Ingestion
print("\n" + "=" * 50)
print("Cell 3: Creating and Ingesting Labels")
print("=" * 50)

# Define Label Creation Logic
def create_labels(df):
    labels = df[["fraud", "timestamp"]].copy()
    labels = labels.rename(columns={"fraud": "label"})
    labels["timestamp"] = labels["timestamp"].astype("datetime64[ns]")
    labels["label"] = labels["label"].astype(int)
    return labels

# Define FeatureSet
labels_set = fstore.FeatureSet(
    "labels",
    entities=[fstore.Entity("source")],
    timestamp_key="timestamp",
    description="training labels",
    engine="pandas"
)

labels_set.graph.to(name="create_labels", handler=create_labels)

# Ingest with Explicit Targets (Parquet only)
print("Ingesting labels to Parquet...")
labels_df = labels_set.ingest(
    transactions_data,
    targets=[
        ParquetTarget(name="parquet", path="./store/labels")
    ]
)

print("Labels ingestion done.")
print(f"Labels DataFrame shape: {labels_df.shape}")
print(labels_df.head(3))

# Cell 4: Summary
print("\n" + "=" * 50)
print("Cell 4: Summary")
print("=" * 50)
print("Part 1: Data Ingestion Complete!")
print("-" * 30)
print(f"Transactions stored in: ./store/transactions")
print(f"Events stored in:       ./store/events")
print(f"Labels stored in:       ./store/labels")
print("\n" + "=" * 50)
print("All data ingestion steps completed successfully!")
print("=" * 50)

