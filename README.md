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
