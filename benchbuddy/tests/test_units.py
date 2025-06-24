import pytest
from modules.units import convert_volume, convert_temperature

def test_convert_volume():
    # µL wordt omgezet naar mL.
    assert convert_volume(1000, "µL", "mL") == 1
    # mL wordt omgezet naar L.
    assert convert_volume(1000, "mL", "L") == 1
    # L wordt omgezet naar µL.
    assert convert_volume(1, "L", "µL") == 1_000_000
    # Dezelfde volume wordt omgezet.
    assert convert_volume(5, "mL", "mL") == 5

def test_convert_temperature():
    # Zelfde units worden omgezet.
    assert convert_temperature(25, "°C", "°C") == 25
    assert convert_temperature(77, "°F", "°F") == 77
    # Celcius wordt omgezet naar fahrenheit.
    assert round(convert_temperature(0, "°C", "°F"), 2) == 32.00
    assert round(convert_temperature(100, "°C", "°F"), 2) == 212.00
    # Fahrenheit wordt omgezet naar celcius.
    assert round(convert_temperature(32, "°F", "°C"), 2) == 0.00
    assert round(convert_temperature(212, "°F", "°C"), 2) == 100.00
    # Onbekende conversie die niet mogelijk is, geeft foutmelding.
    assert convert_temperature(0, "°C", "K") is None

# Round wordt gebruikt om de kommagetallen af te ronden voor de unittest.
# https://docs.python.org/3/library/unittest.html

