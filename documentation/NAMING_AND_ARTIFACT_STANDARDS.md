# Project Naming and Artifact Storage Standards

## File Naming

Use lowercase snake_case for Python files and datasets.

## Notebook Naming

Use descriptive notebook names without spaces.

Example:
data_quality_assessment.ipynb

## Dataset Naming

raw_uac_data.csv
cleaned_uac_data.csv
processed_uac_data.csv

## Model Naming

model_<model_name>_<target>_<horizon>d.joblib

## Forecast Naming

forecast_<target>_<horizon>d.csv

## Figure Naming

figure_<description>.png

## Report Naming

report_<description>.pdf

## Artifact Storage

- Raw data: data/raw/
- Intermediate data: data/interim/
- Processed data: data/processed/
- Figures: outputs/figures/
- Forecasts: outputs/forecasts/
- Reports: outputs/reports/
- Tables: outputs/tables/
- Models: models/
- Documentation: documentation/

Raw source data must remain unchanged.
