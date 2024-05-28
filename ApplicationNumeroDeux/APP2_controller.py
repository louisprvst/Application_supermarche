import sys , APP2_model , APP2_vue
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal

################################################### APP2 CONTROLLER ###################################################

class controller() :
    

    # Constructeur : 
    
    def __init__(self) -> None:

        self.modele = APP2_model.model()
        self.vue = APP2_vue.vueApplication()
        
        self.popup_nl = APP2_vue.popup_new_liste()
    

    # Signaux de la fenetre principal :
    
        self.vue.MAINW_open_liste_signal.connect(self.open_liste)
        
        self.vue.MAINW_new_liste_signal.connect(self.new_liste)
        
        self.vue.MAINW_save_liste_signal.connect(self.save_liste)
        
        
    # Signaux de la popup nouvelle liste :
        
        self.popup_nl.POPNL_save_signal.connect(self.save_to_json)
        

    # Envoie des signaux :
    
    def new_liste(self) :
        self.popup_nl.show()
        
    def save_to_json(self , nom , date , filename) :
        self.modele.save_to_json(nom , date , filename)
        self.popup_nl.close()
        
    def open_liste(self , filename):       
    
        formated_data = self.modele.open_liste(filename)
        
        self.vue.update_list_view(formated_data)
        
    def save_liste(self , new_items , current_file) :
        self.modele.save_liste(new_items , current_file)
         
        
        
        
        
################################################### MAIN CONTROLLER ###################################################

if __name__ == "__main__" :
    
    app = QApplication(sys.argv)
    
    ctrl = controller()
    
    sys.exit(app.exec())