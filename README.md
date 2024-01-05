# Projet_Python_MongoDB
Système de Gestion de Bibliothèque avec MongoDB
Ce script Python offre un simple Système de Gestion de Bibliothèque utilisant MongoDB comme base de données. Il permet aux utilisateurs d'effectuer diverses opérations telles que la visualisation, l'ajout, la suppression, la modification de livres, et l'affichage de statistiques.

	Prérequis : Python 3.x ,MongoDB
	Bibliothèques Python requises : pymongo, pandas, colorama
# Installation
Installez les bibliothèques Python requises à l'aide de la commande suivante :

	bash
	Copy code >> pip install pymongo pandas colorama
	Assurez-vous que MongoDB est installé et en cours d'exécution sur localhost:27017.

# Naviguez à travers le menu en utilisant les options fournies :

	  1: Voir tous les livres
	  2: Rechercher des livres par critères
	  3: Ajouter un livre
	  4: Supprimer un livre
	  5: Modifier un livre
	  6: Voir les statistiques
	  7: Changer les options
	  8: Quitter
# Fonctionnalités
	Voir tous les livres (Option 1) : Affiche tous les livres ou un nombre spécifié de livres par page.
	
	Rechercher des livres par critères (Option 2) : Permet aux utilisateurs de rechercher des livres en fonction des auteurs, des titres ou des années. Prend en charge le tri et la pagination.
	
	Ajouter un livre (Option 3) : Ajoute un nouveau livre à la bibliothèque avec des attributs spécifiés.
	
	Supprimer un livre (Option 4) : Permet aux utilisateurs de supprimer un seul livre ou plusieurs livres en fonction de critères tels que l'auteur, le type ou l'année.
	
	Modifier un livre (Option 5) : Permet aux utilisateurs de mettre à jour les attributs d'un livre.
	
	Voir les statistiques (Option 6) : Fournit des informations statistiques telles que le nombre total et moyen de livres par auteur, type ou année. Prend en charge le tri et la pagination.
	
	Changer les options (Option 7) : Permet aux utilisateurs de modifier les options d'affichage, telles que le nombre d'éléments par page.
	
	Quitter (Option 8) : Quitte le programme.

# Remarque
	Assurez-vous de personnaliser l'URL de connexion à MongoDB (mongodb://localhost:27017/) et les noms de base de données/collection (my-first-db et books) en fonction de votre configuration MongoDB.

N'hésitez pas à améliorer et modifier le script en fonction de vos besoins spécifiques.
