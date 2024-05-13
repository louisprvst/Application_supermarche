# Code provisoire assemblage et modifications du code test.py et de la vue fait par Mathéïs

# Alexis Demol TPB - Version du 12-05-24
# Assemblage avec le code de Mathéïs

import json
import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDialog, QFileDialog, QDialogButtonBox, QMessageBox, QToolBar, QDockWidget, QMenu,  QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap, QIcon, QAction, QPainter, QPen
from PyQt6.QtCore import Qt, QPoint


# --- class widget: hérite de QLabel ------------------------------------------
class Image(QLabel):

    def __init__(self, chemin: str):
        '''Constructeur de la classe'''

        # appel au constructeur de la classe mère
        super().__init__() 
        
        self.image = QPixmap(chemin)
        self.setPixmap(self.image)
        
class Plateau(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.pixmap = QPixmap()
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        # connecter le clic a une fonction 
        self.image_label.mousePressEvent = self.ouvrirFenetre

    def chargerImage(self, chemin: str):
        if chemin:
            self.pixmap.load(chemin)
            self.image_label.setPixmap(self.pixmap)

    # créer un quadrillage avec les lignes, colonnes et les dimensions X et Y
    # J'ai du recréer la fonction pour créer le quadrillage pour permettre de créer le projet puis afficher le quadrillage, avec l'ancienne fonction cela ne voulait pas, j'ai du donc changer de maniére
    def createQuadrillage(self, lgn, cols, dimX, dimY):

        # permet de dessiner le quadrillage 
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

    # ouverture fenetre 
    def ouvrirFenetre(self, event):
        fenetreModal = FenetreTexte("\n Légumes")
        fenetreModal.exec()


class FenetreTexte(QDialog):
    def __init__(self, text):
        super().__init__()

        self.setWindowTitle("Fenetre texte test")
        label = QLabel(f"Contenu du rayon: {text}")

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
        self.setFixedSize(800, 400)


# Nous permet de créer un nouveau projet
class NewProjetDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Nouveau Projet")
        layout = QVBoxLayout(self)
        
        self.nomProjet = QLineEdit()
        self.auteurProjet = QLineEdit()
        self.dateCreationProjet = QLineEdit()
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

    def getProjetDetails(self):
        return {
            'nomProjet': self.nomProjet.text(),
            'auteurProjet': self.auteurProjet.text(),
            'dateCreationProjet': self.dateCreationProjet.text(),
            'nomMagasin': self.nomMagasin.text(),
            'adresse_magasin': self.adresseMagasin.text(),
            'lgn':  int(self.lgn.text()),
            'cols': int(self.cols.text()),
            'dimX': int(self.dimX.text()),
            'dimY': int(self.dimY.text())
        }

# Vue principale de l'appli
class MainWindow(QMainWindow):
    def __init__(self, chemin: str = None):
        super().__init__()
        self.__chemin = chemin
        self.setWindowTitle("Application supermarché")
        self.setWindowIcon(QIcon(sys.path[0] + '/icones/cadie.jpg'))
        self.setGeometry(100, 100, 500, 300)
        
        chemin_json = os.path.join(sys.path[0], "liste_produits.json")
        with open(chemin_json, 'r') as f:
            data = json.load(f)

        dock_articles = QDockWidget('Articles')
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_articles)
        dock_articles.setMaximumWidth(200)

        widget_menu_articles = QWidget()
        layout_menu_articles = QVBoxLayout(widget_menu_articles)

        menu_categorie = QMenu("Catégories", self)
        for categorie, articles in data.items():
            sous_menu_categorie = menu_categorie.addMenu(categorie)
            for article in articles:
                action = QAction(article, self)
                sous_menu_categorie.addAction(action)

        layout_menu_articles.addWidget(menu_categorie)
        dock_articles.setWidget(widget_menu_articles)

        self.plateau = Plateau() # crée l'instance du plateau
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.plateau)
        self.setCentralWidget(central_widget) # met le plateau en screen principale

        # ajout d'une barre d'outils 
        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu('&Fichier')

        action_new_projet = QAction('Nouveau Projet', self)
        action_new_projet.triggered.connect(self.createNewProject)
        menu_fichier.addAction(action_new_projet)
        action_engresitrer_projet = QAction('Enregister un Projet', self)
        menu_fichier.addAction(action_engresitrer_projet)

        self.showMaximized()

    # Permet de charger l'image 
    def chargerImage(self, chemin: str):
        if chemin:
            self.plateau.chargerImage(chemin)
            print("Image chargée avec succès:", chemin)
        else:
            print("Chemin de l'image non valide:", chemin)

    # créer un nouveau projet 
    def createNewProject(self):
        dialogue = NewProjetDialog(self)
        if dialogue.exec():
            details_projet = dialogue.getProjetDetails()
            chemin_image, _ = QFileDialog.getOpenFileName(self, "Charger le plan", "", "Images (*.png *.jpg *.jpeg *.gif)")
            if chemin_image:
                self.chargerImage(chemin_image)
                self.changDimQuadrillage(details_projet)
                QMessageBox.information(self, "Nouveau Projet", "Nouveau projet créé avec succès !")

    # changer les dimensions du quadrillage avec les dimensions spécifié avec la création du projet 
    def changDimQuadrillage(self, details_projet):
        self.plateau.createQuadrillage(details_projet['lgn'], details_projet['cols'], details_projet['dimX'], details_projet['dimY'])

    def enregistrer(self):
        boite = QFileDialog()
        chemin, validation = boite.getSaveFileName(directory = sys.path[0])
        if validation:
            self.__chemin = chemin

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())