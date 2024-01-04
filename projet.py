
from pymongo import MongoClient
from pprint import pprint
import pandas as pd

client = MongoClient("mongodb://localhost:27017/")
db = client["my-first-db"]

#FONCTIONS-------------------------------------------------------------------

def aff_elem(resultats):
    df = pd.DataFrame(list(resultats))
    selected_columns = ["title", "authors", "year", "type"]
    df_selected = df[selected_columns]
    pd.set_option('display.max_colwidth', None)

    print(df_selected)

def aff_elem_complet(resultats):
    if resultats:
        livre = resultats[0]

        for attribut, valeur in livre.items():
            if attribut == '_id':
                attribut = 'id'
            print(f"{attribut}: {valeur}")
    else:
        print("Livre non trouvé.")

#MENU----------------------------------------------------------------------
i=1
while i>=1 and i<=6:

    print("Menu :")
    print("1: Afficher tous les livres")
    print("2: Afficher les livres par critère")
    print("3: Ajouter un livre ")
    print("4: Supprimer un livre ")
    print("5: Modifier un livre ")
    print("6: Statistiques ")
    print("7: Quitter ")
    i = int(input())

    if i == 1:
        None
        # for item in db["users"].find():
        #    pprint.pprint(item)

    #RECHERCHE----------------------------------------------------------------------
    if i == 2:
        pipeline_personnalise = []
        t=1
        choix_t=[]

        base_aggregate=[]
        option_de_tri=0
        option_de_filtre=0

        while t != 0 and len(choix_t)!=3 :
            print("Voulez-vous ajoutez un critère ? 0 pour Quitter")
            if 1 not in choix_t:
                print("1: par auteur")
            if 2 not in choix_t:
                print("2: par titre")
            if 3 not in choix_t:
                print("3: par année")
        
            t = int(input("Choix:"))
            if t not in choix_t:
                if t == 1:
                    auteurs = input("Auteurs : ")
                    pipeline_personnalise.append({"$match": {"authors": {"$eq": auteurs}}})
                    choix_t.append(t)
                elif t == 2:
                    titre = input("Titre : ")
                    pipeline_personnalise.append({"$match": {"title": {"$eq": titre}}})
                    choix_t.append(t)
                elif t == 3:
                    annee = int(input("Année : "))
                    pipeline_personnalise.append({"$match": {"year": {"$eq": annee}}})
                    choix_t.append(t)
            else:
                print("critère déja choisi") 
        trie =1
        while trie >0 and trie <3:
            trie=int(input("Voulez vous rajouter un trie ? 0  pour rien , 1 pour trie par auteur , 2 par titre ,3 par annee"))
            if trie >0:
                typetrie=input("Quelle type de trie croissant/décroissant ? 1 croissant, 2 décroissant")
                if trie==1: texttrie="authors"
                if trie==2: texttrie="title"
                if trie==3: texttrie="year"
                
                pipeline_personnalise.append({"$sort": {texttrie: int(typetrie)}})

        page_number=1
        changer_page="1"
        while changer_page !="0":
            skip_count = (page_number - 1) * 10
            count_doc = len(list(db["books"].aggregate(pipeline_personnalise)))

            print("*------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*")
            print("Page numéro : ",page_number," ------------------   Nombre résultat :",count_doc)
            pipeline_personnalise.append({"$skip": skip_count})
            pipeline_personnalise.append({"$limit": 10})
            aff_elem(db["books"].aggregate(pipeline_personnalise))
            changer_page = input("\n Changer de page ? (0 :pour quitter,1: pour avancer,2: pour reculer)   ")
            if changer_page=="1":
                if ((page_number - 1) * 10)+10 < count_doc:
                    page_number=page_number+1
                else:
                    print("*Error *  --------------  page limit")
            else :
                if changer_page=="2":
                    if page_number > 1:
                        page_number=page_number-1
                    else :
                        print("*Error *  --------------  page limit")                

    #AJOUT----------------------------------------------------------------------
    if i == 3:
        print("Ajout de livre")
        titre=input("titre:")
        type=input("type:")
        annee=input("annee:")
        auteur=[]
        aut =0
        while aut ==0:
            nom_auteur=input("Nom de l'auteur:")
            auteur.append(nom_auteur)
            aut=int(input("Voulez-vous ajouter un autre auteur 0 oui/ 1 non?"))

        db["books"].insert_one({"title":titre,"type":type,"year":int(annee),"authors":auteur})


    #SUPPRESSION----------------------------------------------------------------------
    if i == 4: 
        l=1
        while l >=1 and l <=2:
            print("Sélection de mode de Suppression :")
            print("1: Suppression unique/simple par id")
            print("2: Suppression multiple/complexe")
            print("0: Quitter")
            l=int(input("Choix du mode de suppression:"))
            if l == 1:
                id=input("Id du livre:")
                db["books"].delete_one({"_id":{"$eq":id}})
            if l == 2:
                s=0
                while s >=1 and s <=3:
                    print("Sélection de mode de Suppression complexe :")
                    print("1: Suppression des livres par auteur")
                    print("2: Suppression des livres par type")
                    print("3: Suppression des livres par année")
                    print("0: Quitter")
                    s=int(input("Choix du mode de suppression complexe:"))
                    if s == 1:
                        nom_auteur=input("Nom de l'auteur:")
                        db["books"].delete_many({"authors":{"$eq":nom_auteur}})
                    if s == 2:
                        type=input("Type de livre:")
                        db["books"].delete_many({"authors":{"$eq":type}})
                    if s == 3:
                        annee=int(input("Annee:"))
                        db["books"].delete_many({"year":{"$eq":nom_auteur}})
    #MODIFICATION-----------------------------------------------------------------------------------------
    if i == 5:
        livre_id_recherche = input("Entrez l'ID du livre à rechercher : ")
        livre_recherche=db["books"].find({"_id": livre_id_recherche}) 
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
                db["books"].update_one({"_id": livre_id_recherche}, {"$set": nouveaux_attributs})
                print("Livre mis à jour avec succès.")
            else:
                print("Aucune modification n'a été effectuée.")
        else:
            print("Aucun livre trouvé avec cet ID.")
    #STATS-----------------------------------------------------------------------------------------
    if i == 6:
        None
    #     nom=input("Nom user rechercher:")
    #     nomremp=input("Nom user à remplacer:")
    #     age=input("Age:")
    #     email=input("Email:")
        # if nomremp !="":
        # if age!="":
        # if email!="":
        # db["users"].update_one({"name":nom},{"name":nomremp,"age":int(age),"email":email})



# me=db["users"].aggregate([{"$match": {"email":"je@email.com"}}])
# #print(db["users"].find()[0])  
# print(me)
        
# _id:"series/cogtech/Zancanaro12"
# type:"Article"
# title:"Shared Interfaces for Co-located Interaction."
# pages:Object
#     start:71
#     end:88
# year:2012
# booktitle:"Ubiquitous Display Environments"
# url:"db/series/cogtech/364227662.html#Zancanaro12"

# authors:Array (1):0:"Massimo Zancanaro"
                        # series/cogtech/Zancanaro12
                        # series/cogtech/Wahlster13
        
