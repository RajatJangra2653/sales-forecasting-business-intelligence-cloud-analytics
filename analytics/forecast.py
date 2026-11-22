"""Recursive forecasts with chronological validation and an untouched final test."""
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

MODELS = ['Weekly seasonal naive', 'Calendar ridge', 'Lag gradient boosting']


def features(day, history):
    return [day.toordinal()/365.25, np.sin(2*np.pi*day.dayofyear/365.25),
            np.cos(2*np.pi*day.dayofyear/365.25), *[int(day.dayofweek == j) for j in range(7)],
            int(day.month == 11), history[-1], history[-7], history[-14], history[-28],
            np.mean(history[-7:]), np.mean(history[-28:])]


def predict(train, horizon, model):
    if len(train) < 90:
        raise ValueError('Each training window needs at least 90 daily observations.')
    dates = pd.date_range(train.index[-1]+pd.Timedelta(days=1), periods=horizon)
    history = list(train.values)
    estimator = None
    if model != MODELS[0]:
        x = np.array([features(train.index[i], history[:i]) for i in range(28, len(train))])
        y = train.values[28:]
        estimator = (make_pipeline(StandardScaler(), Ridge(alpha=10)) if model == MODELS[1]
                     else HistGradientBoostingRegressor(max_iter=100, max_leaf_nodes=15,
                                                       l2_regularization=5, random_state=42))
        estimator.fit(x, y)
    values = []
    for day in dates:
        value = history[-7] if estimator is None else estimator.predict([features(day, history)])[0]
        value = max(0., float(value))
        values.append(value)
        history.append(value)
    return pd.Series(values, index=dates)


def metrics(actual, predicted):
    a, p = np.asarray(actual), np.asarray(predicted)
    return {'MAE': float(np.mean(abs(a-p))), 'RMSE': float(np.sqrt(np.mean((a-p)**2))),
            'WAPE (%)': float(100*np.sum(abs(a-p))/np.sum(abs(a))) if np.sum(abs(a)) else np.nan}


def evaluate(series, horizon=28):
    # Two validation folds select the model; a later third fold is untouched until selection.
    if len(series) < 90 + 3*horizon:
        raise ValueError(f'Need at least {90+3*horizon} consecutive days for this horizon.')
    records, residuals = [], {m: [] for m in MODELS}
    for model in MODELS:
        for fold, end in enumerate([len(series)-2*horizon, len(series)-horizon], 1):
            train = series.iloc[:end-horizon]
            actual = series.iloc[end-horizon:end]
            prediction = predict(train, horizon, model)
            records.append({'model': model, 'fold': fold, **metrics(actual, prediction)})
            residuals[model].extend(abs(actual.values-prediction.values))
    folds = pd.DataFrame(records)
    comparison = folds.groupby('model')[['MAE', 'RMSE', 'WAPE (%)']].mean().sort_values('MAE')
    winner = comparison.index[0]
    test = series.iloc[-horizon:]
    test_prediction = predict(series.iloc[:-horizon], horizon, winner)
    test_frame = pd.DataFrame({'actual': test, 'predicted': test_prediction})
    radius = float(np.quantile(residuals[winner], .90))
    forecast = predict(series, horizon, winner).rename('forecast').to_frame()
    forecast['lower'] = np.maximum(0, forecast['forecast']-radius)
    forecast['upper'] = forecast['forecast']+radius
    return winner, comparison, folds, test_frame, metrics(test, test_prediction), forecast
