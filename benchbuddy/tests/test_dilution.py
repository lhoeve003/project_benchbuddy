
from modules.dilution import molar_to_mg_per_ml, mg_per_ml_to_molar
import pytest

def test_molar_to_mg_per_ml_zero():
    assert molar_to_mg_per_ml(0, 100) == 0

def test_mg_per_ml_to_molar_zero():
    assert mg_per_ml_to_molar(0, 100) == 0

def test_mg_per_ml_to_molar_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        mg_per_ml_to_molar(1.0, 0)

# De functie assert pytest.approx is gevonden met ChatGPT.
def test_molar_to_mg_per_ml():

    result = molar_to_mg_per_ml(0.01, 180)
    assert pytest.approx(result) == 1.8

def test_mg_per_ml_to_molar():
    result = mg_per_ml_to_molar(1.8, 180)
    assert pytest.approx(result) == 0.01
