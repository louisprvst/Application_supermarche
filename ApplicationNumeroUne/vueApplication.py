# ============================================================================================================================================================
#                                                     Vue de l'application numéro une
#                                                   Fait par FARDEL Mathéïs et DEMOL Alexis
#=============================================================================================================================================================

import sys, os
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QDialog, QDialogButtonBox, QDockWidget, QLineEdit, QTextEdit, QCalendarWidget, QTreeWidget, QTreeWidgetItem, QPushButton, QFileDialog, QMessageBox, QMenu, QApplication, QScrollArea, QCheckBox, QToolBar, QHBoxLayout
from PyQt6.QtGui import QPixmap, QIcon, QPainter, QPen, QFont, QAction, QMouseEvent
from PyQt6.QtCore import Qt, pyqtSignal

# --------------------------------------------------------------- classe Image ------------------------------------------------------------------------------
class Image(QLabel):
    def __init__(self, chemin: str):
        super().__init__()
        self.image = QPixmap(chemin)
        self.setPixmap(self.image)

# -------------------------------------------------------------- classe Plateau -----------------------------------------------------------------------------
class Plateau(QWidget):
    articleSelected = pyqtSignal(str) 
    caseUpdated = pyqtSignal(tuple, list) 

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.pixmap = QPixmap()
        self.image_label.mousePressEvent = self.ouvrirFenetre
        self.caseQuadrillage = []  # liste pour mettre toute les pos des cases 
        self.produits_dans_cases = {}  # dictionnaire pour stocker les produits par case
        self.objet_selectionne = None 
        self.lgn = 0
        self.cols = 0
        self.dimX = 0
        self.dimY = 0
        self.chemin_image = None  
    
    def setObjetSelectionne(self, objet): 
        self.objet_selectionne = objet
        self.articleSelected.emit(objet)  

    def chargerImage(self, chemin: str):
        if chemin:
            self.chemin_image = chemin  
            self.pixmap.load(chemin)
            self.pixmap = self.pixmap.scaled(900, 700, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(self.pixmap)
            self.image_label.setFixedSize(900, 700) 

    # fonction pour recharger l'image et réinitialise son quadrillage 
    def rechargerImage(self):
        if self.chemin_image:
            self.pixmap.load(self.chemin_image)
            self.pixmap = self.pixmap.scaled(900, 700, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(self.pixmap)
            self.createQuadrillage(self.lgn, self.cols, self.dimX, self.dimY)

    def createQuadrillage(self, lgn, cols, dimX, dimY):
        self.lgn = lgn
        self.cols = cols
        self.dimX = dimX
        self.dimY = dimY

        if not self.pixmap.isNull():
            painter = QPainter(self.pixmap)
            pen = QPen(Qt.GlobalColor.black)
            pen.setWidth(1)
            painter.setPen(pen)
            larg = self.pixmap.width()
            haut = self.pixmap.height()
            cellLarge = larg / cols
            cellHaut = haut / lgn

            self.caseQuadrillage = []  # permet d'effacer les dernières pos 

            for i in range(cols):
                for j in range(lgn):
                    x1 = int(dimX + i * cellLarge)
                    y1 = int(dimY + j * cellHaut)
                    x2 = int(dimX + (i + 1) * cellLarge)
                    y2 = int(dimY + (j + 1) * cellHaut)
                    self.caseQuadrillage.append((x1, y1, x2, y2))
                    painter.drawRect(x1, y1, x2 - x1, y2 - y1)
            painter.end()
            self.image_label.setPixmap(self.pixmap)
            
            for case, produits in self.produits_dans_cases.items():
                self.mettre_a_jour_case(case, afficher_message=False)
    
    # Permet d'ouvrir la fenêtre (EVENT DE TEST)
    def ouvrirFenetre(self, event): 
        posClick = event.pos()
        for (x1, y1, x2, y2) in self.caseQuadrillage:
            if x1 <= posClick.x() <= x2 and y1 <= posClick.y() <= y2:
                case = (x1, y1, x2, y2)
                if case in self.produits_dans_cases:
                    self.afficher_produits_dans_case(case, avec_suppression=True)
                else:
                    self.placer_objet_dans_case(case)
                break
            
    # Permet de placer un objet dans une case
    def placer_objet_dans_case(self, case):  
        if self.objet_selectionne:
            produit = self.objet_selectionne
            if case not in self.produits_dans_cases:
                self.produits_dans_cases[case] = []
            self.produits_dans_cases[case].append(produit)
            self.mettre_a_jour_case(case)
            self.caseUpdated.emit(case, self.produits_dans_cases[case])  
            self.objet_selectionne = None

    # Permet de mettre à jour une case afin d'ajouter un objet dedans et que ça soit à jour
    def mettre_a_jour_case(self, case, afficher_message=True): 
        x1, y1, x2, y2 = case
        painter = QPainter(self.pixmap)
        pen = QPen(Qt.GlobalColor.red)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(x1, y1, x2 - x1, y2 - y1)
        painter.end()
        self.image_label.setPixmap(self.pixmap)
        if afficher_message:
            contenu = "\n".join(self.produits_dans_cases[case])
            QMessageBox.information(self, "Produit placé", f"Produit dans la case ({x1}, {y1}):\n{contenu}")

    # Permet d'afficher le produit présent dans la case en cliquant dessus
    def afficher_produits_dans_case(self, case, avec_suppression=False): 
        x1, y1, x2, y2 = case
        produits = self.produits_dans_cases[case]
        contenu = "\n".join(produits)
        
        # Création de la fenêtre modale
        fenetre = QDialog(self)
        fenetre.setWindowTitle("Produits dans la case")
        layout = QVBoxLayout()
        label = QLabel(f"Produits dans la case ({x1}, {y1}):\n{contenu}")
        layout.addWidget(label)
        
        if avec_suppression:
            bouton_supprimer = QPushButton("Supprimer le contenu")
            bouton_supprimer.clicked.connect(self.creation_gestionnaire_suppression_contenu_case(case, fenetre))
            layout.addWidget(bouton_supprimer)
        
        fenetre.setLayout(layout)
        fenetre.exec()

    def creation_gestionnaire_suppression_contenu_case(self, case, fenetre):
        def gestion():
            self.supprimer_contenu_case(case, fenetre)
        return gestion
        
    def redessiner_case(self, case):
        x1, y1, x2, y2 = case
        painter = QPainter(self.pixmap)
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(x1, y1, x2 - x1, y2 - y1)
        painter.end()
        self.image_label.setPixmap(self.pixmap)


    def supprimer_contenu_case(self, case, fenetre):
        if case in self.produits_dans_cases:
            del self.produits_dans_cases[case]
            self.redessiner_case(case)
            self.caseUpdated.emit(case, [])  
            fenetre.accept()
            QMessageBox.information(self, "Suppression", f"Le contenu de la case ({case[0]}, {case[1]}) a été supprimé.")
    
    def reinitialiser_plateau(self):
        self.image_label.clear()
        self.produits_dans_cases.clear()
        self.caseQuadrillage.clear()
        self.pixmap = QPixmap()
        self.image_label.setPixmap(self.pixmap)
# --------------------------------------------------- classe FenetreText (EVENT TEST) ---------------------------------------------------------------
class FenetreTexte(QDialog):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("Fenetre texte test")
        label = QLabel(text)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
        self.setFixedSize(800, 400)

# ------------------------------------------------------- classe SelectionProduitsDialog ------------------------------------------------------------------------
class SelectionProduitsDialog(QDialog):
    def __init__(self, produits, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sélection des produits")
        self.produits = produits
        layout = QVBoxLayout(self)
        
        self.checkboxes = {}
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        for categorie, articles in produits.items():
            categorie_label = QLabel(categorie)
            categorie_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
            scroll_layout.addWidget(categorie_label)
            for article in articles:
                checkbox = QCheckBox(article)
                scroll_layout.addWidget(checkbox)
                self.checkboxes[article] = checkbox
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, Qt.Orientation.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    # Récupérer les produits sélectionnés
    def get_selected_produits(self):
        selected_produits = {}
        for article, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                categorie = self.find_categorie(article)
                if categorie not in selected_produits:
                    selected_produits[categorie] = []
                selected_produits[categorie].append(article)
        return selected_produits
    
    #Permet de savoir la catégorie d'un produit
    def find_categorie(self, article):
        for categorie, articles in self.produits.items():
            if article in articles:
                return categorie
        return None

# ------------------------------------------------------- classe NewProjetDialog ------------------------------------------------------------------------
class NewProjetDialog(QDialog):
    def __init__(self, produits, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nouveau Projet")
        self.produits = produits
        self.produits_selectionnes = {}
        
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
        self.choisir_produits_button = QPushButton("Choisir les produits disponibles")
        self.choisir_produits_button.clicked.connect(self.ouvrir_selection_produits)
        
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
        layout.addWidget(QLabel("Dimensions x,y à 0 seront exactement en haut à gauche de l'image."))
        layout.addWidget(self.choisir_produits_button)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, Qt.Orientation.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    #Permet d'ouvrir la page pour sélectionner ses produits
    def ouvrir_selection_produits(self):
        dialog = SelectionProduitsDialog(self.produits, self)
        if dialog.exec():
            self.produits_selectionnes = dialog.get_selected_produits()
            
    # Récupérer les détails du projet
    def getProjetDetails(self):
        try:
            return {
                'nomProjet': self.nomProjet.text(),
                'auteurProjet': self.auteurProjet.text(),
                'dateCreationProjet': self.dateCreationProjet.selectedDate().toString(Qt.DateFormat.ISODate),
                'nomMagasin': self.nomMagasin.text(),
                'adresse_magasin': self.adresseMagasin.text(),
                'lgn': int(self.lgn.text()) if self.lgn.text() else 0,
                'cols': int(self.cols.text()) if self.cols.text() else 0,
                'dimX': int(self.dimX.text()) if self.dimX.text() else 0,
                'dimY': int(self.dimY.text()) if self.dimY.text() else 0,
                'produits_selectionnes': self.produits_selectionnes
            }
        except ValueError as e:
            QMessageBox.critical(self, "Erreur", "Veuillez remplir correctement tous les champs.")
            return None

# -------------------------------------------------------------- classe MainWindow ----------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application supermarché")
        self.setWindowIcon(QIcon(sys.path[0] + '/icones/logo_app.png'))
        self.setGeometry(100, 100, 500, 300)
        
        # Contenu du dock de gauche avec les articles
        self.dock_articles = QDockWidget('Articles', self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_articles)
        self.dock_articles.setFixedWidth(250)
        self.objets_widget = QTreeWidget()
        self.objets_widget.setHeaderHidden(True)
        self.objets_widget.setIndentation(20)
        self.objets_widget.setStyleSheet("QTreeWidget::item { margin-top: 10px; margin-bottom: 10px; }")
        self.dock_articles.setWidget(self.objets_widget)
        
        # Connecter l'événement de clic pour les éléments du QTreeWidget
        self.objets_widget.itemClicked.connect(self.selectionner_objet)

        # Attribut pour stocker l'objet sélectionné
        self.objet_selectionne = None
        
        # Contenu du plan dans le widget central
        self.plateau = Plateau()
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.plateau)

        # Ajout des boutons "+" et "-"
        self.boutons_layout = QHBoxLayout()
        self.ajouter_colonnes_button = QPushButton("+ Colonne")
        self.retirer_colonnes_button = QPushButton("- Colonne")
        self.ajouter_lignes_button = QPushButton("+ Ligne")
        self.retirer_lignes_button = QPushButton("- Ligne")
        self.boutons_layout.addWidget(self.ajouter_colonnes_button)
        self.boutons_layout.addWidget(self.retirer_colonnes_button)
        self.boutons_layout.addWidget(self.ajouter_lignes_button)
        self.boutons_layout.addWidget(self.retirer_lignes_button)

        layout.addLayout(self.boutons_layout)
        self.setCentralWidget(central_widget)
        
        # Connecter les boutons aux fonctions correspondantes
        self.ajouter_colonnes_button.clicked.connect(self.ajouter_colonnes)
        self.retirer_colonnes_button.clicked.connect(self.retirer_colonnes)
        self.ajouter_lignes_button.clicked.connect(self.ajouter_lignes)
        self.retirer_lignes_button.clicked.connect(self.retirer_lignes)
        
        # Connecter le signal de sélection d'objet au plateau
        self.objets_widget.itemClicked.connect(self.selectionner_objet)
        
        # Contenu du dock de droite avec les informations du magasin
        self.dock_info_magasin = QDockWidget('Informations Magasin', self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_info_magasin)
        self.dock_info_magasin.setFixedWidth(250)
        self.info_magasin_texte = QTextEdit(self)
        self.dock_info_magasin.setWidget(self.info_magasin_texte)
        
        # Contenu des boutons Valider/Modifier du dock de droite
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        self.modifier_button = QPushButton("Modifier")
        self.valider_button = QPushButton("Valider")
        self.valider_button.hide()
        button_layout.addWidget(self.modifier_button)
        button_layout.addWidget(self.valider_button)
        self.dock_info_magasin.setTitleBarWidget(button_container)
        
        # Signaux pour les boutons
        self.modifier_button.clicked.connect(self.activerModificationInfosMagasin)
        self.valider_button.clicked.connect(self.desactiverModificationInfosMagasin)

        # Définir l'état initial
        self.info_magasin_texte.setReadOnly(True)
        self.valider_button.hide()
        
        # Barre de menu du haut contenant "Fichier"
        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu('&Fichier')
        
        # Action pour créer un nouveau projet
        self.action_new_projet = QAction(QIcon(sys.path[0] + '/icones/plus.png'), 'Nouveau Projet', self)
        self.action_new_projet.setShortcut('Ctrl+N')
        menu_fichier.addAction(self.action_new_projet)
        
        # Action pour enregistrer un projet
        self.action_engresitrer_projet = QAction(QIcon(sys.path[0] + '/icones/save.png'),'Enregistrer un Projet', self)
        self.action_engresitrer_projet.setShortcut('Ctrl+S')
        menu_fichier.addAction(self.action_engresitrer_projet)
        
        # Action pour ouvrir un projet
        self.action_ouvrir_projet = QAction(QIcon(sys.path[0] + '/icones/open.png'),'Ouvrir un Projet', self)
        self.action_ouvrir_projet.setShortcut('Ctrl+O')
        menu_fichier.addAction(self.action_ouvrir_projet)
        
        # Action pour supprimer un projet
        self.action_supprimer_projet = QAction(QIcon(sys.path[0] + '/icones/delete.png'),'Supprimer un Projet', self)
        self.action_supprimer_projet.setShortcut('Ctrl+DELETE') 
        menu_fichier.addAction(self.action_supprimer_projet)
        
        # barre menu pour les affichages 
        menu_affichage = menu_bar.addMenu('&Affichage')
        
        # le sous menu pour les thèmes 
        menu_themes = menu_affichage.addMenu("Thèmes")
        self.action_theme_clair = QAction("Thème clair", self)
        self.action_theme_sombre = QAction("Thème sombre", self)
        menu_themes.addAction(self.action_theme_clair)
        menu_themes.addAction(self.action_theme_sombre)
        self.action_theme_clair.triggered.connect(self.theme_clair)
        self.action_theme_sombre.triggered.connect(self.theme_sombre)

        #Tool Bar 
        toolbar = QToolBar('Tool Bar')
        self.addToolBar(toolbar)
        
        toolbar.addAction(self.action_new_projet)
        toolbar.addSeparator()
        toolbar.addAction(self.action_engresitrer_projet)
        toolbar.addSeparator()
        toolbar.addAction(self.action_ouvrir_projet)
        toolbar.addSeparator()
        toolbar.addAction(self.action_supprimer_projet)
        toolbar.addSeparator()
        
        # Afficher la fenêtre maximisée
        self.showMaximized()
        
    # permet d'ajouter des colonnes dans le quadrillage après avoir créer le projet 
    def ajouter_colonnes(self):
        self.plateau.cols = self.plateau.cols + 1
        self.plateau.rechargerImage()

    # permet de retirer des colonnes dans le quadrillage après avoir créer le projet 
    def retirer_colonnes(self):
        if self.plateau.cols > 1:
            self.plateau.cols = self.plateau.cols - 1
            self.plateau.rechargerImage()
        else:
            self.afficher_message_erreur("Impossible de réduire les colonnes", "Le nombre de colonnes ne peut pas être inférieur.")

    # permet d'ajouter des lignes dans le quadrillage après avoir créer le projet 
    def ajouter_lignes(self):
        self.plateau.lgn = self.plateau.lgn + 1
        self.plateau.rechargerImage()

    # permet de retirer des lignes dans le quadrillage après avoir créer le projet 
    def retirer_lignes(self):
        if self.plateau.lgn > 1:
            self.plateau.lgn = self.plateau.lgn - 1
            self.plateau.rechargerImage()
        else:
            self.afficher_message_erreur("Impossible de réduire les lignes", "Le nombre de lignes ne peut pas être inférieur.")

    # affiche un mess d'erreur (peut etre changer dans le model ?)
    def afficher_message_erreur(self, titre, message):
        QMessageBox.critical(self, titre, message)

    # Permet de pouvoir sélectionner un objet
    def selectionner_objet(self, item, column):  
        self.objet_selectionne = item.text(0) 
        self.plateau.setObjetSelectionne(self.objet_selectionne) 
        self.plateau.articleSelected.emit(self.objet_selectionne)  

    # Permet d'afficher les différents Articles (+ amélioration Police)
    def listeObjets(self, produits):
        self.objets_widget.clear()
        for categorie, articles in produits.items():
            parent = QTreeWidgetItem([categorie])
            parent.setFont(0, QFont('Arial', 14, QFont.Weight.Bold))
            for article in articles:
                child = QTreeWidgetItem([article])
                child.setFont(0, QFont('Arial', 12))
                parent.addChild(child)
            self.objets_widget.addTopLevelItem(parent)

    # Contenu de l'affichage des informations du magasin
    def afficherInfosMagasin(self, details_projet):
        info_magasin = (
            f"Nom du magasin: {details_projet['nomMagasin']}\n"
            f"Adresse du magasin: {details_projet['adresse_magasin']}\n"
            f"Auteur du projet: {details_projet['auteurProjet']}\n"
            f"Date de création du projet: {details_projet['dateCreationProjet']}\n"
        )
        self.info_magasin_texte.setText(info_magasin)
    
    # Méthode pour activer la modification
    def activerModificationInfosMagasin(self):
        self.modifierInfosMagasin(False)

    # Méthode pour désactiver la modification
    def desactiverModificationInfosMagasin(self):
        self.modifierInfosMagasin(True)
        
    # Méthode unique pour activer ou désactiver la modification des informations du magasin
    def modifierInfosMagasin(self, activer):
        if not activer:
            self.info_magasin_texte.setReadOnly(False)
            self.modifier_button.hide()
            self.valider_button.show()
        else:
            self.info_magasin_texte.setReadOnly(True)
            self.modifier_button.show()
            self.valider_button.hide()
            
    # Fonction qui permet d'appliquer le thème sombre
    def theme_sombre(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2B2B2B;
                color: #CCCCCC;
            }
            QLabel, QLineEdit, QTextEdit, QTreeWidget, QDockWidget, QMenuBar, QMenu, QToolBar, QToolButton {
                background-color: #2B2B2B;
                color: #CCCCCC;
            }
            QPushButton {
                background-color: #555555;
                color: #CCCCCC;
            }
            QPushButton::hover {
                background-color: #777777;
            }
        """)

    # Fonction qui permet d'appliquer le thème clair 
    def theme_clair(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
                color: #000000;
            }
            QLabel, QLineEdit, QTextEdit, QTreeWidget, QDockWidget, QMenuBar, QMenu, QToolBar, QToolButton {
                background-color: #FFFFFF;
                color: #000000;
            }
            QPushButton {
                background-color: #E0E0E0;
                color: #000000;
            }
            QPushButton::hover {
                background-color: #C0C0C0;
            }
        """)

# ------------------------------------------------------------------- MAIN POUR TESTER ------------------------------------------------------------------------
if __name__ == "__main__":
    print("Test de la vue")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())