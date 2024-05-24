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
- DEMOL Alexis :
- CAPON Ethan : modification de l'auto complétion pour l'accès des fichiers + algo de dijkstra
