"""Defensive, structured clinical arithmetic tools; not prescribing advice."""
from langchain_core.tools import tool


@tool

def calculate_medication_volume(dose_mg: float, concentration_mg_per_ml: float) -> str:
    """Calculate volume (mL) from a *clinician-confirmed* dose and concentration.

    Educational arithmetic only; does not recommend a dose or verify medication safety.
    """
    try:
        dose = float(dose_mg)
        concentration = float(concentration_mg_per_ml)
        import math
        if not all(map(math.isfinite, (dose, concentration))):
            raise ValueError("inputs must be finite")
        if dose <= 0 or concentration <= 0:
            raise ValueError("dose and concentration must be greater than zero")
        volume = dose / concentration
        if not math.isfinite(volume) or volume > 10000:
            raise ValueError("result outside supported range")
        return f"Arithmetic result: {volume:.3f} mL (dose ÷ concentration). Verify with a clinician."
    except (ValueError, TypeError, OverflowError) as exc:
        return f"Calculation rejected: {exc}"


@tool

def calculate_bmi(weight_kg: float, height_m: float) -> str:
    """Calculate body mass index from positive weight (kg) and height (m)."""
    try:
        import math
        weight, height = float(weight_kg), float(height_m)
        if not math.isfinite(weight) or not math.isfinite(height):
            raise ValueError("inputs must be finite")
        if not (0 < weight <= 500 and 0 < height <= 3):
            raise ValueError("weight or height outside supported range")
        return f"BMI: {weight / height**2:.2f} kg/m². BMI is not a diagnosis."
    except (ValueError, TypeError, OverflowError) as exc:
        return f"Calculation rejected: {exc}"
