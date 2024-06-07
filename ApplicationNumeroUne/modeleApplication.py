# ============================================================================================================================================================
#                                                     Modèle de l'application numéro une
#                                                   Fait par FARDEL Mathéïs et DEMOL Alexis
#=============================================================================================================================================================

import json
import os 

# ----------------------------------------------------------- classe ProjetModel -----------------------------------------------------------------------------
class ProjetModel:
    """
    Classe ProjetModel pour gérer certaines fonctions du controller et de la vue.

    Résumé des attributs et méthodes de la class:

    Attributs:
    ----------
    -details_projet : Dictionnaire contenant les détails du projet actuel.

    Méthodes:
    -------
    -charger_produits(chemin_fichier): Permet de charger les produits avec un fichier jsons.
    -ajouter_produits_speciaux(produits): Permet d'ajouter Entrée du magasin et sortie du magasin
    -mettre_a_jour_details(details): Permet de mettre à jour les détails du projet.
    -sauvegarder_projet(chemin_fichier): Permet de sauvegarder notre projet dans un json.
    -charger_projet(chemin_fichier): Charge les détails d'un projet à partir d'un fichier JSON.
    -supp_projet(chemin_fichier): Supprime le fichier de projet spécifié.

    """

    # Initialise le ProjetModel avec un dictionnaire qui est vide pour les détails du projet.
    def __init__(self):
        self.details_projet = {}
 
    def charger_produits(self, chemin_fichier):
        """
        Permet de charger les produits avec un fichier jsons.

        Parametre:
        ----------
        chemin_fichier : Chemin vers le fichier JSON contenant les produits.

        Returns:
        -------
        Dictionnaire des produits chargés.

        """
        try:
            with open(chemin_fichier, 'r') as f:
                produits = json.load(f)
            return produits
        except Exception as e:
            print(f"Erreur lors du chargement des produits: {e}")
            return {}
    
    def ajouter_produits_speciaux(self, produits):
        """
        Permet d'ajouter Entrée du magasin et sortie du magasin.

        Parametre:
        ----------
        produits : Dictionnaire des produits.

        """
        if "Entree / Sortie" not in produits:
            produits["Entree / Sortie"] = []
        if "Entree du magasin" not in produits["Entree / Sortie"]:
            produits["Entree / Sortie"].append("Entree du magasin")
        if "Sortie du magasin" not in produits["Entree / Sortie"]:
            produits["Entree / Sortie"].append("Sortie du magasin")

    def mettre_a_jour_details(self, details):
        """
        Permet de mettre à jour les détails du projet.

        Parametre:
        ----------
        details : Dictionnaire contenant les nouvelles informations du projet.

        """
        self.details_projet.update(details)

    def sauvegarder_projet(self, chemin_fichier):
        """
        Permet de sauvegarder notre projet dans un json.

        Parametre:
        ----------
        chemin_fichier : Chemin vers le fichier où sauvegarder le projet.

        Returns:
        -------
        Un tuple contenant un booléen indiquant le succès et un message.

        """
        try:
            with open(chemin_fichier, 'w') as f:
                json.dump(self.details_projet, f, indent=4)
            return True, "Projet enregistré avec succès."
        except Exception as e:
            return False, f"Erreur lors de l'enregistrement du projet: {e}"
        
    def charger_projet(self, chemin_fichier):
        """
        Charge les détails d'un projet à partir d'un fichier JSON.

        Parametre:
        ----------
        chemin_fichier : Chemin vers le fichier du projet à charger.

        Returns:
        -------
        Dictionnaire des détails du projet ou une erreur si le projet n'a pas été charger. 

        """
        try:
            with open(chemin_fichier, 'r') as f:
                details_projet = json.load(f)
            return details_projet
        except Exception as e:
            raise IOError(f"Erreur lors du chargement du projet: {e}")
        
    def supp_projet(self, chemin_fichier):
        """
        Supprime le fichier de projet spécifié.

        Parametre:
        ----------
        chemin_fichier : Chemin vers le fichier du projet à supprimer.

        Returns:
        -------
        Un tuple contenant un booléen indiquant le succès et un message ou une erreur lors de la suppression du projet

        """
        try:
            if os.path.exists(chemin_fichier):
                os.remove(chemin_fichier)
                return True, "Projet supprimé avec succès."
            else:
                return False, "Le fichier de projet n'existe pas."
        except Exception as e:
            raise IOError(f"Erreur lors de la suppression du projet: {e}")
