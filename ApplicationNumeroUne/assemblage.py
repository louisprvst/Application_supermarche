import json
import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDialog, QFileDialog, QDialogButtonBox, QMessageBox, QToolBar, QDockWidget, QMenu,  QLineEdit, QPushButton, QTextEdit, QCalendarWidget
from PyQt6.QtGui import QPixmap, QIcon, QAction, QPainter, QPen
from PyQt6.QtCore import Qt, QPoint, pyqtSignal

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

        articleSelected = pyqtSignal(str) 

        layout = QVBoxLayout(self)
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        self.pixmap = QPixmap()  

        # connecter le clic a une fonction 
        self.image_label.mousePressEvent = self.ouvrirFenetre

    def chargerImage(self, chemin: str):
        if chemin:
            self.pixmap.load(chemin)
            self.pixmap = self.pixmap.scaled(1200, 720, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)  # Permet de bien redimensionner l'image / Normalement adapté avec une bonne partie des tailles d'écran
            self.image_label.setPixmap(self.pixmap)
        else:
            print("Chemin de l'image non valide:", chemin)

    # créer un quadrillage avec les lignes, colonnes et les dimensions X et Y
    # J'ai du recréer la fonction pour créer le quadrillage pour permettre de créer le projet puis afficher le quadrillage, avec l'ancienne fonction cela ne voulait pas, j'ai du donc changer de maniére
    def createQuadrillage(self, lgn, cols, dimX, dimY):
        if not self.pixmap.isNull():  # on vérifie d'abord si le pixmap peut etre valide
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
        self.setWindowTitle("Application supermarché")
        self.setWindowIcon(QIcon(sys.path[0] + '/icones/cadie.jpg'))
        self.setGeometry(100, 100, 500, 300)
        
        chemin_json = os.path.join(sys.path[0], "liste_produits.json")
        with open(chemin_json, 'r') as f:
            data = json.load(f)

        # Ajout d'un premier dock pour les articles 
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

        # Ajout d'un deuxième dock pour les info du magasin sur la droite
        dock_info_magasin = QDockWidget('Informations Magasin')
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock_info_magasin)
        dock_info_magasin.setMaximumWidth(200)

        self.info_magasin_texte = QTextEdit()  
        dock_info_magasin.setWidget(self.info_magasin_texte)  

        # Bouton modifier dans le deuxiéme docker pour les infos du magasins 
        modifier_button = QPushButton("Modifier")
        dock_info_magasin.setTitleBarWidget(modifier_button)
        modifier_button.clicked.connect(self.activerModificationInfosMagasin)

        # mettre le texte en lecture seul 
        self.info_magasin_texte.setReadOnly(True)  

        # ajout d'une barre d'outils 
        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu('&Fichier')

        action_new_projet = QAction('Nouveau Projet', self)
        action_new_projet.setShortcut('Ctrl+N')
        action_new_projet.triggered.connect(self.createNewProject)
        menu_fichier.addAction(action_new_projet)
        action_engresitrer_projet = QAction('Enregister un Projet', self)
        action_engresitrer_projet.setShortcut('Ctrl+S')
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
                self.chargerImage(chemin_image) # charger l'image quand on a créer le projet 
                self.changDimQuadrillage(details_projet) # changer les dimensions du quadrillage après la création du projet 
                self.afficherInfosMagasin(details_projet)  # permet d'afficher les infos sur le magasins
                QMessageBox.information(self, "Nouveau Projet", "Nouveau projet créé avec succès !")

    # changer les dimensions du quadrillage avec les dimensions spécifié avec la création du projet 
    def changDimQuadrillage(self, details_projet):
        self.plateau.createQuadrillage(details_projet['lgn'], details_projet['cols'], details_projet['dimX'], details_projet['dimY'])

    # Fonction qui nous permet d'afficher les informations utile du magasins 
    def afficherInfosMagasin(self, details_projet):
        info_magasin = f"Nom du magasin: {details_projet['nomMagasin']}\n"
        info_magasin += f"Adresse du magasin: {details_projet['adresse_magasin']}\n"
        info_magasin += f"Auteur du projet: {details_projet['auteurProjet']}\n"
        info_magasin += f"Date de création du projet: {details_projet['dateCreationProjet']}\n"
        self.info_magasin_texte.setText(info_magasin)

    # fonction de test pour enregister le projet (Pas fonctionnel)
    def enregistrer(self):
        boite = QFileDialog()
        chemin, validation = boite.getSaveFileName(directory = sys.path[0])
        if validation:
            self.__chemin = chemin

    # permettre la modification du docker avec les informations du magasins
    def activerModificationInfosMagasin(self):
        if self.info_magasin_texte.isReadOnly():
            self.info_magasin_texte.setReadOnly(False)
        else:
            self.info_magasin_texte.setReadOnly(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())