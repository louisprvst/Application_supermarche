import sys
import json
from PyQt6.QtWidgets import QApplication, QLineEdit, QCompleter
from PyQt6.QtCore import Qt

# Fonction pour charger les noms des produits à partir d'un fichier JSON
def load_product_names(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        print("JSON loaded successfully:", data)  # Message de débogage
        return list(data.keys())
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' is not a valid JSON.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

# Initialisation de l'application PyQt6
app = QApplication(sys.argv)

# Création d'un QLineEdit
line_of_text = QLineEdit("")

# Chargement des noms de produits depuis le fichier JSON
word_bank = load_product_names("liste_produitsbis.json")
print("Word bank:", word_bank)  # Message de débogage

# Vérification si la word_bank est vide
if not word_bank:
    print("No products loaded. Exiting.")
    sys.exit(1)

# Configuration du QCompleter
completer = QCompleter(word_bank)
completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
completer.setFilterMode(Qt.MatchFlag.MatchContains)
line_of_text.setCompleter(completer)

# Affichage du QLineEdit
line_of_text.show()

# Lancement de l'application
sys.exit(app.exec())
