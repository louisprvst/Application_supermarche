# ============================================================================================================================================================
#                                                     Modèle de l'application numéro une
#                                                   Fait par FARDEL Mathéïs et DEMOL Alexis
#=============================================================================================================================================================

import json

# ----------------------------------------------------------- classe ProjetModel -----------------------------------------------------------------------------
class ProjetModel:
    def __init__(self):
        self.details_projet = {}

    # Permet de charger les produits 
    def charger_produits(self, chemin_fichier):
        try:
            with open(chemin_fichier, 'r') as f:
                produits = json.load(f)
            return produits
        except Exception as e:
            print(f"Erreur lors du chargement des produits: {e}")
            return {}

    # Permet de mettre à jour les détails du projet
    def mettre_a_jour_details(self, details):
        self.details_projet.update(details)

    # Permet de sauvegarder notre projet
    def sauvegarder_projet(self, chemin_fichier):
        try:
            with open(chemin_fichier, 'w') as f:
                json.dump(self.details_projet, f, indent=4)
            return True, "Projet enregistré avec succès."
        except Exception as e:
            return False, f"Erreur lors de l'enregistrement du projet: {e}"
