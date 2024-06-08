import json

################################################### APP2 MODEL ###################################################

class model():  
    
    # Ces fonctions sont issues de l'application 1 :
    
    def __init__(self):
        self.details_projet = {}

    def charger_produits(self, chemin_fichier):
        try:
            with open(chemin_fichier, 'r') as f:
                produits = json.load(f)
            return produits
        except Exception as e:
            print(f"Erreur lors du chargement des produits: {e}")
            return {}
    
    def mettre_a_jour_details(self, details):
        self.details_projet.update(details)

    def charger_projet(self, chemin_fichier):
        try:
            with open(chemin_fichier, 'r') as f:
                details_projet = json.load(f)
            return details_projet
        except Exception as e:
            raise IOError(f"Erreur lors du chargement du projet: {e}") 
        
    # Cette fonction permet d'enregistrer une liste mais uniquement lors de sa création 

    def save_to_json(self , nom , date , filename):
        
        data = {
            'listname': nom,
            'listdate': date
        }

        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
            
    # Cette fonction permet de récuperer les informations d'une liste en format json et le renvoie
                  
    def open_liste(self , filename):        
        
        with open(filename, 'r') as file:
            
            self.data = json.load(file)
            
            formatted_data = f"\n Nom : {self.data['listname']} \n\n Date : {self.data['listdate']}"
            
            return formatted_data
            
    # Cette fonction de récuperer le contenu d'une liste en format json et le renvoie

    def open_liste_items(self, filename):
        
        with open(filename, 'r') as file:
            
            self.data = json.load(file)
            
            articles = self.data.get('Liste des articles', [])
            
            data_items = ""
            
            if articles:
                data_items += ", ".join(articles)
            
            return data_items
        
    # Cette fonction permet de sauvegarder une liste qui est créer
            
    def save_liste(self , new_items , current_file):
        
        # Initialiser self.data s'il n'est pas déjà initialisé
        if "Liste des articles" not in self.data:
            self.data["Liste des articles"] = []
            
        self.data["Liste des articles"].extend(new_items)
        
        # Supprimer les doublons
        self.data["Liste des articles"] = list(set(self.data["Liste des articles"]))
        
        # Enregistrer les données mises à jour dans le fichier JSON
        with open(current_file, "w") as json_file:
            json.dump(self.data, json_file, indent=4) 