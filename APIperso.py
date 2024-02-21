from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import pandas as pd
import json

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI()

# Charger le fichier CSV
Champignons = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/e5ba031c-ae1c-476a-a920-5fd401935b2a', encoding='latin1')

# Suppression de la colonne Unnamed :
del Champignons['Unnamed: 42']

# Transformation de l'autre colonne numérique :
Champignons['Diametre maximum du chapeau'] = Champignons['Diametre maximum du chapeau'].apply(lambda x: float(x.replace(',','.')))

@app.get("/champignons", response_class=JSONResponse)
async def get_champignons(
    diametre_max_chapeau: float = Query(None, description="Diamètre maximum du chapeau pour filtrer les champignons"),
    nombre_resultats: int = Query(20, description="Nombre de résultats à afficher")
):
    # Filtrer les champignons en fonction du diamètre maximum du chapeau si le paramètre est fourni
    if diametre_max_chapeau is not None:
        champignons_filtres = Champignons[Champignons['Diametre maximum du chapeau'] <= diametre_max_chapeau]
    else:
        champignons_filtres = Champignons

    # Limiter le nombre de résultats à afficher
    champignons_limite = champignons_filtres.head(nombre_resultats)

    # Convertir les valeurs de la DataFrame en un format JSON compatible
    champignons_json = json.loads(champignons_limite.to_json(orient="records"))

    return champignons_json



