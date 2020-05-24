# @autor : SEMBLANET Tom (ISAE-SUPAERO)

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import sys, json

import utility_functions as u_f
import gross_calculation as g_c



json_simu = json.loads(sys.argv[1])
open("__.txt", 'w').write(str(json_simu))

# Instanciation des objets de la simulation & chargement des paramètres
u_f.loadSimulation(json_simu)

# Boucles principale de calcul
dict_ = g_c.GeneralCalculation(json_simu["exploitation"])

# Envoie des données à l'UI
print(json.dumps(dict_))

