import sys
from PyQt6.QtWidgets import QApplication
from APP2_controller import controller

################################################### MAIN CONTROLLER ###################################################

# Veuillez exécuter ce programme afin de lancer la seconde application, MarketItemFinder.

if __name__ == "__main__" :
    
    app = QApplication(sys.argv)
    
    ctrl = controller()
    
    sys.exit(app.exec())
