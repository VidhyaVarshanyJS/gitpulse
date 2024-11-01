import os
import pandas as pd

CSV_FILE_PATH = "repo_metrics.csv"

def load_csv_data():
    """Load existing CSV data if the file exists, otherwise return an empty DataFrame."""
    if os.path.exists(CSV_FILE_PATH):
        return pd.read_csv(CSV_FILE_PATH)
    else:
        # Return an empty dataframe with predefined columns if the file doesn't exist
        return pd.DataFrame(columns=["username", "repo_name", "metrics"])

def store_data_to_csv(username, repo_name, metrics_df):
    """Store user, repo, and metrics data in the CSV, avoiding duplicates."""
    # Load existing data
    df = load_csv_data()

    # Check if the entry already exists (avoiding duplicates)
    if not ((df["username"] == username) & (df["repo_name"] == repo_name)).any():
        # If the combination does not exist, append new entry
        new_entry = {
            "username": username,
            "repo_name": repo_name,
            "metrics": metrics_df.to_json()  # Store the metrics as a JSON string for simplicity
        }
        df = df._append(new_entry, ignore_index=True)

        # Save the updated DataFrame back to the CSV
        df.to_csv(CSV_FILE_PATH, index=False)
        return f"Data for {repo_name} has been stored successfully."
    else:
        return f"Data for {repo_name} already exists in the CSV file."
