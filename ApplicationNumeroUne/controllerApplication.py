# ============================================================================================================================================================
#                                                     contrôleur de l'application numéro une
#                                                   Fait par FARDEL Mathéïs et DEMOL Alexis
#=============================================================================================================================================================

import sys, json
import os
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap
from modeleApplication import ProjetModel
from vueApplication import MainWindow, NewProjetDialog

# -------------------------------------------------------------- classe Contrôleur ---------------------------------------------------------------------------
class Controller:
    def __init__(self):
        self.model = ProjetModel()
        self.view = MainWindow()
        self.chemin_projet = None
        self.plan_modifiable = True
        
        # Connecter les actions de la vue aux méthodes du contrôleur
        self.view.action_new_projet.triggered.connect(self.creer_nouveau_projet)
        self.view.action_engresitrer_projet.triggered.connect(self.enregistrer_projet)
        self.view.action_ouvrir_projet.triggered.connect(self.ouvrir_projet)
        self.view.valider_button.clicked.connect(self.sauvegarder_infos_magasin)
        self.view.action_supprimer_projet.triggered.connect(self.supprimer_projet)
        self.view.ajouter_colonnes_button.clicked.connect(self.ajouter_colonnes)
        self.view.retirer_colonnes_button.clicked.connect(self.retirer_colonnes)
        self.view.ajouter_lignes_button.clicked.connect(self.ajouter_lignes)
        self.view.retirer_lignes_button.clicked.connect(self.retirer_lignes)
        
        # permet de connecter le signal de séléction d'objet sur le plateau pour désactiver les modif 
        self.view.plateau.articleSelected.connect(self.desactiver_modifications)
        self.view.plateau.caseUpdated.connect(self.mettre_a_jour_case_dans_modele)
        
        # Charger les données initiales du Modèle
        self.produits = self.charger_produits()

    # Charger les produits du JSON pour les ajouter à la vue
    def charger_produits(self):
        chemin_json = os.path.join(sys.path[0], "liste_produits.json")
        return self.model.charger_produits(chemin_json)

    # Créer un nouveau projet
    def creer_nouveau_projet(self):
        self.reinitialiser_plateau()
        dialogue = NewProjetDialog(self.produits)
        if dialogue.exec():
            details_projet = dialogue.getProjetDetails()
            if details_projet:
                chemin_image, _ = QFileDialog.getOpenFileName(self.view, "Charger le plan", "", "Images (*.png *.jpg *.jpeg *.gif)")
                if chemin_image:
                    details_projet['chemin_image'] = chemin_image
                    lgn = details_projet.get('lgn', 10) or 10
                    cols = details_projet.get('cols', 10) or 10
                    details_projet['lgn'] = lgn
                    details_projet['cols'] = cols
                    self.view.plateau.chargerImage(chemin_image)
                    self.view.plateau.createQuadrillage(lgn, cols, details_projet['dimX'], details_projet['dimY'])
                    self.view.afficherInfosMagasin(details_projet)
                    self.model.mettre_a_jour_details(details_projet)
                    self.view.listeObjets(details_projet['produits_selectionnes'])
                    self.view.plateau.cols = cols
                    self.view.plateau.lgn = lgn
                    self.plan_modifiable = True  
                    self.activer_modifications()  
                    QMessageBox.information(self.view, "Nouveau Projet", "Nouveau projet créé avec succès !")

   # Enregistrer un projet
    def enregistrer_projet(self):
        if not self.model.details_projet:
            QMessageBox.warning(self.view, "Enregistrement du Projet", "Il n'y a aucun projet à enregistrer !")
            return
        
       # Convertir les clés des cases en listes pour JSON
        produits_dans_cases_list_keys = {str(k): v for k, v in self.view.plateau.produits_dans_cases.items()}
        chemin_image = self.model.details_projet.pop('chemin_image', None)  # Retirer chemin_image avant de sauvegarder
        
        # Sélectionner le dossier où enregistrer les données du projet
        chemin_dossier = QFileDialog.getExistingDirectory(self.view, "Sélectionner un dossier pour enregistrer le projet")
        if chemin_dossier:
            nom_projet = self.model.details_projet.get('nomProjet', 'projet_sans_nom')
            chemin_projet = os.path.join(chemin_dossier, nom_projet)
            
            # Créer le dossier pour le projet
            os.makedirs(chemin_projet, exist_ok=True)
            
            # Sauvegarder les informations du projet dans un fichier JSON
            chemin_fichier_projet = os.path.join(chemin_projet, f"{nom_projet}.json")
            message = self.model.sauvegarder_projet(chemin_fichier_projet)
            
            # Copier l'image du plan dans le dossier du projet
        if chemin_image:
            chemin_image_cible = os.path.join(chemin_projet, 'plan' + os.path.splitext(chemin_image)[1])
            if os.path.exists(chemin_image):
                with open(chemin_image, 'rb') as lecture:
                    with open(chemin_image_cible, 'wb') as ecriture:
                        ecriture.write(lecture.read())
            
            # Sauvegarder les données de positionnement
            chemin_fichier_positionnement = os.path.join(chemin_projet, 'positionnement.json')
            try:
                with open(chemin_fichier_positionnement, 'w') as f:
                    json.dump(produits_dans_cases_list_keys, f, indent=4)
                QMessageBox.information(self.view, "Enregistrement du Projet", message + " et les données de positionnement ont été enregistrées.")
            except Exception as e:
                QMessageBox.critical(self.view, "Enregistrement du Projet", f"Erreur lors de l'enregistrement des données de positionnement: {e}")

    # Ouvrir un projet
    def ouvrir_projet(self):
        chemin_dossier = QFileDialog.getExistingDirectory(self.view, "Sélectionner le dossier du projet à ouvrir")
        if chemin_dossier:
            self.chemin_projet = chemin_dossier
            try:
                nom_projet = os.path.basename(chemin_dossier)
                chemin_fichier_projet = os.path.join(chemin_dossier, f"{nom_projet}.json")
                chemin_fichier_positionnement = os.path.join(chemin_dossier, 'positionnement.json')
            
                self.reinitialiser_plateau()
                details_projet = self.model.charger_projet(chemin_fichier_projet)
                produits_dans_cases = self.model.charger_projet(chemin_fichier_positionnement)
                details_projet['produits_dans_cases'] = produits_dans_cases

                chemin_image = os.path.join(chemin_dossier, 'plan' + os.path.splitext(details_projet.get('chemin_image', ''))[1])
                details_projet['chemin_image'] = chemin_image

                self.view.plateau.chargerImage(chemin_image)
                self.view.plateau.createQuadrillage(details_projet['lgn'], details_projet['cols'], details_projet['dimX'], details_projet['dimY'])
                self.view.afficherInfosMagasin(details_projet)
                self.model.mettre_a_jour_details(details_projet)
                self.view.listeObjets(details_projet['produits_selectionnes'])
            
                # Convertir les clés des cases de chaînes en tuples
                produits_dans_cases = {eval(k): v for k, v in produits_dans_cases.items()}
                self.view.plateau.produits_dans_cases = produits_dans_cases
                for case in self.view.plateau.produits_dans_cases:
                    self.view.plateau.mettre_a_jour_case(case, afficher_message=False)
                
                self.plan_modifiable = True  
                self.desactiver_modifications()  
                QMessageBox.information(self.view, "Ouverture du Projet", "Projet ouvert avec succès.")
            except IOError as e:
                QMessageBox.critical(self.view, "Ouverture du Projet", str(e))


    # fonction qui permet de réinitialiser les informations sur le plateau 
    def reinitialiser_plateau(self):
        self.view.plateau.reinitialiser_plateau()
        self.view.info_magasin_texte.clear()
        self.view.objets_widget.clear()
        self.model.details_projet = {}

    # Fonction qui permet de supprimer un projet             
    def supprimer_projet(self):
        msg = QMessageBox(self.view)
        msg.setWindowTitle("Supprimer Projet")
        msg.setText("Voulez-vous vraiment supprimer le projet ? Attention cette action est irréversible !")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        yes = msg.button(QMessageBox.StandardButton.Yes)
        no = msg.button(QMessageBox.StandardButton.No)
        yes.setText("Oui")
        no.setText("Non")
        verif = msg.exec()

        if verif == QMessageBox.StandardButton.No:
            return None
        if verif == QMessageBox.StandardButton.Yes:
            # Supprimer le dossier du projet
            if self.chemin_projet and os.path.exists(self.chemin_projet):
                for racine, dossiers, fichiers in os.walk(self.chemin_projet, topdown=False):
                    for name in fichiers:
                        os.remove(os.path.join(racine, name))
                    for name in dossiers:
                        os.rmdir(os.path.join(racine, name))
                os.rmdir(self.chemin_projet)
            
            self.reinitialiser_plateau()
            self.plan_modifiable = True  
            self.activer_modifications()  
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

    # Fonction pour ajouter des colonnes au plan 
    def ajouter_colonnes(self):
        if self.plan_modifiable:
            self.view.plateau.cols = self.view.plateau.cols + 1
            self.view.plateau.rechargerImage()
            self.model.details_projet['cols'] = self.view.plateau.cols

    # Fonction pour retirer des colonnes au plan 
    def retirer_colonnes(self):
        if self.plan_modifiable:
            cols, success = self.model.retirer_colonnes(self.view.plateau.cols)
            if success:
                self.view.plateau.cols = cols
                self.view.plateau.rechargerImage()
                self.model.details_projet['cols'] = self.view.plateau.cols
            else:
                self.view.afficher_message_erreur("Impossible de réduire les colonnes", "Le nombre de colonnes ne peut pas être inférieur.")

    # Fonction pour ajouter des lignes au plan 
    def ajouter_lignes(self):
        if self.plan_modifiable:
            self.view.plateau.lgn += 1
            self.view.plateau.rechargerImage()
            self.model.details_projet['lgn'] = self.view.plateau.lgn

    # Fonction pour retirer des lignes au plan 
    def retirer_lignes(self):
        if self.plan_modifiable:
            if self.view.plateau.lgn > 1:
                self.view.plateau.lgn = self.view.plateau.lgn - 1
                self.view.plateau.rechargerImage()
                self.model.details_projet['lgn'] = self.view.plateau.lgn
            else:
                self.view.afficher_message_erreur("Impossible de réduire les lignes", "Le nombre de lignes ne peut pas être inférieur.")

    # nous permet de mettre toute les informations des cases dans notre model 
    def mettre_a_jour_case_dans_modele(self, case, produits):
        produits_dans_cases = {}
        for k, v in self.view.plateau.produits_dans_cases.items():
            produits_dans_cases[str(k)] = v
        self.model.details_projet['produits_dans_cases'] = produits_dans_cases


    # permet de désactiver les modif dans le plan 
    def desactiver_modifications(self):
        self.plan_modifiable = False
        self.view.ajouter_colonnes_button.setEnabled(False)
        self.view.retirer_colonnes_button.setEnabled(False)
        self.view.ajouter_lignes_button.setEnabled(False)
        self.view.retirer_lignes_button.setEnabled(False)

    # permet d'activer les modif dans le plan
    def activer_modifications(self):
        self.plan_modifiable = True
        self.view.ajouter_colonnes_button.setEnabled(True)
        self.view.retirer_colonnes_button.setEnabled(True)
        self.view.ajouter_lignes_button.setEnabled(True)
        self.view.retirer_lignes_button.setEnabled(True)
        
# ------------------------------------------------------------------ MAIN ----------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.view.show()
    sys.exit(app.exec())
