# Importeert de streamlit library voor het bouwen van de webapp.
# 'as st' zorgt voor het makkelijker gebruik in de code zelf.
import streamlit as st
# Importeert de save_date functie om gegevens op te kunnen slaan in de database.
from db.database import save_data

# Deze functie zorgt voor de PCR-analyse tool in de streamlit webapp.
def show(c, conn):
    # Toont de titel van de pagina en instructie voor de gebruiker.
    # https://docs.streamlit.io/develop/api-reference/text/st.markdown
    # De html code is verkregen via ChatGPT.
    st.markdown(
        "<div class='section-header'>Simple PCR Analysis</div>",
        unsafe_allow_html=True,
    )

    st.write(
        "Enter Ct values and calculate relative expression (2^-ΔCt)."
    )

    # Zorgt voor het maken van twee invoervelden:
    # De Ct-waarde van het target-gene en het reference gene
    # De getallen worden weergeven met twee getallen achter de komma.
    ct_target = st.number_input("Ct target gene:", format="%.2f")
    ct_reference = st.number_input("Ct reference gene:", format="%.2f")

    # Als de gebruiker op de knop 'Calculate expression' drukt:
    if st.button("Calculate expression"):
        # Wordt gecontroleerd of beide ingevoerde waarden niet negatief zijn.
        if ct_target > 0 and ct_reference > 0:
            # Bereken delta_ct, het verschil tussen de waarden van de target en reference.
            delta_ct = ct_target - ct_reference
            # De relatieve expressie wordt berekent met de formule 2^-ΔCt.
            expression = 2 ** (-delta_ct)
            # De volgendde stuk code is gemaakt m.b.v streamlit functies en ChatGPT.
            # https://docs.streamlit.io/develop/api-reference/status/st.success
            # Toon het resultaat als een succesvolle melding, afgerond op vier decimalen.
            st.success(
                f"Relative expression: {expression:.4f}"
            )
            # Het resultaat wordt opgeslagen in de database.
            save_data(
                c,
                conn,
                "PCR",
                f"Ct target={ct_target}, Ct ref={ct_reference}",
                f"Expression={expression:.4f}",
            )
        # Geef een foutmelding als geen geldige Ct waardes zijn ingevoerd.
        else:
            st.error("Please enter valid Ct values.")


# Met Markdown worden tekstvakken gemaakt met uitleg over wat PCR is,
# wat de Ct waardes betekenen en hoe de gebruikte formule wat zegt over genexpressie.
# ChatGPT is geraadpleegd voor hoe met hekjes en sterretjes,
# de tekst bewerkt kon worden.
    st.markdown("""
Polymerase Chain Reaction (PCR) is a laboratory technique used to
rapidly produce millions to billions of copies of a specific segment
of DNA. This “molecular photocopying” lets scientists study tiny DNA
samples or use them in downstream analyses.

**Key steps**

1. **Denaturation** – heat separates double stranded DNA into single
   strands.
2. **Annealing** – short primers bind to specific sequences on the
   single strands.
3. **Extension** – DNA polymerase synthesises new strands from the
   primers.
4. These steps repeat for 30–40 cycles, giving exponential
   amplification.

PCR is run in a *thermocycler* that automatically changes temperature
for each step and finishes in a few hours.

Source: [Genome.gov PCR glossary](
https://www.genome.gov/genetics-glossary/Polymerase-Chain-Reaction-PCR)
""")

    st.markdown("""
### Understanding Ct Values

In real time PCR, the **cycle threshold (Ct)** is the number of cycles
required for the fluorescence signal to cross a set threshold.

* Low Ct → few cycles needed → **higher starting amount** of target.
* High Ct → many cycles needed → **lower starting amount** of target.

Example: Ct 20 indicates more template than Ct 30.

Source: [VDL NDSU factsheet](
https://www.vdl.ndsu.edu/wp-content/uploads/2022/10/PCR-Ct-Values-1.pdf)
""")

    st.markdown("### The 2<sup> ΔCt</sup> Method")

    st.markdown(
        "This method compares the Ct of your **target gene** with a "
        "**reference (house keeping) gene** to give relative expression:"
    )

    st.latex(
        r"\text{Relative Expression} = 2^{-\left(C_t^{\text{target}} - "
        r"C_t^{\text{reference}}\right)}"
    )

    st.markdown("""
The output is the fold change of the target gene normalised to the
reference gene. Ideal for comparing expression across samples,
treatments, or conditions.

Use the inputs **above** to calculate relative expression with your
Ct values.

Source: [BitesizeBio – ΔΔCt explained](
https://bitesizebio.com/24894/4-easy-steps-to-analyze-your-qpcr-data-using-double-delta-ct-analysis/)
""")
