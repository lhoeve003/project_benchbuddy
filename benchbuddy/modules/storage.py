# Importeert de streamlit library voor het bouwen van de webapp.
# 'as st' zorgt voor het makkelijker gebruik in de code zelf.
import streamlit as st
# Importeer de pandas library voor het werken met CSV bestanden, ook in streamlit.
# "as pd" zorgt voor makkelijker gebruik in de code zelf.
import pandas as pd

# Deze functie:
# Haalt opgeslagen experiment data uit de database
# Zet de data om naar tabel-format
# Zorgt dat gebruikers kunnen zoeken en filteren op datum en of tijd.


def show(c):
    # Met de functies markdown en write van streamlit wordt een titel en uitleg getoont.
    # Met ChatGPT is een html code gemaakt om deze tekst op de pagina te laten zien.
    st.markdown("<div class='section-header'>Data Storage</div>", unsafe_allow_html=True)
    st.write("View all saved experimental data below:")

    # Onderstaande code tot is gemaakt met behulp van benoemde streamlit functies en ChatGPT.
    # Een SQL-query wordt uitgevoerd om alle relevant info uit de tabel,
    # experiment_data uit de database op te halen.
    c.execute("SELECT id, type, input, result, timestamp FROM experiment_data ORDER BY timestamp DESC")
    # Haalt alle resultaten van de query op als een lijst van alle rijen.
    rows = c.fetchall()

    # Als er rijen opgehaald zijn, worden deze omgezet naar een 'DataFrame'.
    # https://www.w3schools.com/Python/pandas/pandas_dataframes.asp
    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Type", "Input", "Result", "Timestamp"])
        # De kolom timestamp wordt omgezet naar datetime format.
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        # Er wordt een uitklapbaar blok gemaakt met st.expander en filters ingesteld.
        # https://docs.streamlit.io/develop/api-reference/layout/st.expander
        with st.expander("🔍 Filter options", expanded=False):
            # https://docs.streamlit.io/develop/api-reference/widgets/st.date_input
            # Filteren op de kolommen input en result.
            search_term = st.text_input("Search in input/result:")
            # Filteren op datum.
            date_range = st.date_input("Filter by date range:", [])

        # Als er een filter is ingevoerd, wordt de DataFrame gefilterd,
        # op rijen waar de zoekterm in voorkomt.
        filtered_df = df

        # Alleen de rijen blijven over waarin de zoekterm voorkomt,
        # in de kolom Input of Result.
        # 'case=False' zorgt voor hoofdletterongevoeligheid.
        # 'na=False' zorgt er voor dat lege waarden niet worden meegenomen.
        if search_term:
            filtered_df = filtered_df[
                filtered_df["Input"].str.contains(search_term, case=False, na=False) |
                filtered_df["Result"].str.contains(search_term, case=False, na=False)
            ]

        # Filter op datum.
        # Controleert of er een start en einddatum is ingevoerd.
        if len(date_range) == 2:
            # Zet de start en einddatums om naar datetime-objecten,
            # zodat ze makkelijk vergeleken kunnen worden.
            start_date = pd.to_datetime(date_range[0])
            end_date = pd.to_datetime(date_range[1])
            # Filtert de DataFrame zodat alleen rijen overblijven,
            # tussen de start en einddatum die is ingevoerd.
            filtered_df = filtered_df[
                (filtered_df["Timestamp"] >= start_date) & (filtered_df["Timestamp"] <= end_date)
            ]
        # Toont de gefilterde DataFrame als een tabel in streamlit,
        # gesorteerd van nieuw naar oud (ascending=False).
        # https://docs.streamlit.io/develop/api-reference/data/st.dataframe
        st.dataframe(filtered_df.sort_values("Timestamp", ascending=False))

        # Downloadknop voor de data als een CSV bestand.
        # Zet de DataFrame om naar een CSV bestand.
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        # Maakt een knop waaarmee het bestand kan worden gedownload in streamlit.
        # https://docs.streamlit.io/develop/api-reference/widgets/st.download_button
        st.download_button(
            # De tekst op de knop met een icoontje.
            label="📥 Download filtered data as CSV",
            # De inhoud van het bestand.
            data=csv,
            # De naam van het bestand dat wordt gedownload.
            file_name='filtered_experiment_data.csv',
            # Dit geeft aan dat het om een CSV bestand gaat.
            mime='text/csv'
        )

    # Als er geen data is wordt een foutmelding laten zien.
    else:
        st.write("No data saved yet.")
