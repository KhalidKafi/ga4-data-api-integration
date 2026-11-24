import os
import sys

import pandas as pd
from dotenv import load_dotenv
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from google.api_core.exceptions import GoogleAPIError
from google.oauth2 import service_account

OUTPUT_FILE = "active_users.csv"


def load_config():
    """Read the key file path and GA4 property ID from .env."""
    load_dotenv()
    key_path = os.getenv("GA4_KEY_PATH")
    property_id = os.getenv("GA4_PROPERTY_ID")

    if not key_path or not property_id:
        sys.exit("Error: set GA4_KEY_PATH and GA4_PROPERTY_ID in your .env file.")
    if not os.path.exists(key_path):
        sys.exit(f"Error: key file not found: {key_path}")

    return key_path, property_id


def fetch_report(key_path, property_id, start_date="30daysAgo", end_date="today"):
    """Call the GA4 Data API for daily active users."""
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = BetaAnalyticsDataClient(credentials=credentials)

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )

    try:
        return client.run_report(request)
    except GoogleAPIError as e:
        sys.exit(f"Error: GA4 request failed: {e}")


def to_dataframe(response):
    """Turn the API response into a sorted Pandas DataFrame."""
    rows = [
        {
            "date": row.dimension_values[0].value,
            "active_users": int(row.metric_values[0].value),
        }
        for row in response.rows
    ]
    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    return df.sort_values("date").reset_index(drop=True)


def main():
    key_path, property_id = load_config()
    response = fetch_report(key_path, property_id)
    df = to_dataframe(response)

    if df.empty:
        print("No data for this date range yet.")
        return

    df.to_csv(OUTPUT_FILE, index=False)
    print(df.to_string(index=False))
    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()