#========================================================================================================================================================
#=                                                                                                                                                      =
#=                                              VUE DE LA PREMIERE APPLICATION by FARDEL Mathéïs                                                        =
#=                                                                                                                                                      =
#========================================================================================================================================================


import json
import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QInputDialog, QLabel, QToolBar, QDockWidget, QMenu
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QFont, QPixmap



# -------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                               classe vueApplication
#--------------------------------------------------------------------------------------------------------------------------------------------------------
class vueApplication(QMainWindow):

    def __init__(self, chemin: str = None):
        super().__init__()
        self.__chemin = chemin
        self.setWindowTitle("Application supermarché")
        self.setWindowIcon(QIcon(sys.path[0] + '/icones/cadie.jpg'))
        self.setGeometry(100, 100, 500, 300)

        # Charger les articles présents dans "liste_produits.json"
        chemin_json = os.path.join(sys.path[0], "liste_produits.json")
        with open(chemin_json, 'r') as f:
            data = json.load(f)

        # Barre de Menu
        menu_bar = self.menuBar()
        menu_theme = menu_bar.addMenu('&Projet')
        menu_theme.addAction('Nouveau projet')
        menu_theme.addAction('Ouvrir projet')

        # Dock contenant tous les différents types d'articles
        dock_articles = QDockWidget('Articles')
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_articles)
        dock_articles.setMaximumWidth(200)

        # Widget pour contenir le menu des articles
        widget_menu_articles = QWidget()
        layout_menu_articles = QVBoxLayout(widget_menu_articles)

        # Créer un menu déroulant pour les catégories d'articles
        menu_categorie = QMenu("Catégories", self)
        for categorie, articles in data.items():
            sous_menu_categorie = menu_categorie.addMenu(categorie)
            for article in articles:
                action = QAction(article, self)
                sous_menu_categorie.addAction(action)

        layout_menu_articles.addWidget(menu_categorie)
        dock_articles.setWidget(widget_menu_articles)
        
        
        # Widget central contenant le plan
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #taille dans laquelle l'image s'insérera
        image_size = (1150, 1150)

        # QLabel pour afficher l'image
        pixmap = QPixmap(sys.path[0] + '/icones/plan11.jpg')
        label = QLabel()
        label.setPixmap(pixmap.scaled(*image_size, Qt.AspectRatioMode.KeepAspectRatio))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ajouter le QLabel dans le widget central
        central_layout.addWidget(label)
        self.setCentralWidget(central_widget)

        self.showMaximized()

# Main pour tester la vue
if __name__ == "__main__":
    # création d'une QApplication
    app = QApplication(sys.argv)
    # création de la fenêtre de l'application
    fenetre = vueApplication()
    # lancement de l'application
    sys.exit(app.exec())
