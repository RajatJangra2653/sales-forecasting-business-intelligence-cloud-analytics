"""Deterministic demo generator and strict sales data contract."""
import numpy as np
import pandas as pd

REQUIRED = ['date', 'region', 'category', 'units', 'revenue', 'cost']


def demo_data(seed=42):
    rng = np.random.default_rng(seed)
    rows = []
    for i, day in enumerate(pd.date_range('2022-01-01', '2025-12-31')):
        for region, weight in [('North', 1.2), ('South', 1.0), ('West', .85)]:
            for category, price in [('Electronics', 180), ('Home', 65), ('Apparel', 40)]:
                demand = (24 + .008*i + 7*np.sin(2*np.pi*i/365.25)
                          + 5*(day.dayofweek >= 5) + 12*(day.month == 11)) * weight
                units = max(0, int(rng.normal(demand, 5)))
                revenue = round(units * price * rng.uniform(.90, 1.05), 2)
                rows.append((day, region, category, units, revenue, round(revenue*rng.uniform(.55, .78), 2)))
    return pd.DataFrame(rows, columns=REQUIRED)


def validate_data(df):
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise ValueError('Missing columns: ' + ', '.join(sorted(missing)))
    df = df[REQUIRED].copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True).dt.tz_convert(None).dt.normalize()
    for col in ['units', 'revenue', 'cost']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        if not np.isfinite(df[col]).all() or (df[col] < 0).any():
            raise ValueError(f'{col} must contain finite, non-negative numbers.')
    if df.isna().any().any() or any(df[c].astype(str).str.strip().eq('').any() for c in ['region', 'category']):
        raise ValueError('Dates, dimensions and numeric fields cannot be blank or invalid.')
    if df.empty:
        raise ValueError('The dataset is empty.')
    return df.sort_values('date').reset_index(drop=True)


def daily_series(df, missing_as_zero=False):
    series = df.groupby('date')['revenue'].sum().sort_index().asfreq('D')
    if series.isna().any():
        if not missing_as_zero:
            raise ValueError('Missing calendar days. Confirm they represent zero sales using the sidebar option.')
        series = series.fillna(0)
    return series


def load_gcs(bucket, name):
    """Uses Application Default Credentials; never accepts credentials in uploads."""
    import io
    from google.cloud import storage
    blob = storage.Client().bucket(bucket).blob(name)
    if blob.size is None:
        blob.reload()
    if blob.size > 20 * 1024 * 1024:
        raise ValueError('Cloud CSV exceeds the 20 MB limit.')
    return pd.read_csv(io.BytesIO(blob.download_as_bytes()))
