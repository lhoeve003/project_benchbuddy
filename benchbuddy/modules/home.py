# Importeert de streamlit library voor het bouwen van de webapp.
# 'as st' zorgt voor het makkelijker gebruik in de code zelf.
import streamlit as st

# Functie voor de welkomst pagina van de webapp.
def show():
    # Toont een grote titel aan de pagina.
    # https://docs.streamlit.io/develop/api-reference/text/st.markdown
    # De html code is verkregen via Chatgpt.
    st.markdown("<div class='title'>Welcome to BenchBuddy!</div>",
                unsafe_allow_html=True)

    # Toont een tekst met uitleg met wat BenchBuddy is.
    # https://docs.streamlit.io/develop/api-reference/write-magic/st.write
    st.write("""
    BenchBuddy is your practical aid for the biomedical laboratory.
    Use it to manage timers, perform calculations, make dilutions,
    analyze PCR, and save results. Ideal for students and lab researchers
    who want to work clearly, quickly, and accurately.
    """)

    # De plaatsing van horizontale lijn zorgt voor een scheiding tussen de titel en de introductie.
    # De tekst is geplaatst als 'Markdown' zodat tekst bewerkt kan worden.
    # https://docs.streamlit.io/develop/api-reference/text/st.markdown
    st.markdown("---")
    st.markdown("### Overview of tools:")

    st.markdown("**⏱️ Timer**  \n- Use a countdown to track your timed lab steps easily.")
    st.markdown("- Just enter your time, press start, and get notified when the timer ends.")
    st.markdown("- Ideal for incubations, reactions, and other time-based steps on the laboratorium.")

    st.markdown("**💧 Dilution calculator**  \n- Determine dilution volumes easily.")
    st.markdown("- Enter start and end concentrations and get exact volumes.")
    st.markdown("- Prevent prep errors and save time on your experiments with clear output.")

    st.markdown("**📏 Units conversion**  \n- Convert between volumes and temperatures quickly.")
    st.markdown("- No more guesswork and prevent mistakes with unit conversions.")
    st.markdown("- Essential for accurate pipetting and reporting experiments.")

    st.markdown("**🧬 PCR Analysis**  \n- Analyze your qPCR experiment using 2^-ΔCt calculations.")
    st.markdown("- Compare expression between target and reference genes.")
    st.markdown("- Simplifies Ct-based gene expression analysis for your experiment results.")

    st.markdown("**💾 Data Storage**  \n- Save and organize your calculations easily.")
    st.markdown("- Review past data anytime for reproducibility and tracking.")
    st.markdown(
        "- Great for record keeping and lab documentation as it is possible to save your results as CSV file.")
