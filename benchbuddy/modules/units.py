# Importeert de streamlit library voor het bouwen van de webapp.
# 'as st' zorgt voor het makkelijker gebruik in de code zelf.
import streamlit as st
# Importeert de save_date functie om gegevens op te kunnen slaan in de database.
from db.database import save_data

# Omrekenen van volumes, microliter, mililiter en liter.
def convert_volume(value, from_unit, to_unit):
    # Library om aan te geven hoeveel mililiter elke unit is.
    units = {"µL": 0.001, "mL": 1, "L": 1000}
    # Zet de waarde om naar mililiter, en daarna naar gewenste unit.
    return value * units[from_unit] / units[to_unit]

# Omrekenen van temperatuur, celcius en fahrenheit.
def convert_temperature(value, from_unit, to_unit):
    # Als de omzetting hetzelfde is, orginele waarde wordt terug gegeven.
    if from_unit == to_unit:
        return value
    # Van celcius naar fahrenheit:
    # Vermenigvuldig met 9/5, plus 32.
    if from_unit == "°C" and to_unit == "°F":
        return value * 9/5 + 32
    # Van fahrenheit naar celcius:
    # Trek 32 af en vermenigvuldig met 5/9.
    elif from_unit == "°F" and to_unit == "°C":
        return (value - 32) * 5/9
    else:
        return None

# Deze functie zorgt voor een pagina in streamlit voor een unit converter.
def show(c, conn):
    # Met de functies markdown en write van streamlit wordt een titel en uitleg weergeven.
    # De html code is met ChatGPT gemaakt.
    st.markdown("<div class='section-header'>Unit Converter</div>", unsafe_allow_html=True)
    st.write("Convert between different volume units or temperatures.")

    # De gebruiker kan kiezen voor een conversion voor volume of temperature.
    conversion_type = st.selectbox("Select conversion type:", ["Volume", "Temperature"])

    # Onderstaande code voor volume en temperatrue is gemaakt m.b.v. streamlit functies en ChatGPT.

    # Als de user volume wilt omzetten:
    if conversion_type == "Volume":
        # Invoerveld om getal in te vullen.
        # Geen negatieve waarden.
        # Het getal wordt weergeven met vier getallen achter de komma.
        value = st.number_input("Volume:", min_value=0.0, format="%.4f")
        # De gebruiker kiest een van de drie units voor de input en output.
        unit_in = st.selectbox("From unit:", ["mL", "L", "µL"])
        unit_out = st.selectbox("To unit:", ["mL", "L", "µL"])

        # Er wordt een 'convert' knop gemaakt, en als deze wordt ingedrukt:
        if st.button("Convert"):
            # Laat het resultaat zien met vier getallen achter de komma.
            # Het resultaat wordt opgeslagen in de database.
            result = convert_volume(value, unit_in, unit_out)
            st.success(f"{value} {unit_in} = {result:.4f} {unit_out}")
            save_data(c, conn, "Units", f"{value} {unit_in} to {unit_out}", f"{result:.4f} {unit_out}")


    # Als de gebruiker kiest voor de temperature conversion:
    else:
        # Laat de gebruiker een invoerveld zien voor de input.
        # De input wordt weergeven met twee getallen achter de komma.
        value = st.number_input("Temperature:", format="%.2f")
        # https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox
        # De gebruiker kiest hiermee de eenheid van de input.
        unit_in = st.selectbox("From unit:", ["°C", "°F"])
        # De gebruiker kiest hierrmee de eenheid van de output.
        unit_out = st.selectbox("To unit:", ["°C", "°F"])

        # Als de gebruiker op de knop 'convert' drukt:
        if st.button("Convert"):
            result = convert_temperature(value, unit_in, unit_out)
            # Controleert of de omrekening gelukt is.
            if result is not None:
                # Laat het resultaat zien met twee getallen achter de komma met de eenheid.
                st.success(f"{value} {unit_in} = {result:.2f} {unit_out}")
                # Het resultaat wordt opgeslagen in de database.
                save_data(c, conn, "Units", f"{value} {unit_in} to {unit_out}", f"{result:.2f} {unit_out}")
            else:
                # Bij bijv. een niet-bestaande eenheid wordt een foutmelding weergeven.
                st.error("Unsupported temperature conversion.")
