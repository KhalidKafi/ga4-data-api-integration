from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric, Dimension
from google.oauth2 import service_account

import os
from dotenv import load_dotenv

load_dotenv()
key_path = os.getenv("GA4_KEY_PATH")
property_id = os.getenv("GA4_PROPERTY_ID")

# Path to your downloaded credentials file
credentials = service_account.Credentials.from_service_account_file(
    key_path
)

client = BetaAnalyticsDataClient(credentials=credentials)

request = RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[Dimension(name="date")],
    metrics=[Metric(name="activeUsers")],
    date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
)

response = client.run_report(request)

print("GA4 Active Users Report (last 7 days):")
for row in response.rows:
    print(row.dimension_values[0].value, "->", row.metric_values[0].value, "active users")