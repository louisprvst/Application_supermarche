import sys
from PyQt6.QtWidgets import QApplication,QMainWindow,QToolBar,QFileDialog
from PyQt6.QtGui import QIcon, QAction, QShortcut
from PyQt6.QtCore import Qt, pyqtSignal

class vueApplication(QMainWindow):

    def __init__(self):
        
        super().__init__()

        self.setWindowTitle("Item Finder")
        self.setWindowIcon(QIcon(sys.path[0] + '/icones/'))
        
    ######################### AFFICHAGE #########################
        
    #Menu Bar

        menu_bar = self.menuBar()
        
    #Menu Fichiers :
        
        menu_Fichiers = menu_bar.addMenu('&Fichier')
        
        fic_ouvrir = QAction(QIcon(sys.path[0] + '/icones/map.png'), 'Choisir un magasin', self)
        ##fic_ouvrir.triggered.connect(self.fic_ouvrir)
        fic_ouvrir.setShortcut("Ctrl+O")
        menu_Fichiers.addAction(fic_ouvrir)
        
    #Menu Listes :
        
        menu_Listes = menu_bar.addMenu('&Listes')
        
        liste_new = QAction(QIcon(sys.path[0] + '/icones/plus.png'), 'Nouvelle liste', self)
        ##liste_new.triggered.connect(self.liste_new)
        liste_new.setShortcut("Ctrl+L")
        menu_Listes.addAction(liste_new)
        
        liste_open = QAction(QIcon(sys.path[0] + '/icones/list.png'), 'Ouvrir une liste', self)
        liste_open.setShortcut("Ctrl+P")
        liste_open.triggered.connect(self.open_liste)
        menu_Listes.addAction(liste_open)
        
    #Menu Aides :
        
        menu_help = menu_bar.addMenu('&Aides')
        
        help_info = QAction(QIcon(sys.path[0] + '/icones/question.png'), 'A propos', self)
        help_info.setShortcut("Ctrl+I")
        menu_help.addAction(help_info)    
        
    #Tool Bar 
        
        toolbar = QToolBar('Tool Bar')
        self.addToolBar(toolbar)
        
        toolbar.addAction(fic_ouvrir)
        toolbar.addSeparator()
        toolbar.addAction(liste_new)
        toolbar.addAction(liste_open)

        self.showMaximized()
    
    ######################### SIGNAUX #########################

    def open_liste(self):
        fichier_liste = QFileDialog.getOpenFileName(self, "Choisir un fichier liste :")


#Main pour tester la vue
if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = vueApplication()
    sys.exit(app.exec())