# ============================================================================================================================================================
#                                                     Vue de l'application numéro une
#                                                   Fait par FARDEL Mathéïs et DEMOL Alexis
#=============================================================================================================================================================

import sys, os
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QDialog, QDialogButtonBox, QDockWidget, QLineEdit, QTextEdit, QCalendarWidget, QTreeWidget, QTreeWidgetItem, QPushButton, QFileDialog, QMessageBox, QMenu, QApplication, QScrollArea, QCheckBox, QToolBar, QHBoxLayout
from PyQt6.QtGui import QPixmap, QIcon, QPainter, QPen, QFont, QAction, QMouseEvent
from PyQt6.QtCore import Qt, pyqtSignal


def ouvrir_pdf(pdf_path):
    """
    Ouvre un fichier PDF en utilisant l'application par défaut du système.

    Parametre:
    ----------
    pdf_path : Le chemin vers le fichier PDF à ouvrir.

    """
    if sys.platform == "win32": # Ouvre le pdf sous Windows 
        os.startfile(pdf_path)
    elif sys.platform == "linux":
        os.system(f'xdg-open {pdf_path}') # Ouvre le pdf sous Linux et ses distrib: Debian, ubuntu etc..
    elif sys.platform == "darwin":
        os.system(f"open '{pdf_path}'") # Ouvre le pdf sous mac 

# --------------------------------------------------------------- classe Image ------------------------------------------------------------------------------
class Image(QLabel):
    """
    Classe Image qui hérite de QLabel pour afficher une image.

    Résumé des attributs et méthodes de la class:

    Attributs:
    ----------
    -image : L'objet QPixmap contenant l'image chargée à partir du chemin fourni.

    Méthodes:
    -------
    -__init__(chemin): Initialise l'objet Image avec le chemin de l'image à charger.

    """

    def __init__(self, chemin: str):
        """
        Initialise l'objet Image.

        Parametre:
        ----------
        chemin : Le chemin vers l'image à afficher.
        """
        super().__init__()
        self.image = QPixmap(chemin)
        self.setPixmap(self.image)

# -------------------------------------------------------------- classe Plateau -----------------------------------------------------------------------------
class Plateau(QWidget):
    """
    Classe Plateau permettant de représenter notre plan avec un quadrillage et une gestion des cases dans celui ci.

    Résumé des attributs et méthodes de la class:

    Attributs:
    ----------
    -articleSelected : Signal émis lorsqu'un article est sélectionné.
    -caseUpdated : Signal émis lorsqu'une case est mise à jour.
    -layout : Layout vertical pour permettre d'organiser nos widgets.
    -image_label : Label pour afficher l'image du plateau.
    -pixmap : Contient l'image chargée.
    -caseQuadrillage : Liste des coordonnées des cases du quadrillage.
    -produits_dans_cases : Dictionnaire des produits placés dans les cases.
    -objet_selectionne : L'objet qui est actuellement sélectionné.
    -lgn : Nombre de lignes dans le quadrillage.
    -cols : Nombre de colonnes dans le quadrillage.
    -dimX : Dimension X des cases.
    -dimY : Dimension Y des cases.
    -chemin_image : Chemin de l'image chargée.

    Méthodes:
    -------
    -__init__(): Initialise le Plateau. 
    -setObjetSelectionne(objet): Définit l'objet que l'ou souhaite sélectionné.
    -chargerImage(chemin): Charge une image à partir d'un chemin quelconque.
    -rechargerImage(): Fonction pour recharger l'image et réinitialiser son quadrillage 
    -createQuadrillage(lgn, cols, dimX, dimY): Crée un quadrillage sur l'image de notre plan de magasins.
    -ouvrirFenetre(event): Ouvre une fenetre modal.
    -placer_objet_dans_case(case): Place un objet dans une case que l'on veut.
    -mettre_a_jour_case(case, afficher_message): Met a jour la case pour ajouter un bojet dedans.
    -afficher_produits_dans_case(case, avec_suppression): Affiche le produit présent dans une case quand on clique dessus.
    -creation_gestionnaire_suppression_contenu_case(case, fenetre): Crée un gestionnaire pour gérer la suppresion du contenu d'une de nos case.
    -redessiner_case(case): Redessine la case rouge en noir après avoir était supprimer.
    -supprimer_contenu_case(case, fenetre): Supprime le contenu de la case.
    -reinitialiser_plateau(): Réinitialise le plateau en effacant l'image et les produits. 

    """

    articleSelected = pyqtSignal(str) 
    caseUpdated = pyqtSignal(tuple, list) 

    # Initialise le Plateau. 
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.pixmap = QPixmap()
        self.image_label.mousePressEvent = self.ouvrirFenetre
        self.caseQuadrillage = []  
        self.produits_dans_cases = {}  
        self.objet_selectionne = None 
        self.lgn = 0
        self.cols = 0
        self.dimX = 0
        self.dimY = 0
        self.chemin_image = None  
    
    def setObjetSelectionne(self, objet): 
        """
        Définit l'objet que l'ou souhaite sélectionné.

        Parametre:
        ----------
        objet : Le nom de l'objet sélectionné.

        """
        self.objet_selectionne = objet
        self.articleSelected.emit(objet)  

    def chargerImage(self, chemin: str):
        """
        Charge une image à partir d'un chemin quelconque.

        Parametre:
        ----------
        chemin : Le chemin de l'image à charger.

        """
        if chemin:
            self.chemin_image = chemin  
            self.pixmap.load(chemin)
            self.pixmap = self.pixmap.scaled(900, 700, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(self.pixmap)
            self.image_label.setFixedSize(900, 700)
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 

    # Fonction pour recharger l'image et réinitialiser son quadrillage 
    def rechargerImage(self):
        if self.chemin_image:
            self.pixmap.load(self.chemin_image)
            self.pixmap = self.pixmap.scaled(900, 700, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(self.pixmap)
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  
            self.createQuadrillage(self.lgn, self.cols, self.dimX, self.dimY)

    def createQuadrillage(self, lgn, cols, dimX, dimY):
        """
        Crée un quadrillage sur l'image de notre plan de magasins.

        Parametre:
        ----------
        lgn : Nombre de lignes du quadrillage.
        cols : Nombre de colonnes du quadrillage.
        dimX : Dimension X des cases.
        dimY : Dimension Y des cases.

        """
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

            self.caseQuadrillage = [] 

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
    
    def ouvrirFenetre(self, event): 
        """
        Ouvre une fenetre modal. 

        Parametre:
        ----------
        event : L'événement de clic de la souris.

        """
        posClick = event.pos()

        # Calculer le décalage de l'image centrée
        image_rect = self.image_label.pixmap().rect()
        label_rect = self.image_label.rect()
        decalage_x = (label_rect.width() - image_rect.width()) // 2
        decalage_y = (label_rect.height() - image_rect.height()) // 2

        # Ajuster les coordonnées de clic
        x_ajuste = posClick.x() - decalage_x
        y_ajuste = posClick.y() - decalage_y

        for (x1, y1, x2, y2) in self.caseQuadrillage:
            if x1 <= x_ajuste <= x2 and y1 <= y_ajuste <= y2:
                case = (x1, y1, x2, y2)
                if case in self.produits_dans_cases:
                    self.afficher_produits_dans_case(case, avec_suppression=True)
                else:
                    self.placer_objet_dans_case(case)
                break
    
    def placer_objet_dans_case(self, case):  
        """
        Place un objet dans une case que l'on veut.

        Parametre:
        ----------
        case: Les coordonnées de la case.

        """
        if self.objet_selectionne:
            produit = self.objet_selectionne
            if case not in self.produits_dans_cases:
                self.produits_dans_cases[case] = []
            self.produits_dans_cases[case].append(produit)
            self.mettre_a_jour_case(case)
            self.caseUpdated.emit(case, self.produits_dans_cases[case])  
            self.objet_selectionne = None

    def mettre_a_jour_case(self, case, afficher_message=True): 
        """
        Met a jour la case pour ajouter un bojet dedans.

        Parametre:
        ----------
        case: Les coordonnées de la case.
        afficher_message : Indique si un message doit être affiché (par défaut True).

        """
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

    def afficher_produits_dans_case(self, case, avec_suppression=False): 
        """
        Affiche le produit présent dans une case quand on clique dessus.

        Parametre:
        ----------
        case: Les coordonnées de la case.
        avec_suppression : Indique si l'option de suppression doit être affichée (par défaut False).

        """
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
        """
        Crée un gestionnaire pour gérer la suppresion du contenu d'une de nos case.

        Parametre:
        ----------
        case: Les coordonnées de la case.
        fenetre : La fenêtre de dialogue pour la suppression.

        Returns:
        -------
        La fonction de gestion de la suppression.

        """
        def gestion():
            self.supprimer_contenu_case(case, fenetre)
        return gestion
        
    def redessiner_case(self, case):
        """
        Redessine la case rouge en noir après avoir était supprimer.

        Parametre:
        ----------
        case: Les coordonnées de la case.

        """
        x1, y1, x2, y2 = case
        painter = QPainter(self.pixmap)
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(x1, y1, x2 - x1, y2 - y1)
        painter.end()
        self.image_label.setPixmap(self.pixmap)

    def supprimer_contenu_case(self, case, fenetre):
        """
        Supprime le contenu de la case.

        Parametre:
        ----------
        case: Les coordonnées de la case.
        fenetre : La fenêtre de dialogue pour la suppression.

        """
        if case in self.produits_dans_cases:
            del self.produits_dans_cases[case]
            self.redessiner_case(case)
            self.caseUpdated.emit(case, [])  
            fenetre.accept()
            QMessageBox.information(self, "Suppression", f"Le contenu de la case ({case[0]}, {case[1]}) a été supprimé.")
    
    # Réinitialise le plateau en effacant l'image et les produits. 
    def reinitialiser_plateau(self):
        self.image_label.clear()
        self.produits_dans_cases.clear()
        self.caseQuadrillage.clear()
        self.pixmap = QPixmap()
        self.image_label.setPixmap(self.pixmap)

# ------------------------------------------------------- classe SelectionProduitsDialog ------------------------------------------------------------------------
class SelectionProduitsDialog(QDialog):
    """
    Classe SelectionProduitsDialog pour afficher une fenetre de sélection des produits.

    Résumé des attributs et méthodes de la class:

    Attributs:
    ----------
    -produits : Dictionnaire des produits disponibles dans le magasins.
    -checkboxes : Dictionnaire des cases à cocher pour les produits qui sont séléctionné pour etre dans le magasins.

    Méthodes:
    -------
    -get_selected_produits(): Récupérer les produits sélectionnés.
    -find_categorie(article: str): Permet de savoir la catégorie d'un produit

    """

    def __init__(self, produits, parent=None):
        """
        Initialise l'objet SelectionProduitsDialog.

        Parametre:
        ----------
        produits : Le dictionnaire des produits disponibles.
        parent : Le widget parent (par défaut None).

        """
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
        
    def get_selected_produits(self):
        """
        Récupérer les produits sélectionnés.

        Returns:
        -------
        Le dictionnaire des produits sélectionnés.

        """
        selected_produits = {}
        for article, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                categorie = self.find_categorie(article)
                if categorie not in selected_produits:
                    selected_produits[categorie] = []
                selected_produits[categorie].append(article)
        return selected_produits
    
    def find_categorie(self, article):
        """
        Permet de savoir la catégorie d'un produit.

        Parametre:
        ----------
        article : Le nom de l'article.

        Returns:
        -------
        La catégorie de l'article.

        """
        for categorie, articles in self.produits.items():
            if article in articles:
                return categorie
        return None

# ------------------------------------------------------- classe NewProjetDialog ------------------------------------------------------------------------
class NewProjetDialog(QDialog):
    """
    Classe NewProjetDialog pour créer un nouveau projet.

    Résumé des attributs et méthodes de la class:

    Attributs:
    ----------
    -produits : Dictionnaire des produits disponibles.
    -produits_selectionnes : Dictionnaire des produits sélectionnés du magasins.
    -nomProjet : Permet de saisir le nom du projet.
    -auteurProjet : Permet de saisir l'auteur du projet.
    -dateCreationProjet : Widget pour sélectionner la date de création du projet.
    -nomMagasin : Permet de saisir le nom du magasin.
    -adresseMagasin : Permet de saisir l'adresse du magasin.
    -lgn : Permet de saisir le nombre de lignes du quadrillage.
    -cols : Permet de saisir le nombre de colonnes du quadrillage.
    -dimX : Permet de saisir les dimensions X des cases.
    -dimY : Permet de saisir les dimensions Y des cases.
    -choisir_produits_button : Bouton pour ouvrir la sélection des produits.

    Méthodes:
    -------
    ouvrir_selection_produits(): Permet d'ouvrir la page pour sélectionner ses produits
    getProjetDetails(): Récupere tout les détails important a garder du projet.

    """

    def __init__(self, produits, parent=None):
        """
        Initialise l'objet NewProjetDialog.

        Parametre:
        ----------
        produits : Le dictionnaire des produits disponibles.
        parent : Le widget parent (qui est par défaut en None).

        """
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
            
    def getProjetDetails(self):
        """
        Récupere tout les détails important a garder du projet.

        Returns:
        -------
        Le dictionnaire des détails du projet.

        """
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
    """
    Classe MainWindow permettant d'afficher la fenêtre principale de l'application MarketPlan Editor.

    Résumé des attributs et méthodes de la class:

    Attributs:
    ----------
    -dock_articles : Dock widget pour afficher les articles (celui de gauche).
    -objets_widget : Widget pour afficher les objets sous forme d'arborescence (des sous listes).
    -objet_selectionne : L'objet actuellement sélectionné.
    -plateau : Widget du plateau central.
    -boutons_layout : Layout horizontal pour les boutons de gestion des colonnes et lignes.
    -ajouter_colonnes_button : Bouton pour ajouter des colonnes.
    -retirer_colonnes_button : Bouton pour retirer des colonnes.
    -ajouter_lignes_button : Bouton pour ajouter des lignes.
    -retirer_lignes_button : Bouton pour retirer des lignes.
    -dock_info_magasin : Dock widget pour afficher les informations du magasin.
    -info_magasin_texte : Widget de texte pour afficher les informations du magasin.
    -modifier_button : Bouton pour activer la modification des informations du magasin.
    -valider_button : Bouton pour valider les modifications des informations du magasin.
    -action_new_projet : Action pour créer un nouveau projet.
    -action_engresitrer_projet : Action pour enregistrer un projet.
    -action_ouvrir_projet : Action pour ouvrir un projet.
    -action_supprimer_projet : Action pour supprimer un projet.
    -action_theme_clair : Action pour appliquer le thème clair.
    -action_theme_sombre : Action pour appliquer le thème sombre.
    -action_notice : Action pour afficher la notice d'utilisation de l'application MarketPlan Editor.

    Méthodes:
    -------
    -afficher_notice(): Affiche la notice d'utilisation de l'application MarketPlan Editor 
    -ajouter_colonnes(): Permet d'ajouter des colonnes dans le quadrillage après avoir créer le projet 
    -retirer_colonnes(): Permet de retirer des colonnes dans le quadrillage après avoir créer le projet 
    -ajouter_lignes(): Permet d'ajouter des lignes dans le quadrillage après avoir créer le projet 
    -retirer_lignes(): Permet de retirer des lignes dans le quadrillage après avoir créer le projet 
    -afficher_message_erreur(titre, message): Permet d'afficher un message d'erreur.
    -selectionner_objet(item, column): Permet de pouvoir sélectionner un objet.
    -listeObjets(produits): Permet d'afficher les différents Articles.
    -afficherInfosMagasin(details_projet): Affiche les informations du magasin.
    -activerModificationInfosMagasin(): Active la modification des informations du magasin.
    -desactiverModificationInfosMagasin(): Désactive la modification des informations du magasin.
    -modifierInfosMagasin(activer): Active ou désactive la modification des informations du magasin.
    -theme_sombre(): Fonction qui permet d'appliquer le thème sombre.
    -theme_clair(): Fonction qui permet d'appliquer le thème clair.

    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MarketPlan Editor")
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
        layout.addWidget(self.plateau, alignment=Qt.AlignmentFlag.AlignCenter)  

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
        
        # Barre menu pour les affichages 
        menu_affichage = menu_bar.addMenu('&Affichage')
        
        # Sous-menu pour les thèmes 
        menu_themes = menu_affichage.addMenu("Thèmes")
        self.action_theme_clair = QAction("Thème clair", self)
        self.action_theme_sombre = QAction("Thème sombre", self)
        menu_themes.addAction(self.action_theme_clair)
        menu_themes.addAction(self.action_theme_sombre)
        self.action_theme_clair.triggered.connect(self.theme_clair)
        self.action_theme_sombre.triggered.connect(self.theme_sombre)

        # Menu "Aide" avec le menu "Notice"
        menu_aide = menu_bar.addMenu('&Aide')
        self.action_notice = QAction("Notice", self)
        menu_aide.addAction(self.action_notice)
        self.action_notice.triggered.connect(self.afficher_notice)

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

    # Affiche la notice d'utilisation de l'application MarketPlan Editor 
    def afficher_notice(self):
        chemin_pdf = os.path.join(sys.path[0], 'Notice-MarketPlanEditor.pdf')
        if os.path.exists(chemin_pdf):
            ouvrir_pdf(chemin_pdf)
        else:
            QMessageBox.critical(self, "Erreur", "Le fichier de la notice est introuvable.")
        
    # Permet d'ajouter des colonnes dans le quadrillage après avoir créer le projet 
    def ajouter_colonnes(self):
        self.plateau.cols = self.plateau.cols + 1
        self.plateau.rechargerImage()

    # Permet de retirer des colonnes dans le quadrillage après avoir créer le projet 
    def retirer_colonnes(self):
        if self.plateau.cols > 1:
            self.plateau.cols = self.plateau.cols - 1
            self.plateau.rechargerImage()

    # Permet d'ajouter des lignes dans le quadrillage après avoir créer le projet 
    def ajouter_lignes(self):
        self.plateau.lgn = self.plateau.lgn + 1
        self.plateau.rechargerImage()

    # Permet de retirer des lignes dans le quadrillage après avoir créer le projet 
    def retirer_lignes(self):
        if self.plateau.lgn > 1:
            self.plateau.lgn = self.plateau.lgn - 1
            self.plateau.rechargerImage()

    # Permet d'afficher un message d'erreur !
    def afficher_message_erreur(self, titre, message):
        QMessageBox.critical(self, titre, message)

    def selectionner_objet(self, item, column):  
        """
        Permet de pouvoir sélectionner un objet.

        Parametre:
        ----------
        item : L'élément sélectionné dans le docker.
        column : La colonne de l'élément sélectionné.

        """
        self.objet_selectionne = item.text(0) 
        self.plateau.setObjetSelectionne(self.objet_selectionne) 
        self.plateau.articleSelected.emit(self.objet_selectionne)  

    def listeObjets(self, produits):
        """
        Permet d'afficher les différents Articles.

        Parametre:
        ----------
        produits : Le dictionnaire des produits.

        """
        self.objets_widget.clear()
        for categorie, articles in produits.items():
            parent = QTreeWidgetItem([categorie])
            parent.setFont(0, QFont('Arial', 14, QFont.Weight.Bold))
            for article in articles:
                child = QTreeWidgetItem([article])
                child.setFont(0, QFont('Arial', 12))
                parent.addChild(child)
            self.objets_widget.addTopLevelItem(parent)

    def afficherInfosMagasin(self, details_projet):
        """
        Affiche les informations du magasin.

        Parametre:
        ----------
        details_projet : Le dictionnaire des détails du projet.

        """
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
        """
        Active ou désactive la modification des informations du magasin.

        Parametre:
        ----------
        activer : Indique si la modification doit être activée ou désactivée.

        """
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