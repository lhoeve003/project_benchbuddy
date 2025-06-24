#Importeert de streamlit library voor het bouwen van de webapp.
# 'as st' zorgt voor het makkelijker gebruik in de code zelf.
import streamlit as st
# Importeert zelfgemaakte modules uit de map modules.
from modules import home, timer, dilution, units, pcr, storage
# Importeert de save_date functie uit database.py om gegevens op te kunnen slaan in de database.
from db.database import init_db, save_data
# Importeert functies om CSS stijlen toe te passen op het design van streamlit.
from styles.custom_css import apply_custom_css
# Importeert image uit Pillow, voor de opening en bewerking van afbeeldingen.
from PIL import Image
# Importeert os, voor het werken met bestanden en mappen op je computer.
import os

# Deze functie voegt de aangepast CSS stijl toe aan de streamlit applicatie.
# Gemaakt via ChatGPT.
apply_custom_css()

# Gemaakt met os functies en ChatGPT.
# https://docs.python.org/3/library/os.path.html
# Controle of het bestand logo.png bestaat
logo_path = "assets/logo.png"
logo = Image.open(logo_path) if os.path.exists(logo_path) else None
# Als het logo bestaat wordt het ingeladen in de sidebar van de applicatie.
# https://docs.streamlit.io/develop/api-reference/media/st.logo
if logo:
    st.sidebar.image(logo, use_container_width=True)
# De afbeelding logo.png is zelf gemaakt m.b.v. Procreate 5.3.15,
# en sjablonen van Canva.



# Opzetten van verbinding met database, bron: ChatGPT.
# Conn is connectie, c is de cursor voor het uitvoeren van SQL query's.
conn, c = init_db()

# Zorgt ervoor dat als de gebruiker de site opent,
# het standaardmenu 'home' is.
# https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
if "menu" not in st.session_state:
    st.session_state.menu = "🏠 Home"

# Hier wordt een navigatiemenu in de side bar van de applicatie gemaakt.
# https://docs.streamlit.io/develop/api-reference/text/st.title
st.sidebar.title("BenchBuddy Navigation")
# De user kan een van de opties selecteren om naar dit onderdeel van de applicatie te gaan.
# Gemaakt met ChatGPT, https://docs.streamlit.io/develop/api-reference/widgets/st.radio en:
# https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
menu = st.sidebar.radio("Go to", [
    "🏠 Home",
    "⏱️ Timer",
    "💧 Dilution calculator",
    "📏 Units conversion",
    "🧬 PCR Analysis",
    "💾 Data Storage"
], index=[
    "🏠 Home",
    "⏱️ Timer",
    "💧 Dilution calculator",
    "📏 Units conversion",
    "🧬 PCR Analysis",
    "💾 Data Storage"
# Zorgt dat het menu op de juiste pagina staat, ook bij opnieuw inladen.
].index(st.session_state.menu))
# Dit zorgt er voor dat de gekozen pagina in het navigatiemenu wordt opgeslagen in streamlit.
if menu != st.session_state.menu:
    st.session_state.menu = menu

# Gemaakt m.b.v ChatGPT:
# Hier wordt bepaalt welk onderdeel van de streamlit applicatie wordt getoont,
# gebaseerd op de keuze van de user in het navigatiemenu in de sidebar.
if menu == "🏠 Home":
    home.show()
elif menu == "⏱️ Timer":
    timer.show()
elif menu == "💧 Dilution calculator":
    dilution.show(c, conn)
elif menu == "📏 Units conversion":
    units.show(c, conn)
elif menu == "🧬 PCR Analysis":
    pcr.show(c, conn)
elif menu == "💾 Data Storage":
    storage.show(c)

# Sluit de database verbinding af.
conn.close()
