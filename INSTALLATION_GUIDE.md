# Installation Guide

## Requirements

- Windows 10 or later
- Python
- Anaconda or Miniconda
- Jupyter Notebook
- Streamlit

## Open the project

```powershell
cd "C:\Users\hp\Predictive Forecasting of Care Load & Placement Demand"
```

## Activate the deployment environment

```powershell
.\.deployment_test_env\Scripts\Activate.ps1
```

If the environment does not exist, create one:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For deployment dependencies, use:

```powershell
pip install -r requirements-deployment.txt
```

## Start Jupyter

```powershell
jupyter notebook
```

## Start the dashboard

```powershell
python -m streamlit run app.py
```

Run commands from the project root.
