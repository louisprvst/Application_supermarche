import sys
from PyQt6.QtWidgets import QApplication,QVBoxLayout,QMainWindow,QToolBar,QFileDialog,QWidget,QVBoxLayout,QLabel,QLineEdit,QDateEdit,QDialogButtonBox,QDockWidget,QTextEdit,QMessageBox
from PyQt6.QtGui import QIcon , QAction , QPixmap , QPainter , QPen
from PyQt6.QtCore import Qt , pyqtSignal , QPoint


###################################################### CLASS IMAGE ( APP 1 ) ######################################################

class Image(QLabel):
    
    def __init__(self, chemin: str):
        
        super().__init__()
        self.image = QPixmap(chemin)
        self.setPixmap(self.image)


##################################################### CLASS PLATEAU ( APP 1 ) #####################################################

class Plateau(QWidget):
    
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
        self.chemin_image = None  # Ajouter l'attribut pour le chemin de l'image
    
    def chargerImage(self, chemin: str):
        if chemin:
            self.chemin_image = chemin  # Stocker le chemin de l'image
            self.pixmap.load(chemin)
            self.pixmap = self.pixmap.scaled(1200, 720, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(self.pixmap)
          
             
# Fonction pour tracer un chemin entre les articles qui ne vient pas du code de l'app 1

    def tracerChemin(self):
        if not self.produits_dans_cases:
            return

        cases = list(self.produits_dans_cases.keys())
        points = [QPoint((x1 + x2) // 2, (y1 + y2) // 2) for (x1, y1, x2, y2) in cases]

        if points:
            painter = QPainter(self.pixmap)
            pen = QPen(Qt.GlobalColor.red)
            pen.setWidth(15)
            painter.setPen(pen)

            for i in range(len(points) - 1):
                painter.drawLine(points[i], points[i + 1])

            painter.end()
            self.image_label.setPixmap(self.pixmap)
            

    def rechargerImage(self):
        """Méthode pour recharger l'image et réinitialiser le quadrillage"""
        if self.chemin_image:
            self.pixmap.load(self.chemin_image)
            self.pixmap = self.pixmap.scaled(1200, 720, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
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
            
            self.tracerChemin()
    
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

        
    def redessiner_case(self, case):
        x1, y1, x2, y2 = case
        painter = QPainter(self.pixmap)
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(x1, y1, x2 - x1, y2 - y1)
        painter.end()
        self.image_label.setPixmap(self.pixmap)


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

        self.dock_list = QDockWidget('Ma liste :', self)
        
        self.json_display = QTextEdit()
        self.json_display.setPlaceholderText("Veuillez choisir un fichier liste.json ou en créer un ...")
        self.json_display.setReadOnly(True)
        
        self.dock_list.setWidget(self.json_display)
        
        self.dock_list.setMaximumWidth(200)
        
        self.titre = QLabel("Entrez vos articles :")
        
        self.user_input = QTextEdit()
        self.user_input.setPlaceholderText("Entrez votre liste ici...")
        self.user_input.setMinimumHeight(700)
        self.user_input.setMaximumHeight(700)
        
        layout = QVBoxLayout()
        layout.addWidget(self.json_display)
        layout.addWidget(self.titre)
        layout.addWidget(self.user_input)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.dock_list.setWidget(widget)
        
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_list)
        self.dock_list.setMinimumWidth(200)
 
        # Contenu du plan dans le widget central
        self.plateau = Plateau()
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.plateau)
    
        self.setCentralWidget(central_widget)
 
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

       
################################################### MAIN TEST ###################################################

if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)
    
    fenetre = vueApplication()
    fenetre.show()
    
    sys.exit(app.exec())