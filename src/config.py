from pathlib import Path
import random
import os
import numpy as np

# Project identification
PROJECT_NAME = "Predictive Forecasting of Care Load & Placement Demand"

PROJECT_ROOT = Path(__file__).resolve().parent

# Reproducibility
RANDOM_STATE = 42

random.seed(RANDOM_STATE)
np.random.seed(RANDOM_STATE)
os.environ["PYTHONHASHSEED"] = str(RANDOM_STATE)

# Forecasting configuration
TARGET_VARIABLE = "Children in HHS Care"

FORECAST_HORIZONS = [1, 7, 14, 30]

SECONDARY_TARGETS = [
    "Children apprehended and placed in CBP custody*",
    "Children in CBP custody",
    "Children transferred out of CBP custody",
    "Children discharged from HHS Care"
]

DATE_COLUMN = "Date"

# Dataset configuration
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
INTERIM_DATA_DIR = PROJECT_ROOT / "data" / "interim"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
EXTERNAL_DATA_DIR = PROJECT_ROOT / "data" / "external"

DATASET_FILENAME = "HHS_Unaccompanied_Alien_Children_Program(3).csv"

RAW_DATA_PATH = RAW_DATA_DIR / DATASET_FILENAME

# Output directories
OUTPUT_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"
FORECASTS_DIR = OUTPUT_DIR / "forecasts"
REPORTS_DIR = OUTPUT_DIR / "reports"
TABLES_DIR = OUTPUT_DIR / "tables"

# Modeling directories
MODELS_DIR = PROJECT_ROOT / "models"

# Documentation directories
DOCUMENTATION_DIR = PROJECT_ROOT / "documentation"

# Model evaluation metrics
EVALUATION_METRICS = [
    "MAE",
    "RMSE",
    "MAPE",
    "WAPE"
]

# Time-series validation
TEST_SIZE = 0.20
VALIDATION_METHOD = "Chronological Walk-Forward Validation"

# Artifact naming conventions
DATE_FORMAT = "%Y%m%d"
MODEL_ARTIFACT_FORMAT = "model_{model_name}_{target}_{horizon}d.joblib"
FORECAST_ARTIFACT_FORMAT = "forecast_{target}_{horizon}d.csv"

# Ensure output directories exist
for directory in [
    RAW_DATA_DIR,
    INTERIM_DATA_DIR,
    PROCESSED_DATA_DIR,
    EXTERNAL_DATA_DIR,
    FIGURES_DIR,
    FORECASTS_DIR,
    REPORTS_DIR,
    TABLES_DIR,
    MODELS_DIR
]:
    directory.mkdir(parents=True, exist_ok=True)
