# Projet Application supermarche

### Membres :

- PREVOST Louis
- FARDEL Mathéïs
- DEMOL Alexis
- CAPON Ethan

# Objectifs des deux applications

Positionner les produits sur un plan de magasin

Traçer un chemin efficace pour collecter les produits d'une liste de courses

# Contraintes de conception

Architecture MVC

Utilisation de PyQt

Utilisation exclusive des bibliothèques vues en cours

# Compte-rendu des séances

### 6/05/2024 de 13h à 14h30 :

- Membres présents physiquement : FARDEL Mathéïs, PREVOST Louis, DEMOL Alexis
- FARDEL Mathéïs : installation de git/pyqt6 sur ubuntu et accès au dépot git et création de la base + Brainstorming
- PREVOST Louis : création du dépot git et paramétrage de ce dernier + Brainstorming
- DEMOL Alexis : installation de git/pyqt6 sur ubuntu et accès au dépot git + Brainstorming

### 7/05/2024 de 10h à 11h30 :

- Membres présents physiquement : FARDEL Mathéïs, PREVOST Louis, DEMOL Alexis
- FARDEL Mathéïs : début de la vue de la première application (petit problème du déroulant du Dock à régler prochaine heure)
- PREVOST Louis : début de la vue de la seconde application
- DEMOL Alexis : code privisoire pour création de case afin d'y déposer les articles

### 7/05/2024 de 14h30 à 17h30 :

- Membres présents physiquement : FARDEL Mathéïs, PREVOST Louis, DEMOL Alexis
- FARDEL Mathéïs : Avancement de la vue de la première appli (menu déroulant des menu avec les articles du JSON + affichage du plan dans une zone défini)
- PREVOST Louis : Avancement vue seconde appli (barre d'outils et ouverture de fichiers)
- DEMOL Alexis: Progrès réalisés sur le code provisoire ; le quadrillage est désormais fonctionnel et chaque case est cliquable. On a besoin encore de quelques ajustements et assembler le code de Mathéïs et le mien qui est nécessaires.

### 14/05/2024 de 16h à 17h30 :

- Membres présents physiquement : FARDEL Mathéïs, PREVOST Louis, DEMOL Alexis, CAPON Ethan
- FARDEL Mathéïs : Tente de réparer le bug du Dock pour lequel le contenu disparaît si l'on clique dessus
- PREVOST Louis : Début du menu de création de liste de course
- DEMOL Alexis : Résolution du problème de taille pour certaines images trop grande pour certains écran(exemple: image 7-9)
- CAPON Ethan : Raccourci clavier app2 + début auto complétion dans un fichier test.

### 15/05/2024 de 10h à 11h30 :

- Membres présents physiquement : FARDEL Mathéïs, PREVOST Louis, DEMOL Alexis, CAPON Ethan
- FARDEL Mathéïs : tentative de réglage du bug du dock, étant donné que je ne réussis pas je passerai à autre chose prochaine heure.
- PREVOST Louis : Suite du menu de création de liste et sauvegarde en json.
- DEMOL Alexis : Ajout bouton modifier dans le docker pour les infos du magasins + fonctions + ajout de commentaire
- CAPON Ethan : Avancement auto complétion pour les listes.

### 15/05/2024 de 14h30 à 17h30 :

- Membres présents physiquement : FARDEL Mathéïs, PREVOST Louis, DEMOL Alexis, CAPON Ethan :
- FARDEL Mathéïs : Changement de la façon de faire le déroulant et utilisation d'un QTreeWidget (bien mieux et + beau sans bug) donc plus de bug, réalisation du bouton Modifier/Valider sur le dock des infos du magasin
- PREVOST Louis : Suite du menu de création de liste : affichage dans un dock sur le coté et zone de texte pour les articles.
- DEMOL Alexis : Enregister un projet et l'ouvrir + ajout commentaire + Ajout fonction pour sauvegarder les infos du docker + tentative test pour faire crash / bug le programme (aucun soucis détécté)
- CAPON Ethan : Avancement auto complétion pour les listes ( fini mais modification du json a faire).

### 16/05/2024 de 10h à 11h30 :

- Membres présents physiquement : FARDEL Mathéïs, PREVOST Louis, DEMOL Alexis :
- FARDEL Mathéïs : Mise en place du modèle MVC pour l'app 1 (tout était dans le même fichier avant car souci de compréhension de la méthode) Aujourd'hui + Hier soir
- PREVOST Louis : Suite du menu de création de liste : sauvegarde des objets ajouté disponible , plus qu'a ajouté l'auto complétion.
- DEMOL Alexis : Installation de GitHub sur windows pour pouvoir travailler plus rapidement + configuration. Quelque modif et création d'une branch (j'ai pas encore push les changements sur cette branch)

### 17/05/2024 de 8h30 à 11h30 :

- Membres présents physiquement : Aucuns (seul cours de la journée donc travail a distance) (seul cours de la journée donc travail a distance)
- FARDEL Mathéïs : "Ouvrir projet" debug + message d'erreur si on save alors qu'on a pas de projet en cours + si on modifie le dock des infos magasin, le json se met à jour + debug logo app qui n'apparait pas
- PREVOST Louis : Début du tri en mvc mais beaucoup de bug a patch ( voir tout refaire )
- DEMOL Alexis : Fonction pour supprimer un projet + Tentative de débogage des parties de l'image qui ne sont pas dans les cases mais qui sont clickable (Pas trouvé encore)

