# Technical Documentation

## Forecasting objective

Forecast the daily number of children in HHS care.

Target: `children_in_hhs_care`

Date column: `date`

## Processed dataset

- date
- children_apprehended_and_placed_in_cbp_custody
- children_in_cbp_custody
- children_transferred_out_of_cbp_custody
- children_in_hhs_care
- children_discharged_from_hhs_care

## Forecast horizons

- 1 day
- 7 days
- 14 days
- 30 days

## Modeling workflow

1. Data loading and validation
2. Data cleaning and date handling
3. Time-series continuity assessment
4. Exploratory data analysis
5. Feature engineering
6. Chronological data splitting
7. Baseline forecasting
8. Statistical and machine-learning models
9. Forecast evaluation
10. Uncertainty analysis
11. KPI and scenario analysis
12. Dashboard integration

## Evaluation metrics

- MAE
- RMSE
- MAPE

## Model artifacts

Model artifacts and the model registry are maintained under `models/`.

## Monitoring

Monitoring, drift assessment, retraining criteria and model version
documentation are maintained in the documentation and monitoring outputs.

## Limitations

Forecasts are estimates and should be interpreted with uncertainty.
Final research conclusions and operational decisions require human review.
