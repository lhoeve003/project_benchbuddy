# In de db map staat een __init__.py bestandje.
# Deze map bevat code voor de database.
# Dit is nodig voor het verbinding maken en data opslaan/ophalen.


# Dit lege __init__.py bestandje zorgt ervoor dat Python deze map ziet als modules
# Door dit bestandje is het mogelijk om de hele db map te importeren
# Zonder dit bestand kan Python de map niet als module herkenne
# Nu is het wel mogelijk om 'import db' te gebruiken in andere delen van het project

# Dit bestandje is nu leeg omdat het alleen nodig is dat de map wordt herkent als module
# Verdere extra code is dus niet nodig.

# ChatGPT benoemde dit als aanbeveling voor het project, verder is uitgezocht waarom dit nodig was via:
# https://www.geeksforgeeks.org/python/what-is-__init__-py-file-in-python/
# https://www.youtube.com/watch?v=mWaMSGwiSB0
