# Research methodology and dissertation guide

## Research question
Can calendar and lag-based machine learning improve daily revenue forecasts over a weekly seasonal baseline while supporting reproducible, cloud-hosted BI?

## Objectives and implemented scope
1. Validate and aggregate sales data into a daily revenue series.
2. Explore revenue, cost, margin, region, category and calendar patterns.
3. Compare three reproducible algorithms with chronological validation.
4. Serve interactive BI and forecast exports with optional Google Cloud Storage ingestion.
5. Package the system for container deployment and document limitations.

## Experimental design
For N daily observations and forecast horizon H, validation fold 1 trains on [0, N−3H) and evaluates [N−3H, N−2H). Fold 2 trains on [0, N−2H) and evaluates [N−2H, N−H). Select the model with lowest mean validation MAE. Fit that model on [0, N−H) and evaluate once on the final H observations. Finally refit on all observations to predict the future. Require at least 90 training days in the first fold.

The calendar ridge model uses standardized trend, annual sine/cosine, weekday indicators, a November indicator, lags 1/7/14/28 and trailing means 7/28. The November indicator reflects the demo generator and must be justified or reconsidered for real datasets. Gradient boosting uses the same inputs. Future lag features are constructed recursively from earlier predictions. Scaling and fitting occur only inside each training window. Hyperparameters are fixed, not tuned against the final test.

MAE = mean absolute error. RMSE = square root of mean squared error. WAPE = 100 × total absolute error / total actual revenue. WAPE is undefined for zero total actual revenue; the app displays NaN. Metrics are in original currency except WAPE. The naive model repeats the most recent observed week. Compare all models against this baseline before claiming improvement.

The empirical band uses the pooled validation absolute-error 90th percentile. Dependence, horizon effects, small calibration samples and distribution shift prevent guaranteed coverage. It is not a calibrated probabilistic model. Add horizon-specific rolling calibration and coverage reporting for stronger uncertainty research.

## Data and ethics
Demo data contain 13,149 rows covering 2022–2025 with seed 42, trend, annual patterns, weekend effects and noise. It is synthetic, contains no customer data, and must never be presented as company observations. A convincing dissertation needs a licensed real dataset, provenance, a data dictionary, clear currency and cost semantics, and a documented observation window. Repeated input rows are retained; deduplicate using business identifiers upstream if appropriate. Refunds and negative revenue are currently unsupported. Missing days require explicit confirmation before filling with zeros.

## Suggested dissertation structure
- Introduction: problem, business motivation, objectives and research questions.
- Literature review: time-series baselines, machine learning, BI and cloud analytics, using verified academic references.
- Design: architecture, data schema, algorithms, security and experimental controls.
- Implementation: modules, dashboard, storage connector and hosting workflow.
- Evaluation: real-dataset provenance, fold dates, MAE/RMSE/WAPE tables, baseline improvements, runtime and resource cost measurements.
- Discussion: errors by season/segment, sensitivity to horizon, operational constraints and threats to validity.
- Conclusion: findings supported by measured evidence and future work.

## Threats to validity and extensions
The demo generator favors its known calendar structure. Two validation folds give limited evidence. Filters change the learning problem; avoid choosing filters after looking at final test accuracy. Long recursive horizons can accumulate error. External drivers, stockouts and promotions are absent. Segment forecasts do not reconcile to a hierarchy. The app has no built-in user accounts, persistent forecast registry, scheduled retraining or drift alarms. Future work can add SARIMA/Prophet, probabilistic models, more rolling folds, real drivers, warehouse ingestion and scheduled batch scoring. These are proposed extensions, not implemented features.
