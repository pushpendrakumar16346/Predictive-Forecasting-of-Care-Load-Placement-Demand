# Initial Dataset Limitations

## Dataset
HHS Unaccompanied Alien Children Program

## Initial observations

1. The original CSV contains completely blank rows.
2. The Date column is originally stored as text.
3. Children in HHS Care is originally stored as text
   because values contain thousands separators.
4. The dataset is ordered from newest to oldest.
5. The observations do not occur on every calendar day.
6. Date gaps must be investigated before daily forecasting.
7. The official publisher and source URL have not yet
   been independently verified from the CSV itself.
8. Historical relationships do not establish causation.
9. The dataset contains aggregate operational indicators.
10. External policy, border activity, and humanitarian
    events may not be represented in the historical data.

## Important modeling considerations

- Do not interpret missing dates as zero observations.
- Do not automatically fill missing observations with zero.
- Preserve the original raw CSV.
- Validate date frequency before creating daily forecasts.
- Use chronological validation rather than random splitting.
- Avoid using future observations as model predictors.
- Evaluate forecast performance separately by horizon.
- Investigate whether secondary indicators are available
  at the forecast issue date before using them as predictors.
- Do not assume operational counts are interchangeable
  with population stocks or flow measures.

## Forecasting scope

Primary target:
Children in HHS Care.

Secondary targets:
1. Children apprehended and placed in CBP custody.
2. Children in CBP custody.
3. Children transferred out of CBP custody.
4. Children discharged from HHS Care.

Forecast horizons:
1, 7, 14, and 30 days.
