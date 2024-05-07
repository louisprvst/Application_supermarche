import sys
from PyQt6.QtWidgets import QApplication,QMainWindow,QToolBar
from PyQt6.QtGui import QIcon, QAction

class vueApplication(QMainWindow):

    def __init__(self):
        
        super().__init__()

        self.setWindowTitle("Item Finder")
        self.setWindowIcon(QIcon(sys.path[0] + '/icones/cadie.jpg'))
        
    #Menu Bar

        menu_bar = self.menuBar()
        
    #Menu Fichiers :
        
        menu_Fichiers = menu_bar.addMenu('&Fichier')
        
        fic_ouvrir = QAction(QIcon(sys.path[0] + '/../icones/plus.png'), 'Choisir un magasin', self)
        ##fic_ouvrir.triggered.connect(self.fic_ouvrir)
        menu_Fichiers.addAction(fic_ouvrir)
        
    #Menu Listes :
        
        menu_Listes = menu_bar.addMenu('&Listes')
        
        liste_new = QAction(QIcon(sys.path[0] + '/../icones/plus.png'), 'Nouvelle liste', self)
        ##liste_new.triggered.connect(self.liste_new)
        menu_Listes.addAction(liste_new)
        
        liste_open = QAction(QIcon(sys.path[0] + '/../icones/plus.png'), 'Ouvrir une liste', self)
        ##liste_open.triggered.connect(self.liste_open)
        menu_Listes.addAction(liste_open)
        
    #Menu Aides :
        
        menu_help = menu_bar.addMenu('&Aides')
        
        help_info = QAction(QIcon(sys.path[0] + '/../icones/plus.png'), 'A propos', self)
        menu_help.addAction(help_info)    
        
    #Tool Bar 
        
        toolbar = QToolBar('Tool Bar')
        self.addToolBar(toolbar)

        toolbar.addAction(fic_ouvrir)
        toolbar.addAction(liste_new)
        toolbar.addAction(liste_open)
        toolbar.addAction(help_info)
        
        
        
        
        
        
        
        
        
        

        self.showMaximized()


#Main pour tester la vue
if __name__ == "__main__":

    # création d'une QApplication
    app = QApplication(sys.argv)

    # # création de la fenêtre de l'application
    fenetre = vueApplication()

    # lancement de l'application
    sys.exit(app.exec())
