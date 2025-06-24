# Importeert de streamlit library voor het bouwen van de webapp.
# 'as st' zorgt voor het makkelijker gebruik in de code zelf.
import streamlit as st
# Importeert de save_date functie om gegevens op te kunnen slaan in de database.
from db.database import save_data

# Zet mol/L om naar mg/mL
def molar_to_mg_per_ml(molar, mol_weight):
    # molair (mol/L) × mol_weight (gram/mol) = gram/L.
    # gram/L is hetzelfde als mg/mL.
    return molar * mol_weight

# Zet mg/mL om naar mol/L
def mg_per_ml_to_molar(mg_per_ml, mol_weight):
    # 1 mg/mL =1 g/L*1/1000, dus delen door 1000.
    # Daarna wordt gedeeld door het molgewicht om mol/L te krijgen.
    return mg_per_ml / mol_weight

# Deze functie zorgt voor de aansturing van de streamlit-webapp
def show(c, conn):
    # De functies van streamlit: https://docs.streamlit.io/develop/api-reference/text/st.markdown
    # En: https://docs.streamlit.io/develop/api-reference/write-magic/st.write
    # De html code voor de titel en verdere tekst op de pagina,
    # Is gemaakt m.b.v AI (chatGPT/Perplexity).
    # 'unsafe_allow_html=True' laat toe om HTML te gebruiken voor een betere styling van de webapp.
    st.markdown("<div class='section-header'>Dilution Calculator</div>", unsafe_allow_html=True)
    st.write("Calculate the required volumes for a dilution.")

    # Laat een widget zien op de site,
    # waarmee de gebruiker kan kiezen welke concentratie wordt omgezet.
    # De gebruikers invoer bepaalt de rest van de invoer.
    conc_unit = st.selectbox("Select concentration unit:", ["mg/mL", "M (mol/L)"])

    # Het molgewicht wordt op 'nog niet ingevuld' gezet
    mol_weight = None

    # Controleert welke concentratie-eenheid is gekozen:
    # als de gebruiker voor begin concentratie M heeft gekozen.
    if conc_unit == "M (mol/L)":
        # Als M is gekozen, wordt er een invoerveld getoond voor invoeren van molecuulgewicht.
        # bron: https://docs.streamlit.io/develop/api-reference/widgets/st.number_input
        # Invoer kan alleen positief zijn of 0.
        # Invoer wordt weergeven met vier cijfers achter de komma voor precisie.
        mol_weight = st.number_input("Molecular weight (g/mol):", min_value=0.0, format="%.4f")

    # Vooraf staat deze variable op nul, er is nog geen richting van conversie gekozen.
    conversion_direction = None
    # Controle: is er een waarde ingevuld, en is de gekozen eenheid 'M.
    if mol_weight and conc_unit == "M (mol/L)":
        # Als voorwaarden voldoen, verschijnt keuze knop.
        # https://docs.streamlit.io/develop/api-reference/widgets/st.radio
        conversion_direction = st.radio(
            "Choose conversion:",
            ("Molair naar mg/mL", "mg/mL to Molair")
        )
    else:
        conversion_direction = "No conversion"

    # Maak een invoer veld op streamlit zodat de gebruiker de concentratie of volume kan invullen.
    # De eenheid wordt automatisch ingevuld, mg/mL of 'M" (mol/L).
    # Alleen positieve getallen of 0 kunnen worden ingevoerd.
    # Getal wordt weergeven met vier decimalen.
    # Gemaakt met streamlit number_input functie en ChatGPT.
    c1_input = st.number_input(f"Start concentration: ({conc_unit}):", min_value=0.0, format="%.4f")
    c2_input = st.number_input(f"Final concentration: ({conc_unit}):", min_value=0.0, format="%.4f")
    v2 = st.number_input("End volume (mL):", min_value=0.0, format="%.2f")

    # Gemaakt met streamlit functies en ChatGPT.
    # Zodra de knop met 'calculate' wordt ingedrukt.
    # https://docs.streamlit.io/develop/api-reference/widgets/st.button
    if st.button("Calculate"):
        # Controleer of alle ingevulde waarden wel positieve getallen zijn.
        if c1_input > 0 and c2_input > 0 and v2 > 0:
            # Afhankelijk van de gekozen conversie:
            # Omrekening van mol/L naar mg/mL.
            if conversion_direction == "Molair to mg/mL":
                c1 = molar_to_mg_per_ml(c1_input, mol_weight)
                c2 = molar_to_mg_per_ml(c2_input, mol_weight)
            # Omrekening van mg/mL naar mol/L/
            elif conversion_direction == "mg/mL to Molair":
                c1 = mg_per_ml_to_molar(c1_input, mol_weight)
                c2 = mg_per_ml_to_molar(c2_input, mol_weight)
            # De waarden worden niet omgerekend.
            else:
                c1 = c1_input
                c2 = c2_input

            # Controleert of de startconcentratie groter is dan eindconcentratie,
            # Verdunningen kunnen niet van lage naar hoge concentratie gaan.
            if c1 <= c2:
                st.error("Starting concentration must be greater than the final concentration.")
                return

            # Formule om de verdunning uit te rekenen.
            v1 = (c2 * v2) / c1
            # Bereken het aantal oplosmiddel waarin opgelost moet worden.
            water = v2 - v1
            # Toon het resultaat
            result = f"Take {v1:.2f} mL volue of the stock and add {water:.2f} mL solvent."
            # Als de berekening gelukt is, toon bericht dat het gelukt is.
            # https://docs.streamlit.io/develop/api-reference/status/st.success
            st.success(result)

            # Gemaakt met streamlit functies en chatGPT.
            # Het resultaat wordt opgeslagen in de database.
            save_data(
                c, conn, "Dilution",
                f"C1={c1_input} {conc_unit}, C2={c2_input} {conc_unit}, V2={v2} mL, conversion={conversion_direction}",
                result
            )
        # Als niet alle ingevoerde waarden positief zijn wordt een foutmelding getoond.
        else:
            st.error("Check that all values are entered as positive numbers and the molecular weight (if required).")
