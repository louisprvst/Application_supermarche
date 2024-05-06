import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QInputDialog, QLabel, QToolBar
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QFont

class vueApplication(QMainWindow):

    def __init__(self, chemin: str = None):
        super().__init__()
        self.__chemin = chemin
        self.setWindowTitle("Application supermarché")
        self.setWindowIcon(QIcon(sys.path[0] + '/icones/cadie.png'))
        self.setGeometry(100, 100, 500, 300)

        # barre de menu
        menu_bar = self.menuBar()
        menu_theme = menu_bar.addMenu('&Projet')
        menu_theme.addAction('Nouveau projet')
        menu_theme.addAction('Ouvrir projet')

        self.showMaximized()


#Main pour tester la vue
if __name__ == "__main__":

    # création d'une QApplication
    app = QApplication(sys.argv)

    # # création de la fenêtre de l'application
    fenetre = vueApplication()

    # lancement de l'application
    sys.exit(app.exec())
