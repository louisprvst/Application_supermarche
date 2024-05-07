# Code provisoire pour les créations de case pour les rayons. Système quand on clique sur une case, une fenetre modale s'ouvre
# pour voir les produits disponible dans celui ci.
# La case ne se met pas directement sur l'image ! Il faut modifier cela.

# Alexis Demol TPB

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDialog
from PyQt6.QtGui import QPixmap

class Plateau(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # Plateau
        pixmap = QPixmap(sys.path[0] + '/icones/plan1.jpg')
        image_label = QLabel(self)
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label)

        # case
        case = QLabel(self)
        case.setFixedSize(100, 100)  
        case.setStyleSheet("border: 1px solid black;") 
        case.mousePressEvent = self.ouvrir_fenetre
        layout.addWidget(case)

        self.setLayout(layout)

    # ouverture fenetre 
    def ouvrir_fenetre(self, event):
        fenetre = FenetreTexte("\n Légumes")
        fenetre.exec()

class FenetreTexte(QDialog):
    def __init__(self, text):
        super().__init__()

        self.setWindowTitle("Fenetre texte test.")
        label = QLabel(f"Contenu du rayon: {text}")

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
        self.setFixedSize(800, 400)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Magasins")

        # Recup la taille de l'écran
        screen = QApplication.primaryScreen()  
        screenRes = screen.availableGeometry()  # Recup la res du screen dispo
        self.setGeometry(screenRes)
        self.plateau = Plateau()  # Crée l'instance du plateau
        self.setCentralWidget(self.plateau)  # met le plateau en screen principale

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
