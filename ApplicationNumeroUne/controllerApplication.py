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
        self.view.action_ouvrir_projet.triggered.connect(self.ouvrir_projet)
        self.view.valider_button.clicked.connect(self.sauvegarder_infos_magasin)
        self.view.action_supprimer_projet.triggered.connect(self.supprimer_projet)
        
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
        if not self.model.details_projet:
            QMessageBox.warning(self.view, "Enregistrement du Projet", "Il n'y a aucun projet à enregistrer !")
            return
        
        chemin_fichier, _ = QFileDialog.getSaveFileName(self.view, "Enregistrer le projet", "", "JSON Files (*.json)")
        if chemin_fichier:
            success, message = self.model.sauvegarder_projet(chemin_fichier)
            if success:
                QMessageBox.information(self.view, "Enregistrement du Projet", message)
            else:
                QMessageBox.critical(self.view, "Enregistrement du Projet", message)
               
    #Ouvrir un projet 
    def ouvrir_projet(self):
        chemin_fichier, _ = QFileDialog.getOpenFileName(self.view, "Ouvrir le projet", "", "JSON Files (*.json)")
        print(f"Tentative d'ouverture du fichier: {chemin_fichier}")  # Débogage
        if chemin_fichier:
            try:
                details_projet = self.model.charger_projet(chemin_fichier)
                print(f"Contenu du projet chargé: {details_projet}")  # Débogage
                self.view.plateau.chargerImage(details_projet['chemin_image'])
                self.view.plateau.createQuadrillage(details_projet['lgn'], details_projet['cols'], details_projet['dimX'], details_projet['dimY'])
                self.view.afficherInfosMagasin(details_projet)
                self.model.mettre_a_jour_details(details_projet)
                QMessageBox.information(self.view, "Ouverture du Projet", "Projet ouvert avec succès.")
            except IOError as e:
                QMessageBox.critical(self.view, "Ouverture du Projet", str(e))

    # Fonction qui permet de supprimer un projet             
    def supprimer_projet(self):
        msg = QMessageBox(self.view)
        msg.setWindowTitle("Supprimer Projet")
        msg.setText("Voulez-vous vraiment supprimer le projet ? Attention cette action est irréversible !")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        yes = msg.button(QMessageBox.StandardButton.Yes)
        no = msg.button(QMessageBox.StandardButton.No)
        yes.setText("Oui") # Met le bouton "Yes" en "Oui"
        no.setText("Non")
        verif = msg.exec()

        if verif == QMessageBox.StandardButton.No:

            return None 
        if verif == QMessageBox.StandardButton.Yes:

            self.model.details_projet = {}
            self.view.plateau.image_label.clear()  # permet de vider l'image du plateau
            self.view.info_magasin_texte.clear()  # permet de vider les infos du magasin
            QMessageBox.information(self.view, "Suppression du Projet", "Le projet a été supprimé avec succès.")

    # Sauvegarder les informations du magasin
    def sauvegarder_infos_magasin(self):
        infos_magasin = self.view.info_magasin_texte.toPlainText().split('\n')
        details_projet = {
            'nomMagasin': infos_magasin[0].replace("Nom du magasin: ", ""),
            'adresse_magasin': infos_magasin[1].replace("Adresse du magasin: ", ""),
            'auteurProjet': infos_magasin[2].replace("Auteur du projet: ", ""),
            'dateCreationProjet': infos_magasin[3].replace("Date de création du projet: ", "")
        }
        self.model.mettre_a_jour_details(details_projet)
        QMessageBox.information(self.view, "Informations Magasin", "Informations du magasin enregistrées avec succès.")

# ------------------------------------------------------------------ MAIN ----------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.view.show()
    sys.exit(app.exec())
