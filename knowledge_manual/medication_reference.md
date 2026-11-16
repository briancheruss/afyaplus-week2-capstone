# AfyaPlus Medication Calculation Rules — SYNTHETIC TRAINING DATA

**Status:** Arithmetic demonstration only, not a medication formulary.

## Volume calculation

Given a dose explicitly confirmed by a qualified clinician (mg) and a labeled liquid
concentration (mg/mL), volume (mL) = dose (mg) / concentration (mg/mL).
The system must reject zero, negative, non-finite, and nonsensical values. Do not
calculate or suggest a dose based on symptoms or patient characteristics.

## BMI calculation

BMI = weight in kilograms divided by height in meters squared. BMI is a screening
metric, not a diagnosis. Consult a clinician for interpretation.
