import os
import sys
import json
from PyQt6.QtWidgets import QApplication, QLineEdit, QCompleter, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QStringListModel

# Fonction pour charger les noms des produits à partir d'un fichier JSON
def load_product_names(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        print("JSON loaded successfully:", data)  # Message de débogage
        return list(data.values())  # Retourner les valeurs
    except FileNotFoundError:
        print(f"ERREUR : le fichier '{filename}' est introuvable.")
        return []  # Retourner une liste vide en cas d'erreur

class MultiCompleter(QCompleter):
    def __init__(self, words, parent=None):
        super(MultiCompleter, self).__init__(words, parent)
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setFilterMode(Qt.MatchFlags.MatchContains)
        self.model = QStringListModel(words, self)
        self.setModel(self.model)

    def pathFromIndex(self, index):
        path = super(MultiCompleter, self).pathFromIndex(index)
        text = self.widget().text()
        last_comma_index = text.rfind(',')
        if last_comma_index == -1:
            return path
        return text[:last_comma_index + 1] + ' ' + path

    def splitPath(self, path):
        last_comma_index = path.rfind(',')
        if last_comma_index == -1:
            return super(MultiCompleter, self).splitPath(path)
        return [path[last_comma_index + 1:].strip()]

    
# Initialisation de l'application PyQt6
app = QApplication(sys.argv)

# Création d'une fenêtre principale
main_window = QWidget()
layout = QVBoxLayout(main_window)

# Création d'un QLabel
label = QLabel("Recherche:")
layout.addWidget(label)

# Création d'un QLineEdit
line_of_text = QLineEdit()
layout.addWidget(line_of_text)

# Obtenir le chemin absolu du répertoire du script
fichier = os.path.dirname(__file__)

# Construire le chemin relatif au fichier JSON
fichier_chemin = os.path.join(fichier, 'liste_produitsbis.json')

# Charger les noms de produits depuis le fichier JSON
liste = load_product_names(fichier_chemin)

# Configuration du QCompleter personnalisé
completer = MultiCompleter(liste)
line_of_text.setCompleter(completer)

# Affichage de la fenêtre principale
main_window.show()

# Lancement de l'application
sys.exit(app.exec())
