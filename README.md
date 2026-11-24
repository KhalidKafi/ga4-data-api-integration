# GA4 Data API Integration

A Python script that pulls daily active users from Google Analytics 4 through the GA4 Data API, loads the results into a Pandas DataFrame, and exports them to CSV.

Live test site tracked by this project: https://khalidkafi.github.io/ga4-data-api-integration/

## Tech
- Python
- GA4 Data API (Google's official Python client library)
- Google Cloud service account authentication
- Pandas
- GitHub Pages (test site with the GA4 tag)

## How it works
1. `docs/index.html` is a test page hosted on GitHub Pages with the GA4 tag, so real visits are recorded.
2. `ga4_dashboard.py` reads its settings from `.env`, authenticates with a service account, and requests daily active users for the last 30 days.
3. The response is converted into a sorted Pandas DataFrame and saved as `active_users.csv`.

## Setup
1. Create a Google Cloud project and enable the **Google Analytics Data API**.
2. Create a service account and download its JSON key.
3. In GA4, go to Admin, then Property access management, and add the service account's email as a **Viewer**.
4. Copy `.env.example` to `.env` and fill in your key file path and GA4 property ID.
5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Run
```
python ga4_dashboard.py
```

## Error handling
- Missing settings in `.env`: clear message and exit
- Key file not found: clear message and exit
- Failed API request (for example, `PermissionDenied` when the service account has no access to the property): error message and exit
- No data for the date range: message instead of an empty CSV

## Sample output
Sample output will be added once GA4 data is available.

## Security
Credentials are loaded from `.env` and the key file. Both are listed in `.gitignore` and never committed.