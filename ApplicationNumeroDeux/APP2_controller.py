import sys , os , APP2_model , APP2_vue
from PyQt6.QtWidgets import QApplication,QFileDialog


################################################### APP2 CONTROLLER ###################################################

class controller() :

# Constructeur : 
    
    def __init__(self) -> None:

        self.modele = APP2_model.model()
        self.vue = APP2_vue.vueApplication()
        
        self.popup_nl = APP2_vue.popup_new_liste()
        
        self.chemin_projet = None

# Signaux de la fenetre principal :
    
        self.vue.MAINW_open_liste_signal.connect(self.open_liste)
        
        self.vue.MAINW_new_liste_signal.connect(self.new_liste)
        
        self.vue.MAINW_save_liste_signal.connect(self.save_liste)
        
        self.vue.MAINW_open_shop_signal.connect(self.ouvrir_projet)
        
        self.popup_nl.POPNL_save_signal.connect(self.save_to_json)
        
# Envoie des signaux :
    
    def new_liste(self) :
        self.popup_nl.show()
        
    def save_to_json(self , nom , date , filename) :
        self.modele.save_to_json(nom , date , filename)
        self.popup_nl.close()
        self.vue.new_message_info("Information","Nouvelle liste créer avec succès")
        self.open_liste(filename)
        
    def open_liste(self , filename):       
        formated_data = self.modele.open_liste(filename)
        mes_articles = self.modele.open_liste_items(filename)
        self.vue.currentfile = filename
        self.vue.update_list_view(formated_data,mes_articles)
        self.vue.new_message_info("Information","Liste ouverte avec succès")
   
    def save_liste(self , new_items , current_file) :
        self.modele.save_liste(new_items , current_file)
        self.vue.new_message_info("Information","Liste sauvegarder avec succès")
        

################################################### CODE DE L'APP 1 ###################################################    
        
    def ouvrir_projet(self):
        chemin_dossier = QFileDialog.getExistingDirectory(self.vue, "Sélectionner le dossier du projet à ouvrir")
        if chemin_dossier:
            nom_projet = os.path.basename(chemin_dossier)
            chemin_fichier_projet = os.path.join(chemin_dossier, f"{nom_projet}.json")
            
            details_projet = self.modele.charger_projet(chemin_fichier_projet)
            chemin_image = os.path.join(chemin_dossier, details_projet['chemin_image'])
            details_projet['chemin_image'] = chemin_image

            self.vue.plateau.chargerImage(chemin_image)
            self.vue.plateau.createQuadrillage(details_projet['lgn'], details_projet['cols'], details_projet['dimX'], details_projet['dimY'])
            
            self.modele.mettre_a_jour_details(details_projet)

            # Convertir les clés des cases de chaînes en tuples
            produits_dans_cases = {eval(k): v for k, v in details_projet.get('produits_dans_cases', {}).items()}
            self.vue.plateau.produits_dans_cases = produits_dans_cases
            for case in self.vue.plateau.produits_dans_cases:
                self.vue.plateau.mettre_a_jour_case(case, afficher_message=False)

            self.chemin_projet = chemin_fichier_projet
            self.dossier_projet = chemin_dossier

            self.plan_modifiable = True 
            
################################################### MAIN CONTROLLER ###################################################

if __name__ == "__main__" :
    
    app = QApplication(sys.argv)
    
    ctrl = controller()
    
    sys.exit(app.exec())