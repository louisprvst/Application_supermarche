import os, sys ,json

################################################### APP2 MODEL ###################################################

class model():
        

    def save_to_json(self , nom , date , filename):
        
        data = {
            'listname': nom,
            'listdate': date
        }

        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
            
    def open_liste(self , filename):        
        
            with open(filename, 'r') as file:
                
                self.data = json.load(file)
                
                formatted_data = f"\n Nom : {self.data['listname']} \n\n Date : {self.data['listdate']}"
                
                return formatted_data