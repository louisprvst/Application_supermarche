class File:
    """Classe File pour la gestion de la file d'attente utilisée dans l'algorithme de Dijkstra."""
    def __init__(self, taille_max):
        self.file = []
        self.taille_max = taille_max
    
    def enfiler(self, element):
        if len(self.file) < self.taille_max:
            self.file.append(element)
    
    def defiler(self):
        if not self.est_vide():
            return self.file.pop(0)
    
    def est_vide(self):
        return len(self.file) == 0

def creation_laby():
    """
    Crée un labyrinthe sous forme de liste de listes.
    0 représente un chemin, 1 représente un mur.
    """
    laby = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    return laby

def labyrinthe_vers_graphe(laby):
    """
    Convertit un labyrinthe en un graphe représenté par un dictionnaire.
    Les clés sont les positions (x, y) et les valeurs sont des dictionnaires des voisins accessibles.
    """
    graphe = {}
    ligne, case = len(laby), len(laby[0])
    
    for i in range(ligne):
        for j in range(case):
            if laby[i][j] == 0:
                voisins = {}
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < ligne and 0 <= nj < case and laby[ni][nj] == 0:
                        voisins[(ni, nj)] = 1  # Distance de 1 pour les voisins accessibles
                graphe[(i, j)] = voisins
    
    return graphe

def dijkstra(graphe: dict, depart: tuple, arrivee: tuple) -> dict:
    """
    Algorithme de Dijkstra pour trouver les chemins les plus courts dans un graphe.
    :param: graphe, dictionnaire des voisins du graphe
    :param: depart, tuple, sommet à partir duquel sont calculées les distances
    :param: arrivee, tuple, sommet d'arrivée
    :return: dictionnaire des distances par rapport aux sommets
    """
    file_attente = File(len(graphe))
    file_attente.enfiler(depart)
    distances = {sommet: float('inf') for sommet in graphe}
    distances[depart] = 0
    parents = {depart: None}

    while not file_attente.est_vide():
        sommet_courant = file_attente.defiler()
        
        if sommet_courant == arrivee:
            break

        for voisin in graphe[sommet_courant]:
            nouvelle_distance = distances[sommet_courant] + 1  # Poids de l'arête = 1 dans notre cas

            if nouvelle_distance < distances[voisin]:
                distances[voisin] = nouvelle_distance
                parents[voisin] = sommet_courant
                file_attente.enfiler(voisin)

    chemin = [arrivee]
    while chemin[-1] != depart:
        predecesseur = parents[chemin[-1]]
        chemin.append(predecesseur)

    chemin.reverse()
    return chemin if chemin[0] == depart else None



def afficher_laby(laby, path=[]):
    """
    Affiche le labyrinthe dans le terminal.
    """
    for i, ligne in enumerate(laby):
        for j, case in enumerate(ligne):
            if (i, j) in path:
                print('.', end='')  # Chemin
            elif case == 1:
                print('#', end='')  # Mur
            else:
                print(' ', end='')  # Chemin
        print()  # Nouvelle ligne à la fin de chaque rangée

# Créer le labyrinthe
laby = creation_laby()

# Convertir le labyrinthe en graphe
graphe = labyrinthe_vers_graphe(laby)


# Définir les points de départ et d'arrivée
start = (1, 1)  # Point de départ
end = (5, 4)    # Point d'arrivée

# Trouver le chemin de la sortie
chemin = dijkstra(graphe, start, end)

# Afficher le labyrinthe avec le chemin trouvé
if chemin:
    afficher_laby(laby, chemin)
else:
    print("Aucun chemin trouvé.")
          