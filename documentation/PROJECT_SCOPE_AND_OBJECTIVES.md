# Predictive Forecasting of Care Load & Placement Demand

## 1. Business Problem

The Unaccompanied Alien Children (UAC) Program operates in an
environment where border activity, policy changes, and humanitarian
events can cause rapid changes in the number of children entering
federal care.

Historical descriptive reporting explains previous activity but
does not adequately support proactive resource planning.

This project develops predictive forecasting models to estimate
future care loads and placement-related demand.

## 2. Primary Business Objective

Develop reliable forecasting models to predict the number of
Children in HHS Care over the following horizons:

- 1 day
- 7 days
- 14 days
- 30 days

The forecasts will support planning, resource allocation,
operational readiness, and placement capacity management.

## 3. Research Questions

1. How many children are expected to be in HHS Care over the
   next 1, 7, 14, and 30 days?

2. Which historical patterns and operational indicators are
   associated with changes in HHS care population?

3. How accurately can statistical and machine-learning models
   forecast future care loads?

4. Can CBP custody and transfer indicators improve forecasting
   performance?

5. How can forecast uncertainty support operational planning?

6. How can scenario analysis support capacity planning under
   changing operational conditions?

## 4. Research Hypotheses

H1: Historical care population patterns contain useful information
for forecasting future HHS care loads.

H2: Recent changes in CBP custody and transfer activity can provide
additional forecasting information.

H3: Forecast accuracy differs across forecasting horizons.

H4: Machine-learning and statistical forecasting models may
perform differently depending on the target and horizon.

H5: Forecast uncertainty increases as the forecasting horizon
becomes longer.

These hypotheses will be evaluated empirically.

## 5. Government Stakeholders and Dashboard Users

- HHS leadership and program management.
- Office of Refugee Resettlement (ORR) operational teams.
- UAC program planning and resource allocation teams.
- CBP operational stakeholders.
- Care provider and placement capacity planners.
- Government analysts and forecasting teams.
- Executive decision-makers.

## 6. Primary Forecasting Target

Children in HHS Care

This represents the principal measure of the population
requiring care capacity planning.

## 7. Secondary Forecasting Targets

1. Children apprehended and placed in CBP custody.
2. Children in CBP custody.
3. Children transferred out of CBP custody.
4. Children discharged from HHS Care.

## 8. Forecasting Horizons

- Short-term: 1 day.
- Weekly: 7 days.
- Medium-term: 14 days.
- Extended short-term: 30 days.

## 9. Project Scope

The project includes:

- Historical data inspection and cleaning.
- Missing-date and observation-gap assessment.
- Exploratory time-series analysis.
- Feature engineering.
- Statistical forecasting.
- Machine-learning forecasting.
- Chronological model validation.
- Forecast uncertainty estimation.
- Scenario analysis.
- Performance comparison.
- Interactive Streamlit dashboard.
- Executive reporting.
- Research documentation.

## 10. Proposed Modeling Approaches

Statistical models:
- Naive forecasting.
- Moving average baseline.
- ARIMA.
- SARIMA.
- Exponential Smoothing.

Machine-learning models:
- Random Forest.
- Gradient Boosting.

Model selection will be based on chronological validation
and forecasting performance.

## 11. Model Evaluation

The following metrics will be considered:

- Mean Absolute Error (MAE).
- Root Mean Squared Error (RMSE).
- Mean Absolute Percentage Error (MAPE).
- Weighted Absolute Percentage Error (WAPE).

## 12. Project Limitations

- Historical observations do not guarantee future conditions.
- Sudden policy changes may affect forecast accuracy.
- External humanitarian and geopolitical events may not be
  represented in historical data.
- Irregular observation dates require careful treatment.
- Forecasts are decision-support estimates, not guarantees.
- Aggregate data cannot explain individual child circumstances.
- Forecast accuracy must be assessed separately for each horizon.

## 13. Data Integrity and Ethical Considerations

The analysis will use aggregate operational data.

No individual child-level prediction or profiling will be performed.

Missing observations will not automatically be interpreted
as zero activity.

Forecasts will be presented with appropriate limitations
and uncertainty considerations.

## 14. Reproducibility

- Fixed random seed: 42.
- Central configuration: src/config.py.
- Relative project paths.
- Versioned dependencies through requirements.txt.
- Consistent model and output naming conventions.

## 15. Expected Deliverables

1. Cleaned and processed datasets.
2. Exploratory analysis and visualizations.
3. Forecasting models.
4. Model evaluation results.
5. Forecast outputs for all horizons.
6. Scenario analysis.
7. Interactive dashboard.
8. Research paper.
9. Executive summary.
10. Technical documentation.
