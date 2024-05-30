# ============================================================================================================================================================
#                                                     Modèle de l'application numéro une
#                                                   Fait par FARDEL Mathéïs et DEMOL Alexis
#=============================================================================================================================================================

import json
import os 

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
        
    def charger_projet(self, chemin_fichier):
        try:
            with open(chemin_fichier, 'r') as f:
                details_projet = json.load(f)
            return details_projet
        except Exception as e:
            raise IOError(f"Erreur lors du chargement du projet: {e}")
        
    def supp_projet(self, chemin_fichier):
        try:
            if os.path.exists(chemin_fichier):
                os.remove(chemin_fichier)
                return True, "Projet supprimé avec succès."
            else:
                return False, "Le fichier de projet n'existe pas."
        except Exception as e:
            raise IOError(f"Erreur lors de la suppression du projet: {e}")

    def retirer_colonnes(self, cols):
        if cols > 1:
            return cols - 1, True
        return cols, False