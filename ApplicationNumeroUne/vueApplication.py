#========================================================================================================================================================
#=                                                                                                                                                      =
#=                                              VUE DE LA PREMIERE APPLICATION by FARDEL Mathéïs                                                        =
#=                                                                                                                                                      =
#========================================================================================================================================================


import json
import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QInputDialog, QLabel, QToolBar, QDockWidget, QMenu
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QFont

class vueApplication(QMainWindow):

    def __init__(self, chemin: str = None):
        super().__init__()
        self.__chemin = chemin
        self.setWindowTitle("Application supermarché")
        self.setWindowIcon(QIcon(os.path.join(sys.path[0], 'icones', 'cadie.jpg')))
        self.setGeometry(100, 100, 500, 300)

        # Charger les données du fichier JSON pour les articles
        chemin_json = os.path.join(sys.path[0], "liste_produits.json")
        with open(chemin_json, 'r') as f:
            data = json.load(f)

        # barre de menu
        menu_bar = self.menuBar()
        menu_theme = menu_bar.addMenu('&Projet')
        menu_theme.addAction('Nouveau projet')
        menu_theme.addAction('Ouvrir projet')

        # dock contenant tous les différents types d'articles
        dock_articles = QDockWidget('Articles')
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_articles)
        dock_articles.setMaximumWidth(400)

        # Créer un widget pour contenir le menu des articles
        widget_menu_articles = QWidget()
        layout_menu_articles = QVBoxLayout(widget_menu_articles)

        # Ajouter chaque catégorie d'articles au menu
        for categorie, articles in data.items():
            menu_categorie = QMenu(categorie, self)
            for article in articles:
                action = QAction(article, self)
                menu_categorie.addAction(action)
            layout_menu_articles.addWidget(menu_categorie)

        dock_articles.setWidget(widget_menu_articles)

        self.showMaximized()

# Main pour tester la vue
if __name__ == "__main__":
    # création d'une QApplication
    app = QApplication(sys.argv)
    # création de la fenêtre de l'application
    fenetre = vueApplication()
    # lancement de l'application
    sys.exit(app.exec())
