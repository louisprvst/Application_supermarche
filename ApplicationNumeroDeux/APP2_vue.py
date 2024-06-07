import sys
import json
import os
from PyQt6.QtWidgets import QApplication,QMainWindow,QToolBar,QFileDialog,QWidget,QVBoxLayout,QLabel,QLineEdit,QDateEdit,QDialogButtonBox,QDockWidget,QTextEdit,QMessageBox, QCompleter
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt , pyqtSignal, QStringListModel


##################################################### POPUP INFO #####################################################


class popup_info(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('A propos')
        self.setGeometry(100, 100, 300, 150)
        
        self.name = QLabel("Application item finder.")
        

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
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButtons.Ok | QDialogButtonBox.StandardButtons.Cancel, Qt.Orientations.Horizontal, self)
        
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
    
# Constructeur :
    
    def __init__(self):
        
        super().__init__()

        self.setWindowTitle("Ma liste de course")
        
    # Menu Bar :

        menu_bar = self.menuBar()
        
    # Menu Fichiers :
        
        menu_Fichiers = menu_bar.addMenu('&Fichier')
        
        fic_ouvrir = QAction(QIcon(sys.path[0] + '/icones/magasin.png'), 'Choisir un magasin', self)
        ##fic_ouvrir.triggered.connect(self.fic_ouvrir)
        fic_ouvrir.setShortcut("Ctrl+O")
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
    
    # Cette fonction permet de créer une nouvelle liste
    
    def liste_new(self):
        self.MAINW_new_liste_signal.emit()
        
    # Cette fonction affiche la popup avec les informations sur l'app
        
    def info(self):
        self.popup = popup_info()
        self.popup.show()
    
    # Cette fonction sert a actualiser le texte afficher dans le dock gauche. ( liste des items )
    
    def update_list_view(self , formated_data):
        self.json_display.setPlainText(formated_data)

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
            QLabel, QLineEdit, QTextEdit, QTreeWidget, QDockWidget, QMenuBar, QMenu, QToolBar, QToolButton {
                background-color: #FFFFFF;
                color: #000000;
            }""")
    
    def change_theme_sombre(self):
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #141414;
                color: #FFFFFF;
            }
            QLabel, QLineEdit, QTextEdit, QTreeWidget, QDockWidget, QMenuBar, QMenu, QToolBar, QToolButton {
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