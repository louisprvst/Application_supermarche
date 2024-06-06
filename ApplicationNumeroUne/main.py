# ============================================================================================================================================================
#                                                     Main de l'application numéro une
#                                                   Fait par FARDEL Mathéïs et DEMOL Alexis
#=============================================================================================================================================================

import sys
from PyQt6.QtWidgets import QApplication
from controllerApplication import Controller

# Fonction principale de l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.view.show()
    sys.exit(app.exec())
