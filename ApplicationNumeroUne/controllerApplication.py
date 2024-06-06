# ============================================================================================================================================================
#                                                     contrôleur de l'application numéro une
#                                                   Fait par FARDEL Mathéïs et DEMOL Alexis
#=============================================================================================================================================================

import sys
import os
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from modeleApplication import ProjetModel
from vueApplication import MainWindow, NewProjetDialog

# -------------------------------------------------------------- classe Contrôleur ---------------------------------------------------------------------------
class Controller:
    def __init__(self):
        self.model = ProjetModel()
        self.view = MainWindow()
        self.chemin_projet = None
        self.plan_modifiable = True
        self.dossier_projet = None
        
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

                    # Ajouter "Entrée" et "Sortie" aux produits sélectionnés
                    produits_selectionnes = details_projet['produits_selectionnes']
                    self.model.ajouter_produits_speciaux(produits_selectionnes)
                    self.view.listeObjets(produits_selectionnes)

                    self.view.plateau.cols = cols
                    self.view.plateau.lgn = lgn
                    self.plan_modifiable = True  
                    self.activer_modifications()  
                    QMessageBox.information(self.view, "Nouveau Projet", "Nouveau projet créé avec succès !")

    def enregistrer_projet(self):
        if not self.model.details_projet:
            QMessageBox.warning(self.view, "Enregistrement du Projet", "Il n'y a aucun projet à enregistrer !")
            return
        
        # Vérifier que "Entrée" et "Sortie" sont placés sur le plan
        if not self.verifier_entree_sortie():
            QMessageBox.warning(self.view, "Enregistrement du Projet", "Vous devez placer 'Entrée' et 'Sortie' sur le plan avant d'enregistrer le projet.")
            return
        
        # Convertir les clés des cases en listes pour JSON
        produits_dans_cases_list_keys = {str(k): v for k, v in self.view.plateau.produits_dans_cases.items()}
        self.model.details_projet['produits_dans_cases'] = produits_dans_cases_list_keys

        if self.dossier_projet:
            chemin_projet = self.dossier_projet
        else:
            # Sélectionner le dossier où enregistrer les données du projet
            chemin_dossier = QFileDialog.getExistingDirectory(self.view, "Sélectionner un dossier pour enregistrer le projet")
            if chemin_dossier:
                nom_projet = self.model.details_projet.get('nomProjet', 'projet_sans_nom')
                if not nom_projet:
                    nom_projet = "projet_sans_nom"
                chemin_projet = os.path.join(chemin_dossier, nom_projet)

                # Créer le dossier pour le projet
                os.makedirs(chemin_projet, exist_ok=True)

                # Copier l'image dans le dossier du projet
                chemin_image_source = self.model.details_projet['chemin_image']
                nom_image = os.path.basename(chemin_image_source)
                chemin_image_cible = os.path.join(chemin_projet, nom_image)
                
                try:
                    with open(chemin_image_source, 'rb') as src_file:
                        with open(chemin_image_cible, 'wb') as dest_file:
                            dest_file.write(src_file.read())
                    # Mettre à jour le chemin de l'image dans le fichier JSON pour utiliser un chemin relatif
                    self.model.details_projet['chemin_image'] = nom_image
                except Exception as e:
                    QMessageBox.critical(self.view, "Enregistrement du Projet", f"Erreur lors de la copie de l'image: {e}")
                    return

                self.dossier_projet = chemin_projet

        # Sauvegarder les informations du projet dans un fichier JSON
        nom_projet = self.model.details_projet.get('nomProjet', 'projet_sans_nom')
        chemin_fichier_projet = os.path.join(self.dossier_projet, f"{nom_projet}.json")
        success, message = self.model.sauvegarder_projet(chemin_fichier_projet)
        if success:
            if not self.dossier_projet:
                self.dossier_projet = chemin_projet
            QMessageBox.information(self.view, "Enregistrement du Projet", message)
        else:
            QMessageBox.critical(self.view, "Enregistrement du Projet", message)


   
    def ouvrir_projet(self):
        chemin_dossier = QFileDialog.getExistingDirectory(self.view, "Sélectionner le dossier du projet à ouvrir")
        if chemin_dossier:
            try:
                nom_projet = os.path.basename(chemin_dossier)
                chemin_fichier_projet = os.path.join(chemin_dossier, f"{nom_projet}.json")
                
                details_projet = self.model.charger_projet(chemin_fichier_projet)
                chemin_image = os.path.join(chemin_dossier, details_projet['chemin_image'])
                details_projet['chemin_image'] = chemin_image

                self.view.plateau.chargerImage(chemin_image)
                self.view.plateau.createQuadrillage(details_projet['lgn'], details_projet['cols'], details_projet['dimX'], details_projet['dimY'])
                self.view.afficherInfosMagasin(details_projet)
                self.model.mettre_a_jour_details(details_projet)
                self.view.listeObjets(details_projet['produits_selectionnes'])

                # Convertir les clés des cases de chaînes en tuples
                produits_dans_cases = {eval(k): v for k, v in details_projet.get('produits_dans_cases', {}).items()}
                self.view.plateau.produits_dans_cases = produits_dans_cases
                for case in self.view.plateau.produits_dans_cases:
                    self.view.plateau.mettre_a_jour_case(case, afficher_message=False)

                self.chemin_projet = chemin_fichier_projet
                self.dossier_projet = chemin_dossier

                self.plan_modifiable = True  
                self.desactiver_modifications()  

                QMessageBox.information(self.view, "Ouverture du Projet", "Projet ouvert avec succès.")
            except IOError as e:
                QMessageBox.critical(self.view, "Ouverture du Projet", str(e))



    # Vérifier si "Entrée" et "Sortie" sont placés sur le plan
    def verifier_entree_sortie(self):
        produits_dans_cases = self.view.plateau.produits_dans_cases
        produits_places = [produit for produits in produits_dans_cases.values() for produit in produits]
        return "Entrée du magasin" in produits_places and "Sortie du magasin" in produits_places
    
    # fonction qui permet de réinitialiser les informations sur le plateau 
    def reinitialiser_plateau(self):
        self.view.plateau.reinitialiser_plateau()
        self.view.info_magasin_texte.clear()
        self.view.objets_widget.clear()
        self.model.details_projet = {}
        self.chemin_projet = None
        self.dossier_projet = None
        self.plan_modifiable = True  
        self.activer_modifications()

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
            if self.chemin_projet:
                    dossier_projet = os.path.dirname(self.chemin_projet)
                    for racine, dossiers, fichiers in os.walk(dossier_projet, topdown=False):
                        for name in fichiers:
                            os.remove(os.path.join(racine, name))
                        for name in dossiers:
                            os.rmdir(os.path.join(racine, name))
                    os.rmdir(dossier_projet)

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
        