import sys , json, os
from PyQt6.QtWidgets import QApplication,QDialog,QVBoxLayout,QMainWindow,QToolBar,QFileDialog,QWidget,QVBoxLayout,QLabel,QLineEdit,QDateEdit,QDialogButtonBox,QDockWidget,QTextEdit,QMessageBox, QCompleter
from PyQt6.QtGui import QIcon , QAction , QPixmap , QPainter , QPen
from PyQt6.QtCore import Qt , pyqtSignal, QStringListModel


###################################################### CLASS IMAGE ( APP 1 ) ######################################################

class Image(QLabel):
    
    def __init__(self, chemin: str):
        
        super().__init__()
        self.image = QPixmap(chemin)
        self.setPixmap(self.image)


##################################################### CLASS PLATEAU ( APP 1 ) #####################################################

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
                    self.afficher_produits_dans_case(case)
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
    def afficher_produits_dans_case(self, case): 
        x1, y1, x2, y2 = case
        produits = self.produits_dans_cases[case]
        contenu = "\n".join(produits)
        
        # Création de la fenêtre modale
        fenetre = QDialog(self)
        fenetre.setWindowTitle("Produits dans la case")
        layout = QVBoxLayout()
        label = QLabel(f"Produits dans la case ({x1}, {y1}):\n{contenu}")
        layout.addWidget(label)
        
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
        
    # Tentative de chemin :
    
    def create_adjacency_list(self):
        adj_list = {}
        for idx, case in enumerate(self.caseQuadrillage):
            adj_list[idx] = self.get_adjacent_cases(idx)
        return adj_list

    def get_adjacent_cases(self, idx):
        adjacents = []
        lgn, cols = self.lgn, self.cols
        row, col = divmod(idx, cols)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # haut, bas, gauche, droite

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < lgn and 0 <= c < cols:
                adjacents.append(r * cols + c)
        return adjacents

    def bfs_shortest_path(self, start_idx, end_idx, adj_list):
        queue = [(start_idx, [start_idx])]
        visited = set()

        while queue:
            current, path = queue.pop(0)
            if current == end_idx:
                return path

            if current not in visited:
                visited.add(current)
                for neighbor in adj_list[current]:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))
        return []

    def highlight_path(self, path):
        if not self.pixmap.isNull():
            painter = QPainter(self.pixmap)
            pen = QPen(Qt.GlobalColor.blue)
            pen.setWidth(2)
            painter.setPen(pen)

            for idx in path:
                x1, y1, x2, y2 = self.caseQuadrillage[idx]
                painter.drawRect(x1, y1, x2 - x1, y2 - y1)

            painter.end()
            self.image_label.setPixmap(self.pixmap)

    def find_and_highlight_path(self, start_pos, end_pos):
        adj_list = self.create_adjacency_list()
        start_idx = self.caseQuadrillage.index(start_pos)
        end_idx = self.caseQuadrillage.index(end_pos)
        path = self.bfs_shortest_path(start_idx, end_idx, adj_list)
        self.highlight_path(path)


##################################################### POPUP INFO #####################################################

class popup_info(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('À propos')
        self.setGeometry(100, 100, 300, 150)
        
        self.name = QLabel("Application item finder.")
        
        layout = QVBoxLayout()
        layout.addWidget(self.name)
        self.setLayout(layout)
              
        self.show()
        

################################################### POPUP NEW LISTE ###################################################

class popup_new_liste(QWidget):
    
    # Signaux :
    
    POPNL_save_signal = pyqtSignal(str , str ,str)
    
    # Constructeur : 
    
    def __init__(self):
        
        super().__init__()
        
        self.setWindowTitle('Création de liste')
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.nom_label = QLabel('Nom de la liste :')
        self.nom_input = QLineEdit()

        self.date_label = QLabel('Date de vos courses :')
        self.date_input = QDateEdit()
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, Qt.Orientation.Horizontal, self)
        
        self.buttons.accepted.connect(self.save_to_json)
        self.buttons.rejected.connect(self.close)

        layout.addWidget(self.nom_label)
        layout.addWidget(self.nom_input)
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_input)
        layout.addWidget(self.buttons)

        self.setLayout(layout)
        
    # Envoie des signaux :
        
    def save_to_json(self):
        
        nom = self.nom_input.text()
        date = self.date_input.text()
        filename = f"{nom}.json"
        
        self.POPNL_save_signal.emit(nom,date,filename)
    
        
################################################### VUE APP2 ###################################################
     
class vueApplication(QMainWindow):
    
# Signaux :
    
    MAINW_open_liste_signal = pyqtSignal(str)
    
    MAINW_new_liste_signal = pyqtSignal()
    
    MAINW_save_liste_signal = pyqtSignal(list , str)
    
    MAINW_open_shop_signal = pyqtSignal()
    
# Constructeur :
    
    def __init__(self):
        
        super().__init__()

        self.setWindowTitle("Ma liste de course")
        
    # Menu Bar :

        menu_bar = self.menuBar()
        
    # Menu Fichiers :
        
        menu_Fichiers = menu_bar.addMenu('&Fichier')
       
        fic_ouvrir = QAction(QIcon(sys.path[0] + '/icones/magasin.png'), 'Choisir un magasin', self)
        fic_ouvrir.triggered.connect(self.ouvrir_fichier)
        fic_ouvrir.setShortcut('Ctrl+O')
        menu_Fichiers.addAction(fic_ouvrir)
        
        charger_produits = QAction(QIcon(sys.path[0] + '/icones/open.png'), 'Charger produits', self)
        charger_produits.triggered.connect(self.chargerProduits)
        menu_Fichiers.addAction(charger_produits)
        
    # Menu Listes :
        
        menu_Listes = menu_bar.addMenu('&Listes')
        
        liste_new = QAction(QIcon(sys.path[0] + '/icones/plus.png'), 'Nouvelle liste', self)
        liste_new.triggered.connect(self.liste_new)
        liste_new.setShortcut("Ctrl+L")
        menu_Listes.addAction(liste_new)
        
        liste_open = QAction(QIcon(sys.path[0] + '/icones/list.png'), 'Ouvrir une liste', self)
        liste_open.setShortcut("Ctrl+P")
        liste_open.triggered.connect(self.open_liste)
        menu_Listes.addAction(liste_open)
        
        liste_save = QAction(QIcon(sys.path[0] + '/icones/save.png'), 'Sauvegarder une liste', self)
        liste_save.setShortcut("Ctrl+A")
        liste_save.triggered.connect(self.save_liste)
        menu_Listes.addAction(liste_save)
        
    # Menu Thèmes :
        
        menu_themes = menu_bar.addMenu('&Thèmes')
        
        theme_clair = QAction(QIcon(sys.path[0] + '/icones/'), 'Theme clair', self)
        theme_clair.triggered.connect(self.change_theme_clair)
        menu_themes.addAction(theme_clair)
        
        theme_sombre = QAction(QIcon(sys.path[0] + '/icones/'), 'Theme sombre', self)
        theme_sombre.triggered.connect(self.change_theme_sombre)
        menu_themes.addAction(theme_sombre)
        
        theme_default = QAction(QIcon(sys.path[0] + '/icones/'), 'Theme par défaut', self)
        theme_default.triggered.connect(self.change_theme_default)
        menu_themes.addAction(theme_default)
        
    # Menu Aides :
        
        menu_help = menu_bar.addMenu('&Aides')
        
        help_info = QAction(QIcon(sys.path[0] + '/icones/question.png'), 'A propos', self)
        help_info.triggered.connect(self.info)
        help_info.setShortcut("Ctrl+I")
        menu_help.addAction(help_info)    
        
    # Tool Bar :
        
        toolbar = QToolBar('Tool Bar')
        self.addToolBar(toolbar)
        
        toolbar.addAction(fic_ouvrir)
        toolbar.addSeparator()
        toolbar.addAction(liste_new)
        toolbar.addAction(liste_open)
        toolbar.addAction(liste_save)
        
    # Dock :

        def autocompletion(filename):
            # Fonction pour charger les noms des produits à partir d'un fichier JSON
            try:
                with open(filename, "r") as file:
                    data = json.load(file)
                return list(data.values())  # Retourner les valeurs sous forme de liste
            except FileNotFoundError:
                print(f"ERREUR : le fichier '{filename}' est introuvable.")
                return []  # Retourner une liste vide en cas d'erreur

        class ProduitSuivant(QCompleter):
            def __init__(self, element, parent=None):
                super(ProduitSuivant, self).__init__(element, parent)
                # Configurer la complétion pour être insensible à la casse
                self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                # Configurer le mode de filtrage pour correspondre au texte contenu
                self.setFilterMode(Qt.MatchFlags.MatchContains)
                self.model = QStringListModel(element, self)
                self.setModel(self.model)

            def pathFromIndex(self, index):
                # Obtenir le chemin complet du modèle pour l'index donné
                path = super(ProduitSuivant, self).pathFromIndex(index)
                text = self.widget().text()
                # Trouver la dernière virgule dans le texte
                virgule = text.rfind(',')
                if virgule == -1:
                    # S'il n'y a pas de virgule, retourner le chemin tel quel
                    return path
                # Ajouter le texte après la dernière virgule
                return text[:virgule + 1] + ' ' + path

            def splitPath(self, path):
                # Trouver la dernière virgule dans le chemin
                virgule = path.rfind(',')
                if virgule == -1:
                    # S'il n'y a pas de virgule, utiliser la méthode de la classe parente
                    return super(ProduitSuivant, self).splitPath(path)
                # Retourner le texte après la dernière virgule, en supprimant les espaces
                return [path[virgule + 1:].strip()]


                    


        self.dock_list = QDockWidget('Ma liste :', self)
        
        self.json_display = QTextEdit()
        self.json_display.setPlaceholderText("Veuillez choisir un fichier liste.json ou en créer un ...")
        self.json_display.setReadOnly(True)
        
        self.dock_list.setWidget(self.json_display)
        self.json_display.setMinimumHeight(100)
        self.json_display.setMaximumHeight(100)
        
        self.dock_list.setMaximumWidth(200)
        
        
        self.titre = QLabel("Entrez vos articles :")
        self.titre.setMinimumHeight(25)
        self.titre.setMaximumHeight(25)
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Entrez votre liste ici...")
        self.user_input.setMinimumHeight(100)
        self.user_input.setMaximumHeight(100)
    
        fichier = os.path.dirname(__file__)
        

        # Construire le chemin relatif au fichier JSON
        fichier_chemin = os.path.join(fichier, 'liste_produitsbis.json')
        
        liste = autocompletion(fichier_chemin)
        
        completer = QCompleter(liste)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlags.MatchContains)
        completer = ProduitSuivant(liste)
        self.user_input.setCompleter(completer)
        
        self.comble_widget = QLabel()
        
          
        
        
        layout = QVBoxLayout()
        layout.addWidget(self.json_display)
        layout.addWidget(self.titre)
        layout.addWidget(self.user_input)
        layout.addWidget(self.comble_widget)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.dock_list.setWidget(widget)
        
        self.addDockWidget(Qt.DockWidgetAreas.LeftDockWidgetArea, self.dock_list)
        self.dock_list.setMinimumWidth(200)
        
        self.showMaximized()
      
# Envoie des signaux :

    # Cette fonction permet d'ouvrir un fichier contenant un magasin

    def ouvrir_fichier(self):
        self.MAINW_open_shop_signal.emit()
    
    # Cette fonction permet de créer une nouvelle liste
    
    def liste_new(self):
        self.MAINW_new_liste_signal.emit()
        
    # Cette fonction affiche la popup avec les informations sur l'app
        
    def info(self):
        self.popup = popup_info()
        self.popup.show()
    
    # Cette fonction sert a actualiser le texte afficher dans le dock gauche. ( liste des items )
    
    def update_list_view(self , formated_data , mes_articles):
        self.json_display.setPlainText(formated_data)
        self.user_input.setPlainText(mes_articles)

    # Cette fonction permet d'ouvrir une liste

    def open_liste(self):        
        filename, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier liste :", filter="JSON (*.json)")
        
        if filename:
            
            self.currentfile : str = filename
            
            self.MAINW_open_liste_signal.emit(filename)
            
    # Cette fonction permet de sauvegarder une liste
        
    def save_liste(self):
        
        new_items = [item.strip() for item in self.user_input.toPlainText().split(",")]
        
        self.MAINW_save_liste_signal.emit(new_items , self.currentfile)
            
    # Les fonctions suivante servent a changer de theme.
        
    def change_theme_clair(self):
            
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
                color: #000000;
            }
            QLabel, QLineEdit, QTextEdit, QDockWidget, QMenuBar, QMenu, QToolBar, QToolButton {
                background-color: #FFFFFF;
                color: #000000;
            }""")
    
    def change_theme_sombre(self):
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #141414;
                color: #FFFFFF;
            }
            QLabel, QLineEdit, QTextEdit, QDockWidget, QMenuBar, QMenu, QToolBar, QToolButton {
                background-color: #141414;
                color: #FFFFFF;
            }""")
                
    def change_theme_default(self):
        
        self.setStyleSheet('')
        
    # Cette fonction permet de communiquer un message à l'utilisateur
    
    def new_message_info(self, titre, texte):
        QMessageBox.information(self, titre, texte)
        
    def chargerProduits(self):
        chemin_fichier, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier JSON", "", "JSON Files (*.json);;All Files (*)")
        if chemin_fichier:
            self.plateau.chargerProduitsDepuisJson(chemin_fichier)


       
################################################### MAIN TEST ###################################################

if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)
    
    fenetre = vueApplication()
    fenetre.show()
    
    sys.exit(app.exec())