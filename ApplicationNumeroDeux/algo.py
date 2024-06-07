def trouver_index(self,produit, produits_dans_cases):
        for coord, produits in produits_dans_cases.items():
            if produit in produits:
                return coord
        return None

    def liste_voisins(self):
        adj_list = {}
        for index, case in enumerate(self.caseQuadrillage):
            adj_list[index] = self.get_voisins(index)
        return adj_list

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

    def main_chemin(self):
        script_directory = sys.path[0]
        json_file_path = os.path.join(script_directory, 'b.json')
        with open(json_file_path, 'r', encoding='utf-8') as f:
            articles_data = json.load(f)

        json_file_path = os.path.join(script_directory, 'a/a.json')
        with open(json_file_path, 'r', encoding='utf-8') as f:
            coordinates_data = json.load(f)

        articles_data["Liste des articles"].append("Entree du magasin")
        
        articles_list = articles_data["Liste des articles"]
        produits_dans_cases = coordinates_data["produits_dans_cases"]

        produits_dans_cases_tuples = {
            tuple(map(int, key.strip("()").split(", "))): value
            for key, value in produits_dans_cases.items()
        }

        start_positions = [self.trouver_index(article, produits_dans_cases_tuples) for article in articles_list]
        end_positions = [self.trouver_index("Sortie du magasin", produits_dans_cases_tuples)] * len(start_positions)

        voisins = self.liste_voisins()
        for start_pos, end_pos in zip(start_positions, end_positions):
            if start_pos is not None and end_pos is not None:
                entree = self.caseQuadrillage.index(start_pos)
                sortie = self.caseQuadrillage.index(end_pos)
                path = self.chemin(entree, sortie, voisins)
                self.dessiner_chemin(path)