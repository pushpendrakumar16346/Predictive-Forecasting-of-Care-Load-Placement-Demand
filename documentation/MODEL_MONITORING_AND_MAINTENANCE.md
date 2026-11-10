
# Model Monitoring and Maintenance Procedure

Generated: 2026-11-05 04:33:43

## Monitoring scope

Target variable: children_in_hhs_care

Monitoring should cover:
- Forecast accuracy using MAE, RMSE and MAPE.
- Forecast errors by model and forecast horizon.
- Prediction stability and implausible outputs.
- Data completeness, date continuity and duplicate dates.
- Changes in target distribution.
- Model artifact integrity and version identifiers.

## Monitoring frequency

- Data quality: whenever new data is refreshed.
- Forecast performance: after each evaluation cycle.
- Drift indicators: monthly or after a material data change.
- Model review: monthly and whenever an alert occurs.

## Drift interpretation

- PSI below 0.10: no significant drift indicated.
- PSI from 0.10 to below 0.25: investigate moderate drift.
- PSI 0.25 or higher: significant drift alert.

PSI is a screening indicator, not proof that a model has become inaccurate.

## Retraining criteria

A model review is recommended when:
- Validation MAE or RMSE deteriorates by approximately 20% for two consecutive evaluation periods.
- Significant distribution drift is detected.
- Forecast stability deteriorates.
- Data collection or operational definitions change.

Data quality problems must be resolved before retraining.

## Deployment controls

- Preserve the existing production model until a replacement is validated.
- Record model file hashes and version identifiers.
- Keep chronological validation and test results.
- Compare candidate models with the deployed model and baseline models.
- Record approval and deployment dates.
- Retain rollback capability.

## Important limitation

This document defines the monitoring procedure. It does not establish that continuous automated monitoring or scheduled retraining is running.
