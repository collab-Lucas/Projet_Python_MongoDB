
from pymongo import MongoClient
from pprint import pprint
import pandas as pd
from colorama import Fore, Back, Style
import re
import random
#easy install >> cd C:\Users\Stagiaire\AppData\Local\Programs\Python\Python311\Scripts >> pip install pandas
client = MongoClient("mongodb://localhost:27017/")
db = client["my-first-db"]
collection=db["books"]


#COULEURS------------------------------------------------------------------
BLACK = Fore.BLACK
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
WARNING = '\033[93m'
UNDERLINE = '\033[4m'
BOLD = '\033[1m'
HEADER = '\033[95m'

LIGHT_RED = Fore.LIGHTRED_EX
LIGHT_GREEN = Fore.LIGHTGREEN_EX
LIGHT_BLUE = Fore.LIGHTBLUE_EX
LIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX
LIGHT_CYAN = Fore.LIGHTCYAN_EX
LIGHT_WHITE = Fore.LIGHTWHITE_EX

# Style (Bold, Dim, Normal, Reset_all)
BOLD = Style.BRIGHT
DIM = Style.DIM
NORMAL = Style.NORMAL
RESET_ALL = Style.RESET_ALL

#FONCTIONS-------------------------------------------------------------------

def aff_elem(resultats,selected_columns):
    df = pd.DataFrame(list(resultats))
    if not df.empty:
        df_selected = df[selected_columns]
        pd.set_option('display.max_colwidth', 70)

        print(df_selected)
    else:
        print("Aucun résultat trouvé.")

def aff_tout(resultats):
    df = pd.DataFrame(list(resultats))
    pd.set_option('display.max_colwidth', 30)
    pd.set_option('display.max_columns', None)
    print(df)
    pd.set_option('display.max_columns', 8)

def aff_elem_complet(resultats):
    if resultats:
        for livre in resultats:
            for attribut, valeur in livre.items():
                if attribut == '_id':
                    attribut = 'id'
                print(f"{attribut}: {valeur}")
    else:
        print("Livre non trouvé.")

def aff_stats(resultats):
    df = pd.DataFrame(list(resultats))

    if not df.empty:
        print("Tableau des valeurs :")
        print(df)

    else:
        print("Aucun résultat trouvé.")

def aff_avg(resultats):
    df = pd.DataFrame(list(resultats))

    if not df.empty:
        moyenne = df.at[0, 'moyenne']
        print(f"Moyenne : {moyenne}")
    else:
        print("Aucun résultat trouvé.")


def pagination(pipeline_personnalise,nb_fonction,choix_limit_affichage,selected_columns):
    page_number=1
    changer_page="1"
    while changer_page !="0":
        pipeline_page = pipeline_personnalise.copy()
        skip_count = (page_number - 1) * choix_limit_affichage
        count_doc = len(list(collection.aggregate(pipeline_page)))

        print("*------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*")
        print("Page numéro : ",page_number," ------------------   Nombre résultat :",count_doc)
        pipeline_page.append({"$skip": skip_count})
        pipeline_page.append({"$limit": choix_limit_affichage})
        if nb_fonction=="1": aff_elem(collection.aggregate(pipeline_page),selected_columns)
        elif nb_fonction=="2": aff_stats(collection.aggregate(pipeline_page))
        elif nb_fonction=="3": aff_tout(collection.aggregate(pipeline_page))
        changer_page = input("\n Changer de page ? (0 :pour quitter, 1: pour avancer ➡️, 2: pour reculer ⬅️)   \n")
        if changer_page=="1":
            if ((page_number - 1) * choix_limit_affichage)+choix_limit_affichage < count_doc:
                page_number=page_number+1
            else:
                print(WARNING+"⚠️ //////////////////*Error *  --------------  page limit ⚠️"+ RESET_ALL)
        else :
            if changer_page=="2":
                if page_number > 1:
                    page_number=page_number-1
                else :
                    print(WARNING+"⚠️ //////////////////*Error *  --------------  page limit ⚠️"+ RESET_ALL)        
    


#MENU----------------------------------------------------------------------
i=1
choix_limit_affichage=10
selected_columns = ["title", "authors", "year", "type"]
while i>=1 and i<=7:

    print(UNDERLINE +HEADER+"📚     Menu :"+RESET_ALL)
    print("1: 📖  Afficher tous les livres")
    print("2: 🤔  Afficher les livres par critère")
    print("3: ➕  Ajouter un livre ")
    print("4: 🗑️   Supprimer un livre ")
    print("5: ✏️   Modifier un livre ")
    print("6: 📈  Statistiques ")
    print("7: ⚙️   Options ")
    print(RED+"8: 🚽  Quitter "+RESET_ALL)
    i = int(input())

    if i == 1:
        pipeline_personnalise=[]
        pipeline_personnalise.append({"$match":{}})
        pagination(pipeline_personnalise, "3",choix_limit_affichage,selected_columns)

    #RECHERCHE----------------------------------------------------------------------
    if i == 2:
        print(UNDERLINE+"🔍  RECHERCHE  🔍"+RESET_ALL)
        pipeline_personnalise = []
        t=1
        choix_t=[]

        base_aggregate=[]
        option_de_tri=0
        option_de_filtre=0

        while t != 0 and t != 4:
            print("Voulez-vous ajoutez un critère ? 0 pour Quitter, 4 pour continuer")
            if 1 not in choix_t:
                print("1: par auteur")
            if 2 not in choix_t:
                print("2: par titre")
            if 3 not in choix_t:
                print("3: 🗓️ par année")
        
            t = int(input("Choix:"))
            if t not in choix_t:
                if t == 1:
                    auteurs = input("Auteurs : ")
                    pipeline_personnalise.append({"$match": {"authors":{"$regex": re.compile(re.escape(auteurs), re.IGNORECASE)}}})
                    choix_t.append(t)
                elif t == 2:
                    titre = input("Titre : ")
                    pipeline_personnalise.append({"$match": {"title":{"$regex": re.compile(re.escape(titre), re.IGNORECASE)}}})
                    choix_t.append(t)
                elif t == 3:
                    choix_op=0
                    while choix_op not in [1,2,3,4]:
                        print("Choix d'opération :")
                        print("1 : Si Année = sélection")
                        print("2 : Si Année < sélection")
                        print("3 : Si Année > sélection")
                        print("4 : Si Année entre sélection 1 et sélection 2")
                        choix_op=int(input("choix d'opération : "))
                        if choix_op == 1:
                            op="$eq"
                        elif choix_op == 2:
                            op="$lt"
                        elif choix_op == 3:
                            op="$gt"
                        elif choix_op == 4:
                            annee1 = int(input("Année infèrieure : "))
                            annee2 = int(input("Année supèrieur : "))
                            pipeline_personnalise.append({"$match": {"year": {"$gte": annee1}}})
                            pipeline_personnalise.append({"$match": {"year": {"$lte": annee2}}})
                        else:
                            print("Choix invalide")

                        if choix_op !=4:
                            annee = int(input("Année : "))
                            pipeline_personnalise.append({"$match": {"year": {op: annee}}})

                    choix_t.append(t)
                if len(choix_t) == 3:
                    t =4
            elif t ==4:
                break
            else:
                print("critère déja choisi") 

        if t!= 0:
            trie =1
            while trie >0 and trie <3:
                trie=int(input("Voulez vous rajouter un trie ? 0  pour rien , 1 pour trie par auteur , 2 par titre ,3 par annee  : "))
                if trie >0:
                    typetrie=input("Quelle type de trie croissant/décroissant ? 1 croissant, 2 décroissant  : ")
                    if trie==1: texttrie="authors"
                    if trie==2: texttrie="title"
                    if trie==3: texttrie="year"
                    
                    pipeline_personnalise.append({"$sort": {texttrie: int(typetrie)}})

            pagination(pipeline_personnalise,"1",choix_limit_affichage,selected_columns)       

    #AJOUT----------------------------------------------------------------------
    if i == 3:
        print(UNDERLINE+"Ajout de livre"+RESET_ALL)

        titre=input("titre:")
        type=input("type:")
        annee=input("annee:")
        id= titre+""+type+annee+str(random.randint(100, 2000))+"_"+str(random.randint(100, 2000))
        auteur=[]
        aut =0
        while aut ==0:
            nom_auteur=input("Nom de l'auteur:")
            auteur.append(nom_auteur)
            aut=int(input("Voulez-vous ajouter un autre auteur 0 oui/ 1 non ? "))

        collection.insert_one({"_id":id,"title":titre,"type":type,"year":int(annee),"authors":auteur})

    #SUPPRESSION----------------------------------------------------------------------
    if i == 4: 
        l=1
        while l >=1 and l <=2:
            print(UNDERLINE+LIGHT_RED+"Sélection de mode de Suppression :"+RESET_ALL)
            print("1: Suppression unique/simple par id")
            print("2: Suppression multiple/complexe")
            print("0: Quitter")
            l=int(input("Choix du mode de suppression:"))
            if l == 1:
                id=input("Id du livre:")
                collection.delete_one({"_id":{"$eq":id}})
            if l == 2:
                s=0
                while s >=1 and s <=3:
                    print(UNDERLINE+LIGHT_RED+"Sélection de mode de Suppression complexe :"+RESET_ALL)
                    print("1: Suppression des livres par auteur")
                    print("2: Suppression des livres par type")
                    print("3: Suppression des livres par année")
                    print("0: Quitter")
                    s=int(input("Choix du mode de suppression complexe:"))
                    if s == 1:
                        nom_auteur=input("Nom de l'auteur:")
                        collection.delete_many({"authors":{"$eq":nom_auteur}})
                    if s == 2:
                        type=input("Type de livre:")
                        collection.delete_many({"type":{"$eq":type}})
                    if s == 3:
                        annee=int(input("Annee:"))
                        collection.delete_many({"year":{"$eq":nom_auteur}})

    #MODIFICATION-----------------------------------------------------------------------------------------
    if i == 5:
        print(UNDERLINE+"MODIFCATION"+RESET_ALL)
        livre_id_recherche = input(LIGHT_CYAN+"Entrez l'ID du livre à rechercher : "+RESET_ALL)
        livre_recherche=collection.find({"_id": livre_id_recherche}) 
        nouveaux_attributs = {}
        if livre_recherche:
            print("Livre trouvé : \n")
            aff_elem_complet(livre_recherche)

            nouveaux_attributs = {}
            print("laissez vide  si vous ne voulez pas modifier")
            new_title = input("Nouveau titre : ")
            if new_title != "":
                nouveaux_attributs["title"] = new_title

            new_authors = input("Nouveaux auteurs (séparés par des virgules) : ")
            if new_authors != "":
                nouveaux_attributs["authors"] = [author.strip() for author in new_authors.split(',')]

            new_year = input("Nouvelle année : ")
            if new_year != "":
                nouveaux_attributs["year"] = int(new_year)

            new_type = input("Nouveau type : ")
            if new_type != "":
                nouveaux_attributs["type"] = int(new_type)

            if nouveaux_attributs:
                collection.update_one({"_id": livre_id_recherche}, {"$set": nouveaux_attributs})
                print("Livre mis à jour avec succès.")
            else:
                print("Aucune modification n'a été effectuée.")
        else:
            print("Aucun livre trouvé avec cet ID.")

    #STATS-----------------------------------------------------------------------------------------
    if i == 6:
        print(UNDERLINE+"STATISTIQUES"+RESET_ALL)
        pipeline_personnalise = []
        t=0
        tf=1
        base_aggregate=[]
        option_de_tri=0
        option_de_filtre=0

        while t < 1 or t > 3  :
            print(LIGHT_GREEN+"Voulez-vous ajoutez un critère moy/total par auteur/titre/année ? 0 pour Quitter "+RESET_ALL)
            print("1: par auteur")
            print("2: par type")
            print("3: par année")
            t = int(input("Choix:"))
            if t == 1:
                texttrie="authors"
            elif t == 2:
                texttrie="type"
            elif t == 3:
                texttrie="year"

            pipeline_personnalise.append({"$unwind": f"${texttrie}"})
            pipeline_personnalise.append({"$group": {"_id": f"${texttrie}","total": {"$sum": 1}}})
            pipeline_avg =pipeline_personnalise.copy()
            pipeline_avg.append({"$group": {"_id": None, "moyenne": {"$avg": "$total"}}})

        trie =0
        while trie <1 or trie >2:
            trie=int(input(LIGHT_GREEN+"Voulez vous rajouter un trie ?  1 pour trie par critère auteur/titre/année , 2 par valeur "+RESET_ALL+"\n"))
            if trie >0:
                typetrie=input("Quelle type de trie croissant/décroissant ?  1 croissant, 2 décroissant \n")
                if int(typetrie) ==2:typetrie=-1
                if trie ==1:
                    choixtrie="_id"
                elif trie ==2:
                    choixtrie="total"
                pipeline_personnalise.append({"$sort": {choixtrie: int(typetrie)}})

        aff_avg(collection.aggregate(pipeline_avg))

        pagination(pipeline_personnalise,"2",choix_limit_affichage,selected_columns)

    #OPTIONS-----------------------------------------------------------------------------------------
    if i == 7:
        t=1
        while t !=0  :
            print(LIGHT_GREEN+"OPTIONS "+RESET_ALL)
            print("1: limite par page")
            print("2: élément du tableau/colonne")
            t = int(input("Choix : "))

            if t ==1:
                choix_limit_affichage=0
                while choix_limit_affichage <=0:
                    choix_limit_affichage = input("Nouvelle limite d'élément par page : ")
            elif t ==2:
                selected_columns = ["title", "authors", "year", "type"]
                nv_tab=[]
                choix_opt=1
                while choix_opt !=0  :
                    print("Sélectionner les éléments à afficher lors des résultats , ils s'afficheront en colonne dans l'ordre choisi. 0 : Quitter")
                    print("1: id")
                    print("2: type")
                    print("3: year")
                    print("4: titre")
                    print("5: authors")
                    print("6: page")
                    print("7: publieur")
                    print("8: url")
                    choix_opt = int(input("Element : "))
                    if choix_opt == 1:
                        nv_tab.append("_id")
                    elif choix_opt == 2:
                        nv_tab.append("type")
                    elif choix_opt == 3:
                        nv_tab.append("year")
                    elif choix_opt == 4:
                        nv_tab.append("title")
                    elif choix_opt == 5:
                        nv_tab.append("authors")
                    elif choix_opt == 6:
                        nv_tab.append("pages")
                    elif choix_opt == 7:
                        nv_tab.append("booktitle")
                    elif choix_opt == 8:
                        nv_tab.append("url")
                    selected_columns=nv_tab.copy()

