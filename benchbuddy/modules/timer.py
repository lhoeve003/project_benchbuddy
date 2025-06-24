# Importeert de streamlit library voor het bouwen van de webapp.
# 'as st' zorgt voor het makkelijker gebruik in de code zelf.
import streamlit as st
# Importeert de time module, voor tijdsmetingen.
import time

# Deze functie zorgt voor het maken van de timer functie op streamlit.
def show():
    # Met de functies van streamlit, markdown en write, is benodige tekst ingesteld.
    # De html code is gemaakt met ChatGPT.
    st.markdown("<div class='section-header'>Experiment Timer</div>", unsafe_allow_html=True)
    st.write("Set your timer duration:")

    # Er worden drie verschillende invoervelden gemaakt voor uren, minuten en seconden.
    # De min en max values bepalen het bereik van de input.
    # De key zorgt ervoor dat alle drie invoervelden uniek zijn op streamlit.
    # https://docs.streamlit.io/develop/api-reference/widgets/st.number_input
    hours = st.number_input("Hours",   min_value=0, max_value=23, step=1, key="t_hours")
    minutes = st.number_input("Minutes", min_value=0, max_value=59, step=1, key="t_minutes")
    seconds = st.number_input("Seconds", min_value=0, max_value=59, step=1, key="t_seconds")
    # Hier wordt de input omgerekend naar totale seconden voor de timer zelf.
    total_seconds = int(hours * 3600 + minutes * 60 + seconds)

    # Zorgt voor dat drie variablen altijd bestaan op de pagina:
    # Timer_state: staat de timer aan of uit?
    # Timer_end: mogelijkheid om de timer te stoppen.
    # Timer_left: geeft aan hoe lang de timer nog moet lopen.
    # Onderstaande codes gemaakt met streamlit functie en ChatGPT.
    # https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    if "timer_state" not in st.session_state:
        st.session_state.timer_state = "stopped"
    if "timer_end" not in st.session_state:
        st.session_state.timer_end = None
    if "timer_left" not in st.session_state:
        st.session_state.timer_left = 0

    # Als de gebruiker op de 'start/resume' knop drukt:
    if st.button("Start / Resume"):
        # Als de timer op pauze stond, gaat de tijd verder waar die was.
        if st.session_state.timer_state == "paused":
            # De eindtijd wordt dan opnieuw ingesteld.
            st.session_state.timer_end = time.time() + st.session_state.timer_left
        # Als de timer niet op pauze stond:
        else:
            # Er wordt gecontroleerd of de input groter is dan 0.
            if total_seconds > 0:
                # De eindtijd wordt ingesteld op de input.
                st.session_state.timer_end = time.time() + total_seconds
            # Is de eindtijd negatief, dan wordt er een foutmelding getoond.
            else:
                st.error("Please enter a valid duration.")
        # Als de timer loopt wordt er laten zien dat deze ook echt loopt.
        st.session_state.timer_state = "running"

    # Als er op pauze wordt gedrukt, pauzeert de timer.
    if st.button("Pause") and st.session_state.timer_state == "running":
        # Berekend hoeveel secconden er zijn tot de timer is afgelopen.
        st.session_state.timer_left = max(0, int(st.session_state.timer_end - time.time()))
        # Hiermee onthoudt streamlit dat de timer op pauze staat.
        st.session_state.timer_state = "paused"

    # Er wordt een stop knop gemaakt in streamlit.
    # Als er op deze knop wordt gedrukt dan:
    if st.button("Stop"):
        # De timer stopt.
        st.session_state.timer_state = "stopped"
        # De eindtijd wordt geleegd.
        st.session_state.timer_end = None
        # De tijd over wordt op nul gezet.
        st.session_state.timer_left = 0

    # Als de timer runt:
    if st.session_state.timer_state == "running":
        # Bereken hoeveel seconden er nog over zijn.
        remaining = max(0, int(st.session_state.timer_end - time.time()))
        # Als er geen tijd meer over is:
        if remaining == 0:
            # Zet de timer op stop en toon een melding.
            st.session_state.timer_state = "stopped"
            st.success("⏰ Time is up!")
        # Als er nog tijd over is:
        else:
            # Bereken het aantal seconden over naar uren, minuten en seconden.
            hrs, rem = divmod(remaining, 3600)
            # Toon de overgebleven tijd op de pagina.
            mins, secs = divmod(rem, 60)
            st.info(f"⏳ {hrs:02}:{mins:02}:{secs:02} remaining")
            # Zorgt er voor dat de timer elke seconden bijwerkt.
            st.experimental_rerun()

    # Als de timer op pauze staat:
    elif st.session_state.timer_state == "paused":
        # Haal op wat de resterende tijd is en zet om naar uren, minuten en seconden.
        hrs, rem = divmod(int(st.session_state.timer_left), 3600)
        mins, secs = divmod(rem, 60)
        # Laat een tekst zien met op welke tijd de tijd is gepauseerd.
        # https://docs.streamlit.io/develop/api-reference/status/st.warning
        st.warning(f" Paused at {hrs:02}:{mins:02}:{secs:02}")

    else:
        st.write("Ready to start your timer.")
