# ALGO CHEMIN LOUIS:


    # Cette fonction permet retourner les coordonnées d'un produit precis , ne renvoie rien s'il n'est pas dans le magasin
    
    def trouver_index(self,produit, produits_dans_cases):
        for coord, produits in produits_dans_cases.items():
            if produit in produits:
                return coord
        return None
    
    # Permet de faire une liste des voisins de chaque case un dictionnaire

    def liste_voisins(self):
        adj_list = {}
        for i, case in enumerate(self.caseQuadrillage):
            adj_list[i] = self.get_voisins(i)
        return adj_list
    
    # Cette fonction permet d'obtenir les 4 voisins d'une case

    def get_voisins(self, index):
        adjacents = []
        lgn, cols = self.lgn, self.cols
        row, col = divmod(index, cols)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # haut, bas, gauche, droite

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < lgn and 0 <= c < cols:
                adjacents.append(r * cols + c)
        return adjacents
    
    # Cette fonction est la principal qui permet d'élaborer le chemin et renvoie le chemin une fois avoir visité chaque articles voulu

    def chemin(self, start_index, end_index, adj_list):
        queue = [(start_index, [start_index])]
        visited = set()

        while queue:
            current, path = queue.pop(0)
            if current == end_index:
                return path

            if current not in visited:
                visited.add(current)
                for neighbor in adj_list[current]:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))
        return []
    
    # Cette fonction permet de dessiner le chemin sur le plan :

    def dessiner_chemin(self, path):
        if not self.pixmap.isNull():
            painter = QPainter(self.pixmap)
            pen = QPen(Qt.GlobalColor.blue)
            pen.setWidth(2)
            painter.setPen(pen)

            for index in path:
                x1, y1, x2, y2 = self.caseQuadrillage[index]
                painter.drawRect(x1, y1, x2 - x1, y2 - y1)

            painter.end()
            self.image_label.setPixmap(self.pixmap)
            
    # Fonction pour lancer la création du chemin 

    def main_chemin(self,list,shop):
        
        # Ouverture des json :
        
        with open(list, 'r', encoding='utf-8') as f:
            articles_data = json.load(f)
        print(shop)
        with open(shop, 'r', encoding='utf-8') as f:
            coordinates_data = json.load(f)
            
        # On ajoute l'entrée a la main sinon elle ne se fait pas automatiquement

        articles_data["Liste des articles"].append("Entree du magasin")
        
        # On récupère uniquement certaines categorie dans les json ouvert 
        
        articles_list = articles_data["Liste des articles"]
        produits_dans_cases = coordinates_data["produits_dans_cases"]
        
        # On met les produits sous forme de tuple afin de faciliter la lecture

        produits_dans_cases_tuples = {
            tuple(map(int, key.strip("()").split(", "))): value
            for key, value in produits_dans_cases.items()
        }
        
        # On defini tout les articles a voir ( start_positions ) et la sortie du magasin ( end_psoitions )

        start_positions = [self.trouver_index(article, produits_dans_cases_tuples) for article in articles_list]
        end_positions = [self.trouver_index("Sortie du magasin", produits_dans_cases_tuples)] * len(start_positions)

        voisins = self.liste_voisins()
        for start_pos, end_pos in zip(start_positions, end_positions):
            if start_pos is not None and end_pos is not None:
                entree = self.caseQuadrillage.index(start_pos)
                sortie = self.caseQuadrillage.index(end_pos)
                path = self.chemin(entree, sortie, voisins)
                self.dessiner_chemin(path)