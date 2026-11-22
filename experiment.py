"""Reproducible command-line experiment, independent of the dashboard."""
import argparse
import json
from pathlib import Path
import pandas as pd
from analytics.data import demo_data, validate_data, daily_series
from analytics.forecast import evaluate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', help='Optional real sales CSV; otherwise uses synthetic demo')
    parser.add_argument('--horizon', type=int, choices=[7, 14, 28, 56], default=28)
    parser.add_argument('--output', default='results')
    parser.add_argument('--missing-as-zero', action='store_true')
    args = parser.parse_args()
    data = validate_data(pd.read_csv(args.csv) if args.csv else demo_data())
    series = daily_series(data, args.missing_as_zero)
    winner, comparison, folds, holdout, scores, forecast = evaluate(series, args.horizon)
    output = Path(args.output); output.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(output/'model_comparison.csv')
    folds.to_csv(output/'validation_folds.csv', index=False)
    holdout.to_csv(output/'holdout.csv', index_label='date')
    forecast.to_csv(output/'forecast.csv', index_label='date')
    summary = {'data_source': args.csv or 'SYNTHETIC DEMO (seed 42)',
               'horizon_days': args.horizon, 'first_date': str(series.index.min().date()),
               'last_date': str(series.index.max().date()), 'selected_model': winner,
               'holdout_metrics': {k: None if pd.isna(v) else v for k, v in scores.items()}}
    (output/'summary.json').write_text(json.dumps(summary, indent=2, allow_nan=False)+'\n')
    print(json.dumps(summary, indent=2, allow_nan=False))

if __name__ == '__main__': main()
