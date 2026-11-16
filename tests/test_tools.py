from app.tools import calculate_bmi, calculate_medication_volume


def test_volume():
    assert "5.000 mL" in calculate_medication_volume.invoke({"dose_mg": 250, "concentration_mg_per_ml": 50})


def test_volume_zero_rejected():
    assert "rejected" in calculate_medication_volume.invoke({"dose_mg": 250, "concentration_mg_per_ml": 0})


def test_bmi():
    assert "BMI: 25.00" in calculate_bmi.invoke({"weight_kg": 81, "height_m": 1.8})


def test_bmi_invalid():
    assert "rejected" in calculate_bmi.invoke({"weight_kg": -1, "height_m": 1.8})
