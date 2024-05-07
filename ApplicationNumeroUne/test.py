# Code provisoire pour les créations de case pour les rayons. Système quand on clique sur une case, une fenetre modale s'ouvre
# pour voir les produits disponible dans celui ci.
# Les cases sont mis directement sur l'image, malgrès ca il y a quand meme quelque soucis car cela se positionne pas parfaitement sur une bonne partie des images.

# Alexis Demol TPB

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class Plateau(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # Plateau
        pixmap = QPixmap(sys.path[0] + '/icones/plan11.jpg')
        self.image_label = QLabel(self)
        self.image_label.setPixmap(pixmap)

        layout.addWidget(self.image_label)
        self.createQuadrillage()

        self.setLayout(layout)

    def createQuadrillage(self):
        # Dimensions de la grille
        lgn = 30
        cols = 30
        cellLarg = self.image_label.pixmap().width() // cols
        cellHaut = self.image_label.pixmap().height() // lgn

        for row in range(lgn):

            for col in range(cols):

                cell = QLabel(self.image_label)
                cell.setGeometry(col * cellLarg, row * cellHaut, cellLarg, cellHaut)
                cell.setStyleSheet("border: 1px solid black;") # bordure en noir pour voir les zones ou on peut cliquer 
                cell.mousePressEvent = self.ouvrirFenetre

    # ouverture fenetre 
    def ouvrirFenetre(self, event):
        fenetre = FenetreTexte("\n Légumes")
        fenetre.exec()

class FenetreTexte(QDialog):
    def __init__(self, text):
        super().__init__()

        self.setWindowTitle("Fenetre texte test")
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
