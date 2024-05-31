import os
import sys
import json
from PyQt6.QtWidgets import QApplication, QLineEdit, QCompleter
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

# Fonction pour ajouter un élément sélectionné avec une virgule
# Fonction pour ajouter un élément sélectionné avec une virgule
# Fonction pour ajouter un élément sélectionné avec une virgule
def add_completer_text(text):
    current_text = line_of_text.text()
    # Supprimer la partie de texte en cours de complétion
    if ", " in current_text:
        current_text = current_text.rsplit(", ", 1)[0] + ", "
    else:
        current_text = ""

    current_text += text
    line_of_text.setText(current_text)
    # Positionner le curseur à la fin
    line_of_text.setCursorPosition(len(line_of_text.text()))

    # Réinitialiser le QCompleter pour permettre une nouvelle autocomplétion
    completer.setCompletionPrefix("")
    completer.complete()


# Initialisation de l'application PyQt6
app = QApplication(sys.argv)

# Création d'un QLineEdit
line_of_text = QLineEdit()

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

# Connecter le signal de sélection du QCompleter à la fonction personnalisée
completer.activated[str].connect(add_completer_text)

# Affichage du QLineEdit
line_of_text.show()

# Lancement de l'application
sys.exit(app.exec())
