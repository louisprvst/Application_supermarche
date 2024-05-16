# ============================================================================================================================================================
#                                                     contrôleur de l'application numéro une
#                                                   Fait par FARDEL Mathéïs et DEMOL Alexis
#=============================================================================================================================================================

import sys
import os
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
from modeleApplication import ProjetModel
from vueApplication import MainWindow, NewProjetDialog

# -------------------------------------------------------------- classe Contrôleur ---------------------------------------------------------------------------
class Controller:
    def __init__(self):
        self.model = ProjetModel()
        self.view = MainWindow()
        
        # Connecter les actions de la vue aux méthodes du contrôleur
        self.view.action_new_projet.triggered.connect(self.creer_nouveau_projet)
        self.view.action_engresitrer_projet.triggered.connect(self.enregistrer_projet)
        
        # Charger les données initiales du Modèle
        self.charger_produits()

    # Charger les produits du JSON pour les ajouter à la vue
    def charger_produits(self):
        chemin_json = os.path.join(sys.path[0], "liste_produits.json")
        produits = self.model.charger_produits(chemin_json)
        self.view.listeObjets(produits)

    # Créer un nouveau projet
    def creer_nouveau_projet(self):
        dialogue = NewProjetDialog()
        if dialogue.exec():
            details_projet = dialogue.getProjetDetails()
            chemin_image, _ = QFileDialog.getOpenFileName(self.view, "Charger le plan", "", "Images (*.png *.jpg *.jpeg *.gif)")
            if chemin_image:
                details_projet['chemin_image'] = chemin_image
                self.view.plateau.chargerImage(chemin_image)
                self.view.plateau.createQuadrillage(details_projet['lgn'], details_projet['cols'], details_projet['dimX'], details_projet['dimY'])
                self.view.afficherInfosMagasin(details_projet)
                self.model.mettre_a_jour_details(details_projet)
                QMessageBox.information(self.view, "Nouveau Projet", "Nouveau projet créé avec succès !")

    # Enregistrer un projet
    def enregistrer_projet(self):
        chemin_fichier, _ = QFileDialog.getSaveFileName(self.view, "Enregistrer le projet", "", "JSON Files (*.json)")
        if chemin_fichier:
            success, message = self.model.sauvegarder_projet(chemin_fichier)
            if success:
                QMessageBox.information(self.view, "Enregistrement du Projet", message)
            else:
                QMessageBox.critical(self.view, "Enregistrement du Projet", message)


# ------------------------------------------------------------------ MAIN ----------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.view.show()
    sys.exit(app.exec())
