import sys , json
from PyQt6.QtWidgets import QApplication,QMainWindow,QToolBar,QFileDialog,QWidget,QVBoxLayout,QLabel,QLineEdit,QDateEdit,QDialogButtonBox,QDockWidget,QTextEdit
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt , pyqtSignal


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
        
        self.showMaximized()
        
        
    # Envoie des signaux :
    
    def liste_new(self):
        self.MAINW_new_liste_signal.emit()
        
        
    def info(self):
        self.popup = popup_info()
        self.popup.show()
    
    
    def update_list_view(self , formated_data):
        self.json_display.setPlainText(formated_data)


    def open_liste(self):        
        filename, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier liste :", filter="JSON (*.json)")
        
        if filename:
            
            self.currentfile : str = filename
            
            self.MAINW_open_liste_signal.emit(filename)

        
    def save_liste(self):
        
        new_items = [item.strip() for item in self.user_input.toPlainText().split(",")]
        
        self.MAINW_save_liste_signal.emit(new_items , self.currentfile)
        
        
        
        
        
        
        
        
################################################### MAIN TEST ###################################################

if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)
    
    fenetre = popup_new_liste()
    fenetre.show()
    
    sys.exit(app.exec())