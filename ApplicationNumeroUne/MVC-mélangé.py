
# ============================================================================================================================================================
#                                   ASSEMBLAGE DE TEST.PY ET VUE.PY (à répartir dans M,V,C ensuite)
#                                           Fait par FARDEL Mathéïs et DEMOL Alexis
#=============================================================================================================================================================

import json
import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDialog, QFileDialog, QDialogButtonBox, QMessageBox, QDockWidget, QLineEdit, QTextEdit, QCalendarWidget, QTreeWidget, QTreeWidgetItem, QPushButton
from PyQt6.QtGui import QPixmap, QIcon, QAction, QPainter, QPen, QFont
from PyQt6.QtCore import Qt, pyqtSignal

# -------------------------------------- classe herité de QLabel permettant d'afficher une image (repris du cours) -------------------------------------------
class Image(QLabel):

    def __init__(self, chemin: str):
        '''Constructeur de la classe'''

        # appel au constructeur de la classe mère
        super().__init__() 
        
        self.image = QPixmap(chemin)
        self.setPixmap(self.image)
# ----------------------------------- classe Plateau pour gérer l'affichage de l'image et l'ajout d'un quadrillage --------------------------------------------
class Plateau(QWidget):
    def __init__(self):
        super().__init__()

        self.articleSelected = pyqtSignal(str) 

        layout = QVBoxLayout(self)
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        self.pixmap = QPixmap()  

        # connecter le clic a une fonction 
        self.image_label.mousePressEvent = self.ouvrirFenetre

    # Charger une image et la redimensionner
    def chargerImage(self, chemin: str):
        if chemin:
            self.pixmap.load(chemin)
            self.pixmap = self.pixmap.scaled(1200, 720, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(self.pixmap)
        else:
            print("Chemin de l'image non valide:", chemin)

    # créer un quadrillage avec les lignes, colonnes et les dimensions X et Y
    # J'ai du recréer la fonction pour créer le quadrillage pour permettre de créer le projet puis afficher le quadrillage, avec l'ancienne fonction cela ne voulait pas, j'ai du donc changer de maniére
    def createQuadrillage(self, lgn, cols, dimX, dimY):
        if not self.pixmap.isNull():
            painter = QPainter(self.pixmap)
            pen = QPen(Qt.GlobalColor.black)
            pen.setWidth(1)
            painter.setPen(pen)
            
            larg = self.pixmap.width()
            haut = self.pixmap.height()
            
            # permet de calculer les cases 
            cellLarge = larg / cols
            cellHaut = haut / lgn
            
            # lignes verticales
            for i in range(1, cols):
                x = int(dimX + i * cellLarge)
                painter.drawLine(x, dimY, x, haut + dimY)
            
            # lignes horizontales
            for j in range(1, lgn):
                y = int(dimY + j * cellHaut)
                painter.drawLine(dimX, y, larg + dimX, y)
            
            painter.end()
            self.image_label.setPixmap(self.pixmap)
        else:
            print("Aucune image chargée.")

    # ouverture fenetre 
    def ouvrirFenetre(self, event):
        fenetreModal = FenetreTexte("\n Légumes")
        fenetreModal.exec()

# ----------------------------------------- classe FenetreTexte pour afficher une fenêtre modale avec un texte ----------------------------------------------------
class FenetreTexte(QDialog):
    def __init__(self, text):
        super().__init__()

        self.setWindowTitle("Fenetre texte test")
        label = QLabel(f"Contenu du rayon: {text}")

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
        self.setFixedSize(800, 400)


# ---------------------------------------------------- classe NewProjetDialog pour créer un nouveau projet --------------------------------------------------------
class NewProjetDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Nouveau Projet")
        layout = QVBoxLayout(self)
        
        self.nomProjet = QLineEdit()
        self.auteurProjet = QLineEdit()
        self.dateCreationProjet = QCalendarWidget()
        self.nomMagasin = QLineEdit()
        self.adresseMagasin = QLineEdit()
        self.lgn = QLineEdit()
        self.cols = QLineEdit()
        self.dimX = QLineEdit()
        self.dimY = QLineEdit()
        
        layout.addWidget(QLabel("Nom du projet:"))
        layout.addWidget(self.nomProjet)
        layout.addWidget(QLabel("Auteur du projet:"))
        layout.addWidget(self.auteurProjet)
        layout.addWidget(QLabel("Date de création du projet:"))
        layout.addWidget(self.dateCreationProjet)
        layout.addWidget(QLabel("Nom du magasin:"))
        layout.addWidget(self.nomMagasin)
        layout.addWidget(QLabel("Adresse du magasin:"))
        layout.addWidget(self.adresseMagasin)
        layout.addWidget(QLabel("Nombre de lignes du quadrillage:"))
        layout.addWidget(self.lgn)
        layout.addWidget(QLabel("Nombre de colonnes du quadrillage:"))
        layout.addWidget(self.cols)
        layout.addWidget(QLabel("Dimensions x:"))
        layout.addWidget(self.dimX)
        layout.addWidget(QLabel("Dimensions y:"))
        layout.addWidget(self.dimY)
        layout.addWidget(QLabel("Dimensions x,y a 0 seront exactement en haut a gauche de l'image."))

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, Qt.Orientation.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # Récupérer les détails du projet
    def getProjetDetails(self):
        return {
            'nomProjet': self.nomProjet.text(),
            'auteurProjet': self.auteurProjet.text(),
            'dateCreationProjet': self.dateCreationProjet.selectedDate().toString(Qt.DateFormat.ISODate),
            'nomMagasin': self.nomMagasin.text(),
            'adresse_magasin': self.adresseMagasin.text(),
            'lgn':  int(self.lgn.text()),
            'cols': int(self.cols.text()),
            'dimX': int(self.dimX.text()),
            'dimY': int(self.dimY.text())
        }

#---------------------------------------------------------------- vue de l'application ------------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self, chemin: str = None):
        super().__init__()
        self.__chemin = chemin
        self.details_projet = {}
        self.setWindowTitle("Application supermarché")
        self.setWindowIcon(QIcon(sys.path[0] + '/icones/cadie.jpg'))
        self.setGeometry(100, 100, 500, 300)
        
        # Charger les données du JSON
        chemin_json = os.path.join(sys.path[0], "liste_produits.json")
        with open(chemin_json, 'r') as f:
            self.data = json.load(f)

        # Ajout d'un premier dock pour les articles 
        self.dock_articles = QDockWidget('Articles', self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_articles)
        self.dock_articles.setFixedWidth(350)
        
        self.objets_widget = QTreeWidget()
        self.objets_widget.setHeaderHidden(True)
        self.objets_widget.setIndentation(20)
        self.objets_widget.setStyleSheet("QTreeWidget::item { margin-top: 10px; margin-bottom: 10px; }")
        self.listeObjets(self.data)
        self.dock_articles.setWidget(self.objets_widget)

        self.plateau = Plateau() # crée l'instance du plateau
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.plateau)
        self.setCentralWidget(central_widget) # met le plateau en screen principale

        # Ajout d'un deuxième dock pour les info du magasin sur la droite
        self.dock_info_magasin = QDockWidget('Informations Magasin', self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_info_magasin)
        self.dock_info_magasin.setMaximumWidth(250)
        self.info_magasin_texte = QTextEdit(self)
        self.dock_info_magasin.setWidget(self.info_magasin_texte)

        # Conteneur pour les boutons "Modifier" et "Valider"
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)

        # Bouton modifier et valider dans le deuxième dock pour les infos du magasin 
        self.modifier_button = QPushButton("Modifier")
        self.valider_button = QPushButton("Valider")
        self.valider_button.hide()  # Cacher le bouton Valider au début

        button_layout.addWidget(self.modifier_button)
        button_layout.addWidget(self.valider_button)

        self.dock_info_magasin.setTitleBarWidget(button_container)

        # Signaux pour activer les modifications du QTextEdit
        self.modifier_button.clicked.connect(self.activerModificationInfosMagasin)
        self.valider_button.clicked.connect(self.desactiverModificationInfosMagasin)

        # mettre le texte en lecture seul 
        self.info_magasin_texte.setReadOnly(True)  

        # ajout d'une barre d'outils 
        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu('&Fichier')

        #Action de "Nouveau Projet" et "Enregistrer Projet"
        action_new_projet = QAction('Nouveau Projet', self)
        action_new_projet.setShortcut('Ctrl+N')
        action_new_projet.triggered.connect(self.createNewProject)
        menu_fichier.addAction(action_new_projet)
        action_engresitrer_projet = QAction('Enregister un Projet', self)
        action_engresitrer_projet.setShortcut('Ctrl+S')
        action_engresitrer_projet.triggered.connect(self.enregistrerProjet)
        menu_fichier.addAction(action_engresitrer_projet)
        action_ouvrir_projet = QAction('Ouvrir Projet', self)
        action_ouvrir_projet.setShortcut('Ctrl+O')
        menu_fichier.addAction(action_ouvrir_projet)
        action_ouvrir_projet.triggered.connect(self.ouvrirProjet)

        self.showMaximized()

    #permet de créer la liste des articles en déroulant
    def listeObjets(self, data):
        for categorie, articles in data.items():
            parent = QTreeWidgetItem([categorie])
            parent.setFont(0, QFont('Arial', 14, QFont.Weight.Bold))
            for article in articles:
                child = QTreeWidgetItem([article])
                child.setFont(0, QFont('Arial', 12))
                parent.addChild(child)
            self.objets_widget.addTopLevelItem(parent)


    # permet de charger l'image
    def chargerImage(self, chemin: str):
        if chemin:
            self.plateau.chargerImage(chemin)
            print("Image chargée avec succès:", chemin)
        else:
            print("Chemin de l'image non valide:", chemin)

    # permet de créer un nouveau projet
    def createNewProject(self):
        dialogue = NewProjetDialog(self)
        if dialogue.exec():
            self.details_projet = dialogue.getProjetDetails()
            chemin_image, _ = QFileDialog.getOpenFileName(self, "Charger le plan", "", "Images (*.png *.jpg *.jpeg *.gif)")
            if chemin_image:
                self.details_projet['chemin_image'] = chemin_image
                self.chargerImage(chemin_image) # charger l'image quand on a créer le projet 
                self.changDimQuadrillage(self.details_projet) # changer les dimensions du quadrillage après la création du projet 
                self.afficherInfosMagasin(self.details_projet)  # permet d'afficher les infos sur le magasins
                QMessageBox.information(self, "Nouveau Projet", "Nouveau projet créé avec succès !")

    # permet de changer la dimension du quadrillage
    def changDimQuadrillage(self, details_projet):
        self.plateau.createQuadrillage(details_projet['lgn'], details_projet['cols'], details_projet['dimX'], details_projet['dimY'])

    # permet d'afficher les infos du magasin
    def afficherInfosMagasin(self, details_projet):
        info_magasin = f"Nom du magasin: {details_projet['nomMagasin']}\n"
        info_magasin += f"Adresse du magasin: {details_projet['adresse_magasin']}\n"
        info_magasin += f"Auteur du projet: {details_projet['auteurProjet']}\n"
        info_magasin += f"Date de création du projet: {details_projet['dateCreationProjet']}\n"
        self.info_magasin_texte.setText(info_magasin)

    # Fonction qui permet l'enregistrement des informations du projet en format json
    def enregistrerProjet(self):
        if not self.details_projet:
            QMessageBox.warning(self, "Enregistrement du Projet !", "Il y a aucun projet à enregistrer !")
            return

        chemin_fichier, _ = QFileDialog.getSaveFileName(self, "Enregistrer le projet", "", "JSON Files (*.json)")
        if chemin_fichier:
            try: # gére les exceptions (comme en java avec les try)
                with open(chemin_fichier, 'w') as f:
                    json.dump(self.details_projet, f, indent=4)
                QMessageBox.information(self, "Enregistrement du Projet", "Projet enregistré avec succès.")
            except Exception as e: # gére les soucis qu'il peut y avoir en cas d'erreur, et envoie un Message Box si c'est good ou non 
                QMessageBox.critical(self, "Enregistrement du Projet", f"Erreur lors de l'enregistrement du projet: {e}")

    def ouvrirProjet(self):
        chemin_fichier, _ = QFileDialog.getOpenFileName(self, "Ouvrir le projet", "", "JSON Files (*.json)")
        if chemin_fichier:
            try: # gére les exceptions (comme en java avec les try)
                with open(chemin_fichier, 'r') as f:
                    self.details_projet = json.load(f)
                self.chargerImage(self.details_projet['chemin_image'])
                self.changDimQuadrillage(self.details_projet)
                self.afficherInfosMagasin(self.details_projet)
                QMessageBox.information(self, "Ouverture du Projet", "Projet ouvert avec succès.")
            except Exception as e: # gére les soucis qu'il peut y avoir en cas d'erreur, et envoie un Message Box si c'est good ou non 
                QMessageBox.critical(self, "Ouverture du Projet", f"Erreur lors de l'ouverture du projet: {e}")


    # permettre la modification du docker avec les informations du magasins
    def activerModificationInfosMagasin(self):
        self.info_magasin_texte.setReadOnly(False)
        self.modifier_button.hide()
        self.valider_button.show()

    # retirer la permission de modification du docker avec les infos du magasin
    def desactiverModificationInfosMagasin(self):
        self.info_magasin_texte.setReadOnly(True)
        self.modifier_button.show()
        self.valider_button.hide()


# ------------------------------------------------------------------- MAIN POUR TESTER ------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
