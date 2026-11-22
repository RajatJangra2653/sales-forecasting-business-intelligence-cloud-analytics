import unittest
import numpy as np
import pandas as pd
from analytics.data import demo_data, validate_data, daily_series
from analytics.forecast import evaluate, predict, MODELS

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.df = demo_data().iloc[:2700]

    def test_demo_reproducibility(self):
        pd.testing.assert_frame_equal(demo_data(), demo_data())

    def test_invalid_inputs(self):
        for value in [-1, np.inf, np.nan]:
            bad = self.df.copy(); bad.loc[0, 'revenue'] = value
            with self.assertRaises(ValueError): validate_data(bad)
        with self.assertRaises(ValueError): validate_data(self.df.drop(columns='date'))

    def test_missing_dates_require_policy(self):
        data = self.df[self.df.date != pd.Timestamp('2022-01-03')]
        with self.assertRaises(ValueError): daily_series(data)
        self.assertEqual(daily_series(data, True).loc['2022-01-03'], 0)

    def test_seasonal_baseline_repeats_week(self):
        series = daily_series(self.df)
        result = predict(series, 14, MODELS[0])
        np.testing.assert_array_equal(result.iloc[:7], series.iloc[-7:])
        np.testing.assert_array_equal(result.iloc[7:], series.iloc[-7:])

    def test_temporal_splits_and_future(self):
        series = daily_series(self.df)
        winner, comparison, folds, test, scores, future = evaluate(series, 14)
        self.assertEqual(len(folds), 6)
        self.assertEqual(len(test), 14)
        self.assertEqual(future.index.min(), series.index.max()+pd.Timedelta(days=1))
        self.assertTrue((future.lower <= future.forecast).all())
        self.assertTrue((future.upper >= future.forecast).all())
        # Changing only the final holdout cannot change validation or model selection.
        altered = series.copy(); altered.iloc[-14:] *= 20
        other = evaluate(altered, 14)
        self.assertEqual(winner, other[0])
        pd.testing.assert_frame_equal(comparison, other[1])
        self.assertTrue(np.isfinite(scores['MAE']))

    def test_zero_and_short_series(self):
        series = daily_series(self.df)*0
        self.assertTrue(np.isnan(evaluate(series, 7)[4]['WAPE (%)']))
        with self.assertRaises(ValueError): evaluate(series.iloc[:100], 28)

if __name__ == '__main__': unittest.main()
