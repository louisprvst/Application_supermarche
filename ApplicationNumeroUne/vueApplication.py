# ============================================================================================================================================================
#                                                     Vue de l'application numéro une
#                                                   Fait par FARDEL Mathéïs et DEMOL Alexis
#=============================================================================================================================================================

import sys, os
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QDialog, QDialogButtonBox, QDockWidget, QLineEdit, QTextEdit, QCalendarWidget, QTreeWidget, QTreeWidgetItem, QPushButton, QFileDialog, QMessageBox, QMenu, QApplication, QApplication
from PyQt6.QtGui import QPixmap, QIcon, QPainter, QPen, QFont, QAction
from PyQt6.QtCore import Qt, pyqtSignal

# --------------------------------------------------------------- classe Image ------------------------------------------------------------------------------
class Image(QLabel):
    def __init__(self, chemin: str):
        super().__init__()
        self.image = QPixmap(chemin)
        self.setPixmap(self.image)

# -------------------------------------------------------------- classe Plateau -----------------------------------------------------------------------------
class Plateau(QWidget):
    def __init__(self):
        super().__init__()
        self.articleSelected = pyqtSignal(str)
        layout = QVBoxLayout(self)
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        self.pixmap = QPixmap()
        self.image_label.mousePressEvent = self.ouvrirFenetre

    # Permet de charger le plan du client
    def chargerImage(self, chemin: str):
        if chemin:
            self.pixmap.load(chemin)
            self.pixmap = self.pixmap.scaled(1200, 720, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(self.pixmap)

    # Permet de créer le quadrillage sur le plan
    def createQuadrillage(self, lgn, cols, dimX, dimY):
        if not self.pixmap.isNull():
            painter = QPainter(self.pixmap)
            pen = QPen(Qt.GlobalColor.black)
            pen.setWidth(1)
            painter.setPen(pen)
            larg = self.pixmap.width()
            haut = self.pixmap.height()
            cellLarge = larg / cols
            cellHaut = haut / lgn
            for i in range(1, cols):
                x = int(dimX + i * cellLarge)
                painter.drawLine(x, dimY, x, haut + dimY)
            for j in range(1, lgn):
                y = int(dimY + j * cellHaut)
                painter.drawLine(dimX, y, larg + dimX, y)
            painter.end()
            self.image_label.setPixmap(self.pixmap)

    # Permet d'ouvrir la fênetre (EVENT DE TEST)
    def ouvrirFenetre(self, event):
        fenetreModal = FenetreTexte("\n Légumes")
        fenetreModal.exec()


# --------------------------------------------------- classe FenetreText (EVENT TEST) ---------------------------------------------------------------
class FenetreTexte(QDialog):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("Fenetre texte test")
        label = QLabel(f"Contenu du rayon: {text}")
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
        self.setFixedSize(800, 400)

# ------------------------------------------------------- classe NewProjetDialog ------------------------------------------------------------------------
class NewProjetDialog(QDialog):
    def __init__(self, parent=None):
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

    #Permet d'obtenir les détails du projet
    def getProjetDetails(self):
        return {
            'nomProjet': self.nomProjet.text(),
            'auteurProjet': self.auteurProjet.text(),
            'dateCreationProjet': self.dateCreationProjet.selectedDate().toString(Qt.DateFormat.ISODate),
            'nomMagasin': self.nomMagasin.text(),
            'adresse_magasin': self.adresseMagasin.text(),
            'lgn': int(self.lgn.text()),
            'cols': int(self.cols.text()),
            'dimX': int(self.dimX.text()),
            'dimY': int(self.dimY.text())
        }

# -------------------------------------------------------------- classe MainWindow ----------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application supermarché")
        self.setWindowIcon(QIcon(sys.path[0] + '/icones/logo_app.png'))
        self.setGeometry(100, 100, 500, 300)
        
        #Contenu du dock de gauche avec les articles
        self.dock_articles = QDockWidget('Articles', self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_articles)
        self.dock_articles.setFixedWidth(350)
        self.objets_widget = QTreeWidget()
        self.objets_widget.setHeaderHidden(True)
        self.objets_widget.setIndentation(20)
        self.objets_widget.setStyleSheet("QTreeWidget::item { margin-top: 10px; margin-bottom: 10px; }")
        self.dock_articles.setWidget(self.objets_widget)
        
        #Contenu du plan dans le widget central
        self.plateau = Plateau()
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.plateau)
        self.setCentralWidget(central_widget)
        
        #Contenu du dock de droite avec les informations du magasin
        self.dock_info_magasin = QDockWidget('Informations Magasin', self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_info_magasin)
        self.dock_info_magasin.setMaximumWidth(250)
        self.info_magasin_texte = QTextEdit(self)
        self.dock_info_magasin.setWidget(self.info_magasin_texte)
        
        #Contenu des boutons Valider/Modifier du dock de droite
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        self.modifier_button = QPushButton("Modifier")
        self.valider_button = QPushButton("Valider")
        self.valider_button.hide()
        button_layout.addWidget(self.modifier_button)
        button_layout.addWidget(self.valider_button)
        self.dock_info_magasin.setTitleBarWidget(button_container)
        #Signaux pour les boutons
        self.modifier_button.clicked.connect(self.activerModificationInfosMagasin)
        self.valider_button.clicked.connect(self.desactiverModificationInfosMagasin)
        self.info_magasin_texte.setReadOnly(True)
        
        #Barre de menu du haut contenant "Fichier"
        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu('&Fichier')
        #Action pour créer un nouveau projet
        self.action_new_projet = QAction('Nouveau Projet', self)
        self.action_new_projet.setShortcut('Ctrl+N')
        menu_fichier.addAction(self.action_new_projet)
        #Action pour enregistrer un projet
        self.action_engresitrer_projet = QAction('Enregister un Projet', self)
        self.action_engresitrer_projet.setShortcut('Ctrl+S')
        menu_fichier.addAction(self.action_engresitrer_projet)
        #Action pour ouvrir un projet
        self.action_ouvrir_projet = QAction('Ouvrir Projet', self)
        self.action_ouvrir_projet.setShortcut('Ctrl+O')
        menu_fichier.addAction(self.action_ouvrir_projet)
        
        #Show(tailleMax de l'écran)
        self.showMaximized()

    #Permet d'afficher les différents Articles (+ amélioration Police)
    def listeObjets(self, data):
        for categorie, articles in data.items():
            parent = QTreeWidgetItem([categorie])
            parent.setFont(0, QFont('Arial', 14, QFont.Weight.Bold))
            for article in articles:
                child = QTreeWidgetItem([article])
                child.setFont(0, QFont('Arial', 12))
                parent.addChild(child)
            self.objets_widget.addTopLevelItem(parent)

    #Contenu de l'affichage des informations du magasin
    def afficherInfosMagasin(self, details_projet):
        info_magasin = f"Nom du magasin: {details_projet['nomMagasin']}\n"
        info_magasin += f"Adresse du magasin: {details_projet['adresse_magasin']}\n"
        info_magasin += f"Auteur du projet: {details_projet['auteurProjet']}\n"
        info_magasin += f"Date de création du projet: {details_projet['dateCreationProjet']}\n"
        self.info_magasin_texte.setText(info_magasin)
    
    #Permet au clic de "Modifier" de pouvoir modifier le contenu      
    def activerModificationInfosMagasin(self):
        self.info_magasin_texte.setReadOnly(False)
        self.modifier_button.hide()
        self.valider_button.show()

    #Permet au clic de "Valider" de ne plus pouvoir modifier le contenu
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