import os
import sys
import json
from PyQt6.QtWidgets import QApplication, QLineEdit, QCompleter
from PyQt6.QtCore import Qt

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

# Initialisation de l'application PyQt6
app = QApplication(sys.argv)

# Création d'un QLineEdit
line_of_text = QLineEdit("")


# Obtenir le chemin absolu du répertoire du script
fichier = os.path.dirname(__file__)

# Construire le chemin relatif au fichier JSON
fichier_chemin = os.path.join(fichier, 'liste_produitsbis.json')

# Charger les noms de produits depuis le fichier JSON
liste = load_product_names(fichier_chemin)

# Configuration du QCompleter
completer = QCompleter(liste)
completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
completer.setFilterMode(Qt.MatchFlags.MatchContains)
line_of_text.setCompleter(completer)

# Affichage du QLineEdit
line_of_text.show()

# Lancement de l'application
sys.exit(app.exec())