### 24/05/2024 de 10h à 11h30 et de 16h à 17h30 :

- Membres présents physiquement : FARDEL Mathéïs, PREVOST Louis, DEMOL Alexis, CAPON Ethan :
- FARDEL Mathéïs : Sur l'app1, en l'ouvrant tous les produits étaient dans le dock de gauche. J'ai donc permis que lors de la création du projet, il y ai un bouton pour choisir ses produits, ça ouvre une page où l'on coche les produits que l'on souhaite avoir dans notre magasin et uniquement ceux là sont présents dans le dock de gauche.
- PREVOST Louis : J'ai refait le mvc de l'app 2 de 0 car la version de la semaine derniere ne fonctionnait pas bien. ( Presque finit )
- DEMOL Alexis : Refonte quadrillage + ajout icone + refonte fonction sauvergarder_infos_magasin + petite modif
- CAPON Ethan : modification de l'auto complétion pour l'accès des fichiers + algo de dijkstra

### 27/05/2024 de 16h à 17h30 :
- Membres présents physiquement : FARDEL Mathéïs, DEMOL Alexis
- FARDEL Mathéïs : Reflexion à propos de la mise en place du système pour déposer sur le plateau des objets (sans résultats concrets pour le moment)
- DEMOL Alexis : Résolution du bug pour ouvrir un ancien projet (crash) + Réflexion et début pour ajouter des éléments dans les cases

### 28/05/2024 de 14h30 à 17h30 :
- Membres présents physiquement : FARDEL Mathéïs, PREVOST Louis, DEMOL Alexis
- FARDEL Mathéïs : Possibilité de mettre les objets dans les cases + en enregistrant un projet ça sauvegarde les cases, les objets etc... et en ouvrant un projet, les cases réapparaissent en rouge et le contenu est dedans
- PREVOST Louis : Toute les fonctions sont maintenant sous forme mvc + changement icones ect
- DEMOL Alexis: Possibilité de supprimer le contenu d'une case (avec la couleur qui se remet en noir), Correction du bug que quand on supprime le projet ca ne supprime pas la case rouge créer quand on ajoute un produit dans une case + debut de personnalisation d'affichage comme le theme sombre et le theme clair + petit changement.

### 30/05/2024 de 8h30 à 11h30 :
- Membres présents physiquement : FARDEL Mathéïs, DEMOL Alexis , PREVOST Louis
- FARDEL Mathéïs : lorsque l'on supprime un projet, il y a aussi la suppression du fichier json + debug affichage plan (en fait le souci venait du fichier json... avec d'autres ça fonctionne)
- DEMOL Alexis : Ajout fonction pour retirer et ajouter des colonnes après la création du projet + modif de quelque détail (Il faudras faire des changements pour modif les bug quand on modifie la taille du quadrillage quand on l'ouvre par exemple)
- PREVOST Louis : Ajout des styles (sombre / clair /default) et message d'information ; Prochaine séance ajout de l'ouverture des projets issus de l'app 1.

### 31/05/2024 de 10h à 11h30 et 14h30 à 16h :
- Membres présents physiquement : FARDEL Mathéïs, DEMOL Alexis , PREVOST Louis , CAPON Ethan
- FARDEL Mathéïs : lors de l'enregistrement, un dossier est créé contenant : le plan, un fichier json sur la position des objets, et les autres infos dans un autre fichier json
- DEMOL Alexis : ajout de fonction pour ajouter et retirer des lignes et colonnes sur le quadrillage avec des bloquages quand on ouvre ou créer un autre projet + Réglage du bug quand on ouvre une image trop grande et quand on crée un projet sans informations + d'autre petit détail 
- PREVOST Louis : Création d'une branche pour ajouter l'ouverture de magasin de l'app 1 ( Affiche uniquement le plan et le quadrillage )
- CAPON Ethan : Création d'une branche pour ajouter l'autocomplétation ( presque fini ) 

### 4/06 de 14h30 à 16h :
- Membres présents physiquement : Aucuns
- FARDEL Mathéïs : tentative de régler un bug : "can only concatenate tuple (not "str") to tuple" sans réussite pour le moment
- DEMOL Alexis : Ajustement + Ajout du théme sombre et clair

### 5/06 de 8h30 à 10h :
- Membres présents physiquement : FARDEL Mathéïs, Demol Alexis 
- FARDEL Mathéïs : Ajout de Entrée/Sortie dans les objets, et obligation de les mettre sur le plan pour pouvoir l'enregistrer (car besoin pour app2)
- Demol Alexis: Tentative d'enregistrer le projet que dans un dossier (le push de ce matin ca n'a pas fonctionné)

### 6/06 de 10h à 11h30 :
- Membres présents phtsiquement : FARDEL Mathéïs, DEMOL Alexis, PREVOST Louis, CAPON Ethan
- FARDEL Mathéïs : récupération de la création de dossier afin que le projet soit lisible sur différents PC et ajout qu'en cas de sauvegarde alors que le dossier du projet a déjà été crée, le JSON uniquement soit mis à jour (donc pouvoir enregistrer les avancées d'un projet déjà existant)