from pathlib import Path
import warnings
import html

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


# ---------------------------------------------------------
# Application configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Care Load and Placement Demand Forecasting",
    page_icon="📊",
    layout="wide"
)

ROOT = Path(__file__).resolve().parent

DATA_PATH = (
    ROOT / "data" / "processed" / "cleaned_care_data.csv"
)

OUTPUTS_PATH = ROOT / "outputs"

TARGET_COLUMN = "children_in_hhs_care"
DATE_COLUMN = "date"

FORECAST_HORIZONS = [1, 7, 14, 30]

st.title("Care Load and Placement Demand Forecasting")

st.caption(
    "Historical monitoring, predictive forecasting, "
    "capacity and surge risk, and scenario comparison."
)


# ---------------------------------------------------------
# Data loading
# ---------------------------------------------------------

@st.cache_data
def load_data(file_path, modified_time):
    df = pd.read_csv(file_path)

    if DATE_COLUMN not in df.columns:
        raise ValueError(
            "The dataset must contain a date column."
        )

    df[DATE_COLUMN] = pd.to_datetime(
        df[DATE_COLUMN],
        errors="coerce"
    )

    df = df.dropna(
        subset=[DATE_COLUMN]
    ).sort_values(DATE_COLUMN)

    for column in df.columns:
        if column != DATE_COLUMN:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


@st.cache_data
def load_csv(file_path, modified_time):
    return pd.read_csv(file_path)


def discover_csv_files(folder):
    folder = Path(folder)

    if not folder.exists():
        return []

    return sorted(folder.rglob("*.csv"))


def load_output_records():
    records = []

    for file_path in discover_csv_files(OUTPUTS_PATH):
        try:
            df = load_csv(
                str(file_path),
                file_path.stat().st_mtime
            )

            records.append({
                "name": file_path.name,
                "path": file_path,
                "data": df
            })

        except Exception as error:
            warnings.warn(
                f"Unable to load {file_path.name}: {error}"
            )

    return records


def find_records(records, keywords):
    return [
        record
        for record in records
        if any(
            keyword.lower() in record["name"].lower()
            for keyword in keywords
        )
    ]


def find_date_column(df):
    candidates = [
        "date",
        "Date",
        "ds",
        "timestamp",
        "forecast_date",
        "target_date"
    ]

    for column in candidates:
        if column in df.columns:
            return column

    return None


def get_numeric_columns(df):
    return df.select_dtypes(
        include=np.number
    ).columns.tolist()


def display_table(df):
    if df is None or df.empty:
        st.info("No data available.")
    else:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


def csv_download(df, filename, label):
    if df is None or df.empty:
        return

    st.download_button(
        label=label,
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=filename,
        mime="text/csv",
        use_container_width=True
    )


def html_report(title, body, filename):
    content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{html.escape(title)}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 35px;
            }}
            h1 {{
                color: #17365d;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
            }}
        </style>
    </head>
    <body>
        <h1>{html.escape(title)}</h1>
        {body}
    </body>
    </html>
    """

    st.download_button(
        "Download HTML report",
        data=content.encode("utf-8"),
        file_name=filename,
        mime="text/html"
    )


# ---------------------------------------------------------
# Validate and load the historical dataset
# ---------------------------------------------------------

if not DATA_PATH.exists():
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()

try:
    historical_df = load_data(
        str(DATA_PATH),
        DATA_PATH.stat().st_mtime
    )

except Exception as error:
    st.error(f"Dataset loading error: {error}")
    st.stop()

if TARGET_COLUMN not in historical_df.columns:
    st.error(
        f"Required target column is missing: {TARGET_COLUMN}"
    )
    st.stop()

if historical_df.empty:
    st.error("The historical dataset is empty.")
    st.stop()

output_records = load_output_records()


# ---------------------------------------------------------
# Sidebar controls
# ---------------------------------------------------------

st.sidebar.title("Dashboard Controls")

minimum_date = historical_df[DATE_COLUMN].min().date()
maximum_date = historical_df[DATE_COLUMN].max().date()

date_range = st.sidebar.date_input(
    "Select historical date range",
    value=(minimum_date, maximum_date),
    min_value=minimum_date,
    max_value=maximum_date
)

if isinstance(date_range, (tuple, list)):
    if len(date_range) == 2:
        start_date, end_date = date_range
    elif len(date_range) == 1:
        start_date, end_date = date_range[0], maximum_date
    else:
        start_date, end_date = minimum_date, maximum_date
else:
    start_date, end_date = date_range, maximum_date

if start_date > end_date:
    st.sidebar.error("Invalid date range.")
    st.stop()

filtered_df = historical_df[
    historical_df[DATE_COLUMN].dt.date.between(
        start_date,
        end_date
    )
].copy()

if filtered_df.empty:
    st.warning("No observations in the selected date range.")
    st.stop()

forecast_horizon = st.sidebar.selectbox(
    "Forecast horizon",
    FORECAST_HORIZONS,
    index=2,
    format_func=lambda x: f"{x} days"
)

model_selector = st.sidebar.selectbox(
    "Model selector",
    [
        "All available models",
        "Baseline",
        "Statistical",
        "Machine Learning",
        "Combined"
    ]
)

confidence_level = st.sidebar.selectbox(
    "Confidence level",
    [80, 90, 95, 99],
    index=2,
    format_func=lambda x: f"{x}%"
)

capacity = st.sidebar.number_input(
    "Verified HHS capacity",
    min_value=0,
    value=0,
    step=10
)

st.sidebar.subheader("Scenario assumptions")

inflow_adjustment = st.sidebar.slider(
    "Demand inflow adjustment (%)",
    min_value=-50,
    max_value=50,
    value=0,
    step=5
)

transfer_adjustment = st.sidebar.slider(
    "Transfer adjustment (%)",
    min_value=-50,
    max_value=50,
    value=0,
    step=5
)

discharge_adjustment = st.sidebar.slider(
    "Discharge adjustment (%)",
    min_value=-50,
    max_value=50,
    value=0,
    step=5
)


# ---------------------------------------------------------
# Historical KPI calculations
# ---------------------------------------------------------

latest_value = historical_df[
    TARGET_COLUMN
].dropna()

latest_value = (
    float(latest_value.iloc[-1])
    if not latest_value.empty
    else np.nan
)

period_values = filtered_df[
    TARGET_COLUMN
].dropna()

period_change = (
    float(period_values.iloc[-1] - period_values.iloc[0])
    if len(period_values) >= 2
    else np.nan
)


# ---------------------------------------------------------
# Navigation
# ---------------------------------------------------------

module = st.sidebar.radio(
    "Application module",
    [
        "Overview",
        "Historical Monitoring",
        "Predictive Forecasting",
        "Capacity and Surge Risk",
        "Scenario and Model Comparison"
    ]
)


# ---------------------------------------------------------
# Overview module
# ---------------------------------------------------------

if module == "Overview":

    st.header("System Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Latest HHS Care Load",
        f"{latest_value:,.0f}"
        if pd.notna(latest_value)
        else "Unavailable"
    )

    col2.metric(
        "Historical Records",
        f"{len(historical_df):,}"
    )

    col3.metric(
        "Selected Period Change",
        f"{period_change:+,.0f}"
        if pd.notna(period_change)
        else "Unavailable"
    )

    col4.metric(
        "Available Output Files",
        f"{len(output_records):,}"
    )

    st.subheader("Historical HHS Care Load")

    chart_df = filtered_df[
        [DATE_COLUMN, TARGET_COLUMN]
    ].dropna()

    if not chart_df.empty:
        fig = px.line(
            chart_df,
            x=DATE_COLUMN,
            y=TARGET_COLUMN,
            title="HHS Care Load Over Time"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Recent historical observations")
    display_table(filtered_df.tail(20))

    csv_download(
        filtered_df,
        "historical_data.csv",
        "Download historical data"
    )


# ---------------------------------------------------------
# Historical monitoring module
# ---------------------------------------------------------

elif module == "Historical Monitoring":

    st.header("Historical Monitoring")

    numeric_columns = get_numeric_columns(filtered_df)

    selected_indicators = st.multiselect(
        "Select historical indicators",
        options=numeric_columns,
        default=[
            TARGET_COLUMN
        ] if TARGET_COLUMN in numeric_columns else []
    )

    if selected_indicators:
        chart_df = filtered_df[
            [DATE_COLUMN] + selected_indicators
        ]

        fig = px.line(
            chart_df,
            x=DATE_COLUMN,
            y=selected_indicators,
            title="Historical Indicator Monitoring"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("Select at least one indicator.")

    st.subheader("Descriptive statistics")

    if numeric_columns:
        summary = (
            filtered_df[numeric_columns]
            .describe()
            .T
            .reset_index()
            .rename(columns={"index": "Indicator"})
        )

        display_table(summary)

    st.subheader("Historical data")
    display_table(filtered_df)

    csv_download(
        filtered_df,
        "historical_monitoring.csv",
        "Download historical data"
    )

    report_body = f"""
    <h2>Historical Monitoring</h2>
    <p>Period: {start_date} to {end_date}</p>
    <p>Records: {len(filtered_df)}</p>
    <p>Latest HHS care load: {latest_value}</p>
    """

    html_report(
        "Historical Monitoring Report",
        report_body,
        "historical_monitoring_report.html"
    )


# ---------------------------------------------------------
# Predictive forecasting module
# ---------------------------------------------------------

elif module == "Predictive Forecasting":

    st.header("Predictive Forecasting")

    prediction_records = find_records(
        output_records,
        [
            "prediction",
            "forecast",
            "walk_forward"
        ]
    )

    if not prediction_records:
        st.warning(
            "No saved prediction files were found in outputs."
        )

    else:
        selected_file = st.selectbox(
            "Select forecast file",
            [record["name"] for record in prediction_records]
        )

        selected_record = next(
            record
            for record in prediction_records
            if record["name"] == selected_file
        )

        prediction_df = selected_record["data"].copy()

        display_table(prediction_df.head(200))

        numeric_columns = get_numeric_columns(
            prediction_df
        )

        if numeric_columns:
            prediction_column = st.selectbox(
                "Select prediction column",
                numeric_columns
            )

            date_column = find_date_column(
                prediction_df
            )

            if date_column is not None:
                prediction_df[date_column] = pd.to_datetime(
                    prediction_df[date_column],
                    errors="coerce"
                )

                plot_df = prediction_df.dropna(
                    subset=[
                        date_column,
                        prediction_column
                    ]
                )

                if not plot_df.empty:
                    fig = px.line(
                        plot_df,
                        x=date_column,
                        y=prediction_column,
                        title="Saved Forecast Predictions"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

        csv_download(
            prediction_df,
            "forecast_predictions.csv",
            "Download predictions"
        )

    st.subheader("Forecast configuration")

    st.write("Forecast horizon:", forecast_horizon, "days")
    st.write("Selected model:", model_selector)
    st.write("Confidence level:", confidence_level, "%")

    interval_records = find_records(
        output_records,
        ["interval"]
    )

    if interval_records:
        for record in interval_records:
            with st.expander(record["name"]):
                display_table(record["data"])

                csv_download(
                    record["data"],
                    record["name"],
                    "Download interval data"
                )
    else:
        st.info(
            "No saved prediction interval file was found. "
            "Changing the confidence selector does not "
            "recalculate model intervals."
        )


# ---------------------------------------------------------
# Capacity and surge-risk module
# ---------------------------------------------------------

elif module == "Capacity and Surge Risk":

    st.header("Capacity and Surge Risk")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Latest HHS Care Load",
        f"{latest_value:,.0f}"
        if pd.notna(latest_value)
        else "Unavailable"
    )

    col2.metric(
        "Entered HHS Capacity",
        f"{capacity:,.0f}"
        if capacity > 0
        else "Not supplied"
    )

    if capacity > 0 and pd.notna(latest_value):
        remaining_capacity = capacity - latest_value

        col3.metric(
            "Remaining Capacity",
            f"{remaining_capacity:,.0f}"
        )

        utilization = latest_value / capacity * 100

        st.metric(
            "Capacity Utilization",
            f"{utilization:.2f}%"
        )

        st.progress(
            min(max(utilization / 100, 0.0), 1.0)
        )

        if utilization >= 100:
            st.error(
                "Observed care load has reached or exceeded capacity."
            )
        elif utilization >= 85:
            st.warning(
                "Observed care load is approaching capacity."
            )
        else:
            st.success(
                "Observed care load is below the entered capacity."
            )

    else:
        st.warning(
            "Enter a verified capacity value and ensure "
            "the latest care-load observation is available."
        )

    st.subheader("Saved operational risk outputs")

    risk_records = find_records(
        output_records,
        [
            "capacity_breach_probability",
            "operational_resource_pressure",
            "peak_care_load",
            "scenario_uncertainty"
        ]
    )

    if risk_records:
        for record in risk_records:
            with st.expander(record["name"]):
                display_table(record["data"])

                csv_download(
                    record["data"],
                    record["name"],
                    "Download risk output"
                )
    else:
        st.info(
            "No saved operational risk files were found."
        )

    st.caption(
        "No capacity is inferred or fabricated. "
        "Use a verified operational capacity."
    )


# ---------------------------------------------------------
# Scenario and model-comparison module
# ---------------------------------------------------------

elif module == "Scenario and Model Comparison":

    st.header("Scenario and Model Comparison")

    st.subheader("Current scenario assumptions")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Demand inflow adjustment",
        f"{inflow_adjustment:+d}%"
    )

    col2.metric(
        "Transfer adjustment",
        f"{transfer_adjustment:+d}%"
    )

    col3.metric(
        "Discharge adjustment",
        f"{discharge_adjustment:+d}%"
    )

    st.caption(
        "These controls display scenario assumptions. "
        "They do not automatically rerun the scenario model."
    )

    scenario_records = find_records(
        output_records,
        [
            "scenario_comparison",
            "scenario_forecast_summary",
            "scenario_daily_forecasts",
            "hhs_scenario_comparison",
            "cbp_scenario_comparison",
            "scenario_assumptions"
        ]
    )

    if scenario_records:
        selected_scenario_file = st.selectbox(
            "Select scenario output",
            [record["name"] for record in scenario_records]
        )

        selected_record = next(
            record
            for record in scenario_records
            if record["name"] == selected_scenario_file
        )

        scenario_df = selected_record["data"].copy()

        display_table(scenario_df)

        numeric_columns = get_numeric_columns(
            scenario_df
        )

        date_column = find_date_column(
            scenario_df
        )

        if date_column and numeric_columns:
            scenario_df[date_column] = pd.to_datetime(
                scenario_df[date_column],
                errors="coerce"
            )

            selected_columns = st.multiselect(
                "Select scenario chart variables",
                numeric_columns,
                default=numeric_columns[:3]
            )

            if selected_columns:
                chart_df = scenario_df[
                    [date_column] + selected_columns
                ].dropna(subset=[date_column])

                if not chart_df.empty:
                    fig = px.line(
                        chart_df,
                        x=date_column,
                        y=selected_columns,
                        title="Scenario Forecast Comparison"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

        csv_download(
            scenario_df,
            "scenario_output.csv",
            "Download scenario data"
        )

    else:
        st.warning(
            "No scenario output files were found."
        )

    st.subheader("Model evaluation and comparison")

    comparison_records = find_records(
        output_records,
        [
            "model_comparison",
            "evaluation",
            "metrics",
            "performance",
            "test_errors",
            "validation_errors"
        ]
    )

    if comparison_records:
        for record in comparison_records:
            with st.expander(record["name"]):
                display_table(record["data"])

                csv_download(
                    record["data"],
                    record["name"],
                    "Download comparison data"
                )
    else:
        st.info(
            "No saved model evaluation files were found."
        )

    report_body = f"""
    <h2>Scenario Assumptions</h2>
    <table>
        <tr><th>Variable</th><th>Adjustment</th></tr>
        <tr><td>Demand inflow</td><td>{inflow_adjustment}%</td></tr>
        <tr><td>Transfers</td><td>{transfer_adjustment}%</td></tr>
        <tr><td>Discharges</td><td>{discharge_adjustment}%</td></tr>
    </table>
    <p>Forecast horizon: {forecast_horizon} days</p>
    <p>Confidence level: {confidence_level}%</p>
    <p>Model selection: {html.escape(model_selector)}</p>
    """

    html_report(
        "Scenario and Model Comparison Report",
        report_body,
        "scenario_comparison_report.html"
    )


# ---------------------------------------------------------
# Application footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "Care Load and Placement Demand Forecasting Dashboard"
)

st.caption(
    "Forecast outputs and operational indicators should be "
    "interpreted using their original modelling assumptions "
    "and verified source data."
)
