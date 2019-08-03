#   Le principe du chunking est présent dans la plupart des bouquins sur le NLP
#   exemple : "Oreilly chunking with Python"


# BUT : améliorer le nombre de couples de produits qui matchent
# pour le BIO en utilisant en plus :
# - les entités en MAJUSCULES et celles entre guillemets
# - une métrique fonction de la proportion de mots retrouvés dans les titres
#   par l'extraction des entités. Ce qui permet potentiellement de trouver 
# plus de couples qui matchent

# Autre question : comment paramétrer :
#     - un titre particulier à découper
#     - l'ajout de corpus = ajout de descriptions ?

# Pour l'instant, pas question d'utiliser des expressions régulières en NP, ADJP, ADVP et PP
# qui peuvent etre spécifiques au vin, BIO, smartphones, etc ...

# Et toutes les entités trouvées = vocabulaires d'entités qui servent à découper les titres plus finement que 
# la méthode "chunking" NLP 


#--------------------------------------------------------------------------------------------------------------------#
#--- Les marques sont intéressantes à visualiser avec t-sne On pourrait aussi : -------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#
#--- * les utiliser comme "words" afin de calculer leurs embeddings -------------------------------------------------#
#--- * les utiliser afin de réaliser un modèle "Brand Entity Recognition" avec --------------------------------------#
#--- * un RNN (LSTM) à partir des titres ----------------------------------------------------------------------------#
#--- * peut se généraliser aussi au vin avec les Producteurs équivalents aux brands du BIO --------------------------#
#--------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- step_0_import_data --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

# A faire au début, pour utiliser "%autoreload" : 
# %load_ext autoreload
# %autoreload


# Toutes les librairies utiles
import pandas as pd
import operator
import numpy as np
import re
import itertools
import datetime
import argparse
import os

# 17/05/2019: correction suite à l'exécution de Hervé
# On a besoin de "punkt"
import nltk
nltk.download('punkt')


# Toutes les fonctions utiles
from functions import fun_step_1_create_df as step_1
from functions import fun_step_2_data_cleansing as step_2
from functions import fun_step_3_ngrams as step_3
from functions import fun_step_4_chunks as step_4
from functions import fun_step_5_ngrams_overlapped_and_not_overlapped as step_5
from functions import fun_step_6_get_preliminary_results as step_6
from functions import fun_step_7_extract_upper_entities as step_7
from functions import fun_step_8_extract_double_quotes_entities as step_8
from functions import fun_step_9_entities_found_to_str as step_9
from functions import fun_step_10_extract_combined_one_two_three_four_five_entities as step_10
from functions import fun_step_11_couples_final as step_11

# Option pour afficher entièrement le contenu des colonnes
# pd.set_option('display.max_colwidth',-1)


# Chemin des données source et chemin des données en sortie
# path_root = "/home/hapax94/Documents/vincent/jupyter"

path_root = os.getcwd().replace("/carrefour_chunking_bio/scripts",'')
path_output = "/carrefour_chunking_bio/output"

# Case 1 : 
# path_input_files = "/carrefour_bio/fichiers_générés_par_Hervé"
# dict_one_product = None
# # s = 0.75

# path_input_files = "/carrefour_bio/fichiers_générés_par_Hervé"
# url_one_product = "https://www.greenweez.com/lima-chips-aux-lentilles-original-90g-p83002"
# threshold_value = 0.75
# threshold_value = None
# method_chosen = "all_except_one"

# Case 2 :ON CHOISIT UN PRODUIT QUI MATCHE AVEC UN AUTRE:
# lima-chips-aux-lentilles-original-90g-p83002 chez gwz
# A enlever dans les fichiers :
# - orgc_gwz_product.csv
# - orgc_gwz_offer.csv


# I Enlever ce produit dans les 2 fichiers + lancer "cas 1"

# II Renseigner le dictionnaire en entrée du "cas 2" + lancer le "cas 2"

# Case 2
# path_input_files = None
# path_input_files = "/carrefour_bio/fichiers_générés_par_Hervé"

# path_input_files = "/carrefour_bio/fichiers_générés_par_Hervé"
 # url_one_product = "https://www.greenweez.com/lima-chips-aux-lentilles-original-90g-p83002"

# threshold_value = 0.75
# threshold_value = None
# method_chosen = "new_one"

# Case 3
# path_input_files = "/carrefour_bio/fichiers_générés_par_Hervé"
# url_one_product = None
# threshold_value = None
# method_chosen = "all"

# def main(path_input, dict_product, s):
# def main(path_input, url_product, threshold,  method):

# 06/05/2019: on n'utilise plus le paramètre "path_input"
# def matching_products_with_threshold(path_input, url_product, threshold,  method):
def matching_products_with_threshold(url_product, threshold, method):

    #     global orgc_descriptions, orgc_offers,orgc_descriptions_all_slugs, orgc_offers_all_slugs
    global orgc_descriptions, orgc_offers, orgc_descriptions_all_slugs, orgc_descriptions_all_slugs_except_one, orgc_offers_all_slugs_except_one

    # if path_input != None and dict_product == None:
    # 16/04/2019 : ajout cas "all"
    # if path_input != None and method == "all_except_one":

    # 26/04/2019: ajout du paramètre "all_with_filter"
    # if (path_input != None and method == "all_except_one") or (path_input != None and method == "all"):

    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # if (path_input != None and method == "all_except_one") or (path_input != None and method == "all") or (path_input != None and method == "all_with_filter"):

    # 20/05/2019 : le cas "all_except_one", ne sert plus à rien
    # if method == "all_except_one" or method == "all" or method == "all_with_filter":

    # 28/05/2019: on n'a plus besoin de "all_with_filter"
    # if method == "all" or method == "all_with_filter":
    if method == "all":

        print ("Step 1-1: Import des fichiers .csv product")

        # 06/05/2019 : définition de "path_input"
        path_input = '/carrefour_chunking_bio/fichiers_générés_par_Hervé'

        data_folder_input = path_root + path_input

        # orgc_crf_product = step_1.create_df("orgc_crf_product",data_folder_input + "/crf/","utf8")
        # orgc_crf_product['distributeur'] = 'crf'
        #
        # orgc_gwz_product = step_1.create_df("orgc_gwz_product",data_folder_input + "/gwz/","utf8")
        # orgc_gwz_product['distributeur'] = 'gwz'
        #
        # orgc_ntr_product = step_1.create_df("orgc_ntr_product",data_folder_input + "/ntr/","utf8")
        # orgc_ntr_product['distributeur'] = 'ntr'
        #
        # orgc_wbe_product = step_1.create_df("orgc_wbe_product",data_folder_input + "/wbe/","utf8")
        # orgc_wbe_product['distributeur'] = 'wbe'

        # On rassemble tous les produits bio dans un dataframe
        # frames = [orgc_crf_product, orgc_gwz_product, orgc_ntr_product, orgc_wbe_product]
        # orgc_descriptions = pd.concat(frames)
        print(data_folder_input + "/all/")

        # 10/05/2019 : on normalise les noms des fichiers en entrée
        # orgc_descriptions = step_1.create_df("orgc_all_except_5_slugs_product", data_folder_input + "/all/", "utf8")
        orgc_descriptions = step_1.create_df("orgc_all_slugs_product", data_folder_input + "/all/", "utf8")

        # 09/05/2019 : ajout de la colonne "distributeur"
        orgc_descriptions['distributeur'] = orgc_descriptions['xweb']

        # 10/04/2019 : on prend tous les produits excepté un
        # 26/04/2019 : ajout de cette condition

        # 20/05/2019 : le cas "all_except_one", ne sert plus à rien
        # if path_input != None and method == "all_except_one":
        #     orgc_descriptions = orgc_descriptions[orgc_descriptions['xurl'] != url_product]

        # del frames
        # del orgc_crf_product, orgc_gwz_product, orgc_ntr_product, orgc_wbe_product

        print ("Step 1-2: Import des fichiers .csv offer")
        
        # orgc_crf_offer = step_1.create_df("orgc_crf_offer",data_folder_input + "/crf/","utf8")
        # orgc_crf_offer['distributeur'] = 'crf'
        #
        # orgc_gwz_offer = step_1.create_df("orgc_gwz_offer",data_folder_input + "/gwz/","utf8")
        # orgc_gwz_offer['distributeur'] = 'gwz'
        #
        # orgc_ntr_offer = step_1.create_df("orgc_ntr_offer",data_folder_input + "/ntr/","utf8")
        # orgc_ntr_offer['distributeur'] = 'ntr'
        #
        # orgc_wbe_offer = step_1.create_df("orgc_wbe_offer",data_folder_input + "/wbe/","utf8")
        # orgc_wbe_offer['distributeur'] = 'wbe'

        # On rassemble tous les produits bio dans un dataframe
        # frames = [orgc_crf_offer, orgc_gwz_offer, orgc_ntr_offer, orgc_wbe_offer]
        # orgc_offers = pd.concat(frames)
        # 10/05/2019 : on normalise les noms des fichiers en entrée
        # orgc_offers = step_1.create_df("orgc_all_except_5_slugs_offer", data_folder_input + "/all/", "utf8")
        orgc_offers = step_1.create_df("orgc_all_slugs_offer", data_folder_input + "/all/", "utf8")

        # 09/05/2019 : ajout de la colonne "distributeur"
        orgc_offers['distributeur'] = orgc_offers['xweb']

        # 10/04/2019 : on prend tous les produits excepté un
        # 26/04/2019 : ajout de cette condition

        # 20/05/2019 : le cas "all_except_one", ne sert plus à rien
        # if path_input != None and method == "all_except_one":
        #     orgc_offers = orgc_offers[orgc_offers['xurl'] != url_product]

        # del frames
        # del orgc_crf_offer, orgc_gwz_offer, orgc_ntr_offer, orgc_wbe_offer

    # elif path_input != None and dict_product != None:
    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # elif path_input != None and method == "new_one":
    elif method == "new_one":

        # 06/05/2019: pour un vrai fonctionnement en Prod, on n'a plus besoin
        # de créer un dataframe "orgc_descriptions_all_slugs"

        # print("L'URL du nouveau produit est :", url_product)

        path_input = '/carrefour_chunking_bio/fichiers_générés_par_Hervé'

        data_folder_input = path_root + path_input

        # orgc_crf_product = step_1.create_df("orgc_crf_product", data_folder_input + "/crf/", "utf8")
        # orgc_crf_product['distributeur'] = 'crf'
        # orgc_gwz_product = step_1.create_df("orgc_gwz_product", data_folder_input + "/gwz/", "utf8")
        # orgc_gwz_product['distributeur'] = 'gwz'
        # orgc_ntr_product = step_1.create_df("orgc_ntr_product", data_folder_input + "/ntr/", "utf8")
        # orgc_ntr_product['distributeur'] = 'ntr'
        # orgc_wbe_product = step_1.create_df("orgc_wbe_product", data_folder_input + "/wbe/", "utf8")
        # orgc_wbe_product['distributeur'] = 'wbe'

        # On rassemble tous les produits bio dans un dataframe

        # frames = [orgc_crf_product, orgc_gwz_product, orgc_ntr_product, orgc_wbe_product]
        # orgc_descriptions_all_slugs = pd.concat(frames)

        # 06/05/2019: pour un vrai fonctionnement en Prod, on n'a plus besoin
        # de créer un dataframe "orgc_descriptions_all_slugs"

        # ATTENTION :
        #  "orgc_descriptions_all_slugs" devient "orgc_descriptions_all_slugs_except_one"

        # 09/04/2019 : on prend tous les produits excepté un

        # 06/05/2019: pour un vrai fonctionnement en Prod,
        # le dataframe "orgc_descriptions_all_slugs_except_one" est créé à partir
        # des données extraites dans la base des données crawlées, qui n'ont pas le statut "nouveaux produits"
        # la 1ère fois on pointe sur le répertoire "all"
        # Ensuite on est bloqué pour tester un ajout d'un nouveau produit
        # l'un après l'autre donc on teste une seule fois avec 5 nouveaux produits

        # orgc_descriptions_all_slugs_except_one = orgc_descriptions_all_slugs[orgc_descriptions_all_slugs['xurl'] != url_product]
        # 10/05/2019 : on normalise les noms des fichiers en entrée
        # orgc_descriptions_all_slugs_except_one = step_1.create_df("orgc_all_except_5_slugs_product", data_folder_input + "/all/", "utf8")
        orgc_descriptions_all_slugs_except_one = step_1.create_df("orgc_all_slugs_product", data_folder_input + "/all/",
                                                                  "utf8")

        # 09/05/2019 : ajout de la colonne "distributeur"
        orgc_descriptions_all_slugs_except_one['distributeur'] = orgc_descriptions_all_slugs_except_one['xweb']

        # del frames
        # del orgc_crf_product, orgc_gwz_product, orgc_ntr_product, orgc_wbe_product

        # orgc_crf_offer = step_1.create_df("orgc_crf_offer", data_folder_input + "/crf/", "utf8")
        # orgc_crf_offer['distributeur'] = 'crf'
        # orgc_gwz_offer = step_1.create_df("orgc_gwz_offer", data_folder_input + "/gwz/", "utf8")
        # orgc_gwz_offer['distributeur'] = 'gwz'
        # orgc_ntr_offer = step_1.create_df("orgc_ntr_offer", data_folder_input + "/ntr/", "utf8")
        # orgc_ntr_offer['distributeur'] = 'ntr'
        # orgc_wbe_offer = step_1.create_df("orgc_wbe_offer", data_folder_input + "/wbe/", "utf8")
        # orgc_wbe_offer['distributeur'] = 'wbe'

        # On rassemble tous les produits bio dans un dataframe

        # frames = [orgc_crf_offer, orgc_gwz_offer, orgc_ntr_offer, orgc_wbe_offer]
        # orgc_offers_all_slugs = pd.concat(frames)

        # 09/04/2019 : on prend tous les produits excepté un

        # 06/05/2019: pour un vrai fonctionnement en Prod,
        # le dataframe "orgc_offers_all_slugs_except_one" est créé à partir
        # des données extraites dans la base des données crawlées, qui n'ont pas le statut "nouveaux produits"
        # la 1ère fois on pointe sur le répertoire "all"
        # Ensuite on est bloqué pour tester un ajout d'un nouveau produit
        # l'un après l'autre donc on teste une seule fois avec 5 nouveaux produits

        # orgc_offers_all_slugs_except_one = orgc_offers_all_slugs[orgc_offers_all_slugs['xurl'] != url_product]
        # 10/05/2019 : on normalise les noms des fichiers en entrée
        # orgc_offers_all_slugs_except_one = step_1.create_df("orgc_all_except_5_slugs_offer", data_folder_input + "/all/", "utf8")
        orgc_offers_all_slugs_except_one = step_1.create_df("orgc_all_slugs_offer", data_folder_input + "/all/", "utf8")

        # 09/05/2019 : ajout de la colonne "distributeur"
        orgc_offers_all_slugs_except_one['distributeur'] = orgc_offers_all_slugs_except_one['xweb']

        # ATTENTION :
        #  "orgc_offers_all_slugs" devient "orgc_offers_all_slugs_except_one"

        # del frames
        # del orgc_crf_offer, orgc_gwz_offer, orgc_ntr_offer, orgc_wbe_offer

    #--------------------------------------------------------------------------------------------------------------------#
    #-------------- On constate que le "xtitle" il y a 16754 titres distincts -------------------------------------------#
    #---------Ici, on ne crée pas de titre plus précis, avec xbrand + xsubtitle -----------------------------------------#
    #-------- Remarques : -----------------------------------------------------------------------------------------------#
    #-------- xbrand va etre utilisé pour matcher à la fin de ce process afin d'identifier les produits de memes marques-#
    #-------- le "xsubtitle" est trop détaillé pour GREENWEEZ ! ---------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#
    #---------------------------------------------- step_1_data_cleansing -----------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#

    #--------------------------------------------------------------------------------------------------------------------#
    #------------------- Ne concerne que les titres ---------------------------------------------------------------------#
    #------------------- Pour le BIO, on se demande quels caractères spéciaux sont présents dans les titres ? -----------#
    #--------------------------------------------------------------------------------------------------------------------#

    #---------------------------------------------------------------------------------------------------------------------------#
    #----------- CONCLUSION pour nettoyer les titres : -------------------------------------------------------------------------#
    #------------pourquoi le '"' est remplacé par le '' pour le vin ? ----------------------------------------------------------#
    #---car pour le BIO, il est intéressant de garder ces " ", qui permettent de splitter les titres afin d'extraire une entité -#
    #---On va essayer de splitter les titres avec : les mots à l'intérieur des '"' les mots séparés par ' - ' ou ' : ' ---------#
    #---les mots en majuscule Ensuite il faudra chercher les entités grace au Chunking dans les parties splittées. -------------#
    #---------------------------------------------------------------------------------------------------------------------------#

    #******************************************************************#
    #******** A cette étape:  "bio" est enlevé des stopwords **********#
    #******************************************************************#

    #---------------------------------------------------------------------------------------------------------------------------#
    #--- 1. Création de la colonne "titre sans stopwords" grace à : <br>--------------------------------------------------------#
    #--- Nettoyage des titres bruts : ------------------------------------------------------------------------------------------#
    #--- - suppression des pattern  " ' " et "''" ------------------------------------------------------------------------------#
    #--- - suppression des blancs inutiles de manière à ne garder qu'un seul blanc du type ' ' entre les mots ------------------#
    #--- - suppression des parenthèses "(" et ")" ------------------------------------------------------------------------------#
    #--- - suppression des accents ---------------------------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------------------------------------------------#
    #---  Suppression des stopwords: on essaye en mettant 'bio' ----------------------------------------------------------------#
    #---------------------------------------------------------------------------------------------------------------------------#
    #--- 2. Extraction des entités en majuscules grace aux titres sans stopwords -----------------------------------------------#
    #---------------------------------------------------------------------------------------------------------------------------# 
    #--- 3. Extraction des entités comprises entre guillements grace aux titres sans stopwords----------------------------------#
    #---------------------------------------------------------------------------------------------------------------------------#

    print("Step 2: Nettoyage, suppression des stopwords, split des mots en majuscules et split des mots entre guillemets dans les titres")

    # Si on traite la cas 2, la dataframe "orgc_descriptions" contient un seul produit
    # On suppose aussi que le dictionnaire contient le prix
    # if path_input != None and dict_product != None:

    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # if path_input != None and method == "new_one":
    if method == "new_one":

        # 06/05/2019 : pour se rapprocher du vrai fonctionnement en Prod
        # on pointe sur les données du répertoire "new_one"

        # orgc_descriptions = orgc_descriptions_all_slugs[orgc_descriptions_all_slugs['xurl'] == url_product]
        # 10/05/2019 : on normalise les noms des fichiers en entrée
        # orgc_descriptions = step_1.create_df("orgc_sampled_3_slugs_product", data_folder_input + "/new_one/", "utf8")
        orgc_descriptions = step_1.create_df("orgc_new_one_slugs_product", data_folder_input + "/new_one/", "utf8")

        # 09/05/2019 : ajout de la colonne "distributeur"
        orgc_descriptions['distributeur'] = orgc_descriptions['xweb']

    orgc_descriptions["title_new"] = orgc_descriptions['xtitle'].map(step_2.cleansing_titles)

    # Suppression des stopwords
    orgc_descriptions["title_without_stopwords"] = orgc_descriptions['title_new'].map(step_2.remove_stopwords)

    # Ajouter un split en mettant de coté les mots en MAJUSCULES
    orgc_descriptions["title_splitted_uppercase"] = orgc_descriptions["title_without_stopwords"].map(step_2.split_words_uppercase)
    # Ajouter un split en mettant de coté les mots compris entre deux guillemets
    orgc_descriptions["title_splitted_guillemets"] = orgc_descriptions["title_without_stopwords"].map(step_2.split_words_guillemets)

    # ---------------------------------------------------------------------------------------------------------------------------#
    # ------- Création d'une colonne des titres splittés par les séparateurs : {' , ';' : ',' - '} ------------------------------#
    # ------- Y-a-t-il d'autres séparateurs possibles ? -------------------------------------------------------------------------#
    # ---------------------------------------------------------------------------------------------------------------------------#

    orgc_descriptions["title_splitted"] = orgc_descriptions["title_without_stopwords"].map(step_2.split_title)

    # 26/03/2019 : ajout breadcrumb niveau le plus fin
    # if path_input_files != None and dict_one_product == None:
    #     orgc_descriptions["breadcrumb"] = orgc_descriptions["xbreadcrumb"].map(lambda x: x.split('>')[-1].strip())
    # # 02/04/2019 : ajout des prix des produits
    #     orgc_descriptions = pd.merge(orgc_descriptions, orgc_offers[['xslug','xprice']], on = "xslug", how = "inner")

    orgc_descriptions["breadcrumb"] = orgc_descriptions["xbreadcrumb"].map(lambda x: x.split('>')[-1].strip())

    # 02/04/2019 : ajout des prix des produits
    # if path_input != None and dict_product == None:
    # 16/04/2019 : ajout du cas "all"
    # if path_input != None and method == "all_except_one":

    # 26/04/2019: ajout du paramètre "all_with_filter"
    # if (path_input != None and method == "all_except_one") or (path_input != None and method == "all"):
    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # if (path_input != None and method == "all_except_one") or (path_input != None and method == "all") or (path_input != None and method == "all_with_filter"):

    # 20/05/2019 : le cas "all_except_one", ne sert plus à rien
    # if method == "all_except_one" or method == "all" or method == "all_with_filter":

    # 28/05/2019 : on n'a pas besoin de "all_with_filter" car on peut maintenant utiliser "all" à la place
    # if method == "all" or method == "all_with_filter":
    # if method == "all" or method == "all_with_filter":
    if method == "all":
        orgc_descriptions = pd.merge(orgc_descriptions, orgc_offers[['xslug', 'xprice']], on="xslug", how="inner")

    # ---------------------------------------------------------------------------------------------------------------------------#
    # ----- NB: Pour le "cas 2", on ne va pas avoir besoin de "orgc_descriptions_all_slugs" -----------------------------------------#
    # ---------------------------------------------------------------------------------------------------------------------------#

    # if path_input != None and dict_product != None:
    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # if path_input != None and method == "new_one":
    if method == "new_one":
        # orgc_descriptions_all_slugs["title_new"] = orgc_descriptions_all_slugs['xtitle'].map(step_2.cleansing_titles)
        orgc_descriptions_all_slugs_except_one["title_new"] = orgc_descriptions_all_slugs_except_one['xtitle'].map(step_2.cleansing_titles)

        # Suppression des stopwords
        #     orgc_descriptions_all_slugs["title_without_stopwords"] = orgc_descriptions_all_slugs['title_new'].map(step_2.remove_stopwords)
        orgc_descriptions_all_slugs_except_one["title_without_stopwords"] = orgc_descriptions_all_slugs_except_one['title_new'].map(step_2.remove_stopwords)

        # Ajouter un split en mettant de coté les mots en MAJUSCULES
        #     orgc_descriptions_all_slugs["title_splitted_uppercase"] = orgc_descriptions_all_slugs["title_without_stopwords"].map(step_2.split_words_uppercase)
        orgc_descriptions_all_slugs_except_one["title_splitted_uppercase"] = orgc_descriptions_all_slugs_except_one["title_without_stopwords"].map(step_2.split_words_uppercase)
        # Ajouter un split en mettant de coté les mots compris entre deux guillemets
        #     orgc_descriptions_all_slugs["title_splitted_guillemets"] = orgc_descriptions_all_slugs["title_without_stopwords"].map(step_2.split_words_guillemets)
        orgc_descriptions_all_slugs_except_one["title_splitted_guillemets"] = orgc_descriptions_all_slugs_except_one["title_without_stopwords"].map(step_2.split_words_guillemets)

        # ---------------------------------------------------------------------------------------------------------------------------#
        # ------- Création d'une colonne des titres splittés par les séparateurs : {' , ';' : ',' - '} ------------------------------#
        # ------- Y-a-t-il d'autres séparateurs possibles ? -------------------------------------------------------------------------#
        # ---------------------------------------------------------------------------------------------------------------------------#

        #     orgc_descriptions_all_slugs["title_splitted"] = orgc_descriptions_all_slugs["title_without_stopwords"].map(step_2.split_title)
        orgc_descriptions_all_slugs_except_one["title_splitted"] = orgc_descriptions_all_slugs_except_one["title_without_stopwords"].map(step_2.split_title)

        # 26/03/2019 : ajout breadcrumb niveau le plus fin
        # if path_input_files != None and dict_one_product == None:
        #     orgc_descriptions_all_slugs["breadcrumb"] = orgc_descriptions_all_slugs["xbreadcrumb"].map(lambda x: x.split('>')[-1].strip())
        # # 02/04/2019 : ajout des prix des produits
        #     orgc_descriptions_all_slugs["breadcrumb"] = orgc_descriptions_all_slugs["xbreadcrumb"].map(lambda x: x.split('>')[-1].strip())
        orgc_descriptions_all_slugs_except_one["breadcrumb"] = orgc_descriptions_all_slugs_except_one["xbreadcrumb"].map(lambda x: x.split('>')[-1].strip())

        # ajout des prix des produits
        #     orgc_descriptions_all_slugs = pd.merge(orgc_descriptions_all_slugs, orgc_offers_all_slugs[['xslug','xprice']], on = "xslug", how = "inner")
        orgc_descriptions_all_slugs_except_one = pd.merge(orgc_descriptions_all_slugs_except_one, orgc_offers_all_slugs_except_one[['xslug', 'xprice']], on="xslug", how="inner")

    # 03/04/2019: "cas 1"
    # if path_input != None and dict_product == None:
    #     print("path_root", path_root)
    #     print("path_output", path_output)
    #     orgc_descriptions.to_pickle(path_root + path_output + '/orgc_descriptions_case_1.pkl')
    # # 03/04/2019: "cas 2", on crée le dataframe grace au .pkl de "orgc_descriptions" créé lors du "cas 1"
    # elif path_input == None and dict_product != None:
    #     orgc_descriptions_case_1 = pd.read_pickle(path_root + path_output + '/orgc_descriptions_case_1.pkl')
    #     # ATTENTION : et on ajoute le nouveau produit dans "orgc_descriptions"
    #     orgc_descriptions = pd.concat(orgc_descriptions, orgc_descriptions_case_1)
    
    #---------------------------------------------------------------------------------------------------------------------------#
    #--- Création du dataframe "title_et_ngrams" -------------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------------------------------------------------#
    #--- * on utilise les slugs(appelés "xslug"), les noms de ditributeurs, les titres sans stopwords et les descriptions ------#
    #--- * on nettoie un peu plus les titres sans stopwords en enlevant les blancs ---------------------------------------------#
    #---   qui peuvent etre autour des titres et en mettant en minuscules ------------------------------------------------------#
    #--- * on renomme la colonne "xslug" en "slug" -----------------------------------------------------------------------------#
    #--- * on enlève dans les titres sans stopwords les séparateurs du type virgule "," et deux-points ":" ---------------------#
    #---   On garde les tirets "-" (cf mots composés avec des "-") -------------------------------------------------------------#
    #--- * On remplace dans les titres sans stopwords, les séparateurs du type ' - ' par un espace du type ' ' -----------------#
    #---------------------------------------------------------------------------------------------------------------------------#

    # title_et_ngrams = orgc_descriptions[['xtitle','xbrand','xbreadcrumb','xsubtitle','xdescription']]
    # Ou 
    title_et_ngrams = orgc_descriptions[['xslug','distributeur','title_without_stopwords','xdescription']]

    # On met en minuscules la colonne ''title_without_stopwords'
    title_et_ngrams["title_temp"] = title_et_ngrams['title_without_stopwords'].map(lambda x: (x.strip()).lower())
    title_et_ngrams = title_et_ngrams.drop("title_without_stopwords", axis =1)
    title_et_ngrams.rename(columns={'title_temp': 'title_without_stopwords'}, inplace=True)

    title_et_ngrams.rename(columns={'xslug': 'slug'}, inplace=True)

    # Suppression de séparateurs présents dans les titres de type : '\s*[,:]\s*' 
    title_et_ngrams['title_temp'] = title_et_ngrams['title_without_stopwords'].map(step_2.remove_separateurs)

    title_et_ngrams['title_without_stopwords_new'] = title_et_ngrams['title_temp'].str.replace(' - ',' ')
    title_et_ngrams = title_et_ngrams.drop("title_temp", axis =1)


    #--------------------------------------------------------------------------------------------------------------------#
    #--- Ne concerne que les titres -------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#
    #--- Ajout de nouvelles colonnes dans le dataframe "title_et_ngrams" ------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#
    #--- * création à partir des titres sans stopwords, de la colonne des titres sans le pattern "année" du type AAAA -------#
    #--- * on enlève dans les titres sans stopwords et sans année les séparateurs du type virgule "," et deux-points ":" ----#
    #--- On garde les tirets "-" (cf mots composés avec des "-") --------------------------------------------------------#
    #--- * On remplace dans les titres sans stopwords et sans année, les séparateurs du type ' - ' par un espace du type ' ' -----#
    #--- * on extrait la liste des mots qui composent les titres sans stopwords et sans année ------------------------------------#
    #--- * on nettoie la liste des mots qui composent les titres sans stopwords et sans année ---------------------------#
    #--- en enlevant les blancs qui peuvent etre autour des mots, en mettant en minuscules ----------------------------#
    #--- et en enlevant au début des mots, le pattern du type "' " ------------------------------------------------#
    #--- et en enlevant à la fin des mots, le pattern du type " '" ------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------#

    # Suppression de l'année dans les titres
    title_et_ngrams["title_without_year"] = title_et_ngrams['title_without_stopwords'].map(step_2.remove_year)

    title_et_ngrams['title_temp'] = title_et_ngrams['title_without_year'].map(step_2.remove_separateurs)

    title_et_ngrams['title_without_year_for_words_title'] = title_et_ngrams['title_temp'].str.replace(' - ',' ')

    title_et_ngrams = title_et_ngrams.drop("title_temp", axis =1)

     # 10/11/2018 : problème avec les "d'", extrait : "d'" et "''"
    # title_et_ngrams['words_title'] = title_et_ngrams['title_without_year_for_words_title'].map(step_2.word_tokenize)
    title_et_ngrams['words_title'] = title_et_ngrams['title_without_year_for_words_title'].map(lambda x: x.split(' '))

    # Sert surtout pour enlever les "' " qui peuvent être présents
    title_et_ngrams['words_title_cleansed'] =  title_et_ngrams['words_title'].map(step_2.cleansing_words_after_split)

    #---------------------------------------------------------------------------------------------------------------------#
    #--- Créer aussi dans le "cas 2": "title_et_ngrams_all_slugs" grace à "orgc_descriptions_all_slugs" ------------------#
    #---------------------------------------------------------------------------------------------------------------------#

    # if path_input != None and dict_product != None:
    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # if path_input != None and method == "new_one":
    if method == "new_one":
        # 09/04/2019 : ATTENTION : remplacement de
        # - "title_et_ngrams_all_slugs" par "title_et_ngrams_all_slugs_except_one"
        # - "orgc_descriptions_all_slugs" par "orgc_descriptions_all_slugs_except_one"

        #     title_et_ngrams_all_slugs = orgc_descriptions_all_slugs[['xslug','distributeur','title_without_stopwords','xdescription']]
        title_et_ngrams_all_slugs_except_one = orgc_descriptions_all_slugs_except_one[['xslug', 'distributeur', 'title_without_stopwords', 'xdescription']]

        # On met en minuscules la colonne ''title_without_stopwords'
        title_et_ngrams_all_slugs_except_one["title_temp"] = title_et_ngrams_all_slugs_except_one['title_without_stopwords'].map(lambda x: (x.strip()).lower())
        title_et_ngrams_all_slugs_except_one = title_et_ngrams_all_slugs_except_one.drop("title_without_stopwords", axis=1)
        title_et_ngrams_all_slugs_except_one.rename(columns={'title_temp': 'title_without_stopwords'}, inplace=True)

        title_et_ngrams_all_slugs_except_one.rename(columns={'xslug': 'slug'}, inplace=True)

        # Suppression de séparateurs présents dans les titres de type : '\s*[,:]\s*'
        title_et_ngrams_all_slugs_except_one['title_temp'] = title_et_ngrams_all_slugs_except_one['title_without_stopwords'].map(step_2.remove_separateurs)

        title_et_ngrams_all_slugs_except_one['title_without_stopwords_new'] = title_et_ngrams_all_slugs_except_one['title_temp'].str.replace(' - ', ' ')
        title_et_ngrams_all_slugs_except_one = title_et_ngrams_all_slugs_except_one.drop("title_temp", axis=1)

        # --------------------------------------------------------------------------------------------------------------------#
        # --- Ne concerne que les titres -------------------------------------------------------------------------------------#
        # --------------------------------------------------------------------------------------------------------------------#
        # --- Ajout de nouvelles colonnes dans le dataframe "title_et_ngrams_all_slugs" ------------------------------------------------#
        # --------------------------------------------------------------------------------------------------------------------#
        # --- * création à partir des titres sans stopwords, de la colonne des titres sans le pattern "année" du type AAAA -------#
        # --- * on enlève dans les titres sans stopwords et sans année les séparateurs du type virgule "," et deux-points ":" ----#
        # --- On garde les tirets "-" (cf mots composés avec des "-") --------------------------------------------------------#
        # --- * On remplace dans les titres sans stopwords et sans année, les séparateurs du type ' - ' par un espace du type ' ' -----#
        # --- * on extrait la liste des mots qui composent les titres sans stopwords et sans année ------------------------------------#
        # --- * on nettoie la liste des mots qui composent les titres sans stopwords et sans année ---------------------------#
        # --- en enlevant les blancs qui peuvent etre autour des mots, en mettant en minuscules ----------------------------#
        # --- et en enlevant au début des mots, le pattern du type "' " ------------------------------------------------#
        # --- et en enlevant à la fin des mots, le pattern du type " '" ------------------------------------------------#
        # --------------------------------------------------------------------------------------------------------------#

        # Suppression de l'année dans les titres
        title_et_ngrams_all_slugs_except_one["title_without_year"] = title_et_ngrams_all_slugs_except_one['title_without_stopwords'].map(step_2.remove_year)

        title_et_ngrams_all_slugs_except_one['title_temp'] = title_et_ngrams_all_slugs_except_one['title_without_year'].map(step_2.remove_separateurs)

        title_et_ngrams_all_slugs_except_one['title_without_year_for_words_title'] = \
        title_et_ngrams_all_slugs_except_one['title_temp'].str.replace(' - ', ' ')

        title_et_ngrams_all_slugs_except_one = title_et_ngrams_all_slugs_except_one.drop("title_temp", axis=1)

        # 10/11/2018 : problème avec les "d'", extrait : "d'" et "''"
        # title_et_ngrams_all_slugs['words_title'] = title_et_ngrams_all_slugs['title_without_year_for_words_title'].map(step_2.word_tokenize)
        title_et_ngrams_all_slugs_except_one['words_title'] = title_et_ngrams_all_slugs_except_one['title_without_year_for_words_title'].map(lambda x: x.split(' '))

        # Sert surtout pour enlever les "' " qui peuvent être présents
        title_et_ngrams_all_slugs_except_one['words_title_cleansed'] = title_et_ngrams_all_slugs_except_one['words_title'].map(step_2.cleansing_words_after_split)

    #--------------------------------------------------------------------------------------------------------------------#
    #--- Création des dictionnaires de 1-grams, 2-grams, 4-grams et 5-grams ---------------------------------------------#
    #--- grâce à la colonne 'words_title_cleansed' du dataframe "title_et_ngrams" ---------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#
    #--- Ces dictionnaires ont leurs : ----------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#
    #--- * clés égales aux n-grams présents dans les titres des produits ------------------------------------------------#
    #--- * valeurs égales au nombre de fois qu'un n-gram est présent dans tous les titres des produits ------------------#
    #--------------------------------------------------------------------------------------------------------------------#

    print ("Step 3: Extraction des ngrams dans les titres")

    print("\n On traite le dictionnaire des 1-grams !")

    dict_all_1_grams = dict()

    # 16/02/2018 : on utilise "words_title_cleansed" à la place de "words_title"

    for row in title_et_ngrams.itertuples():
        flag_update_dict = False
        
    #     ngram_presents = row.words_title
        ngram_presents = row.words_title_cleansed   
        
        for i in range(len(ngram_presents)):
              
            if ngram_presents[i] not in dict_all_1_grams :
                dict_all_1_grams[ngram_presents[i]] = 0
                
                if ngram_presents[i] in row.title_without_year_for_words_title:
                    dict_all_1_grams[ngram_presents[i]] = 1
                    flag_update_dict = True

            # Si on traite un nouveau "title" de vin
            # et que le ngram en question est déjà dans le dico,
            # On peut incrémenter le compteur 
            if ngram_presents[i] in dict_all_1_grams and flag_update_dict == False:
                if ngram_presents[i] in row.title_without_year_for_words_title:
                     dict_all_1_grams[ngram_presents[i]] = dict_all_1_grams[ngram_presents[i]] + 1

    print("\n On traite le dictionnaire des 2-grams !")
    dict_all_2_grams = dict()

    for row in title_et_ngrams.itertuples():
        flag_update_dict = False
        
    #     if find_ngrams(row.words_title,2) != []:
    #         ngram_presents = find_ngrams(row.words_title,2)
        if step_3.find_ngrams(row.words_title_cleansed,2) != []:
            ngram_presents = step_3.find_ngrams(row.words_title_cleansed,2)
            
        for i in range(len(ngram_presents)):
              
            if ngram_presents[i] not in dict_all_2_grams :
                dict_all_2_grams[ngram_presents[i]] = 0 
                
                if ngram_presents[i] in row.title_without_year_for_words_title:
                    dict_all_2_grams[ngram_presents[i]] = 1
                    flag_update_dict = True

            # Si on traite un nouveau "title" de vin
            # et que le ngram en question est déjà dans le dico,
            # On peut incrémenter le compteur 
            if ngram_presents[i] in dict_all_2_grams and flag_update_dict == False:
                if ngram_presents[i] in row.title_without_year_for_words_title:
                     dict_all_2_grams[ngram_presents[i]] = dict_all_2_grams[ngram_presents[i]] + 1


    print("\n On traite le dictionnaire des 3-grams !")
    dict_all_3_grams = dict()

    for row in title_et_ngrams.itertuples(): 
        flag_update_dict = False
        
    #     if find_ngrams(row.words_title,3) != []:
    #         ngram_presents = find_ngrams(row.words_title,3)
        if step_3.find_ngrams(row.words_title_cleansed,3) != []:
            ngram_presents = step_3.find_ngrams(row.words_title_cleansed,3)

        for i in range(len(ngram_presents)):
              
            if ngram_presents[i] not in dict_all_3_grams :
                dict_all_3_grams[ngram_presents[i]] = 0 
                
                if ngram_presents[i] in row.title_without_year_for_words_title:
                    dict_all_3_grams[ngram_presents[i]] = 1
                    flag_update_dict = True

            # Si on traite un nouveau "title" de vin
            # et que le ngram en question est déjà dans le dico,
            # On peut incrémenter le compteur 
            if ngram_presents[i] in dict_all_3_grams and flag_update_dict == False:
                if ngram_presents[i] in row.title_without_year_for_words_title:
                     dict_all_3_grams[ngram_presents[i]] = dict_all_3_grams[ngram_presents[i]] + 1

    print("\n On traite le dictionnaire des 4-grams !")                
    dict_all_4_grams = dict()

    for row in title_et_ngrams.itertuples():
        flag_update_dict = False
        
        
    #     if find_ngrams(row.words_title,4) != []:
    #         ngram_presents = find_ngrams(row.words_title,4)
        if step_3.find_ngrams(row.words_title_cleansed,4) != []:
            ngram_presents = step_3.find_ngrams(row.words_title_cleansed,4)

        for i in range(len(ngram_presents)):
              
            if ngram_presents[i] not in dict_all_4_grams :
                dict_all_4_grams[ngram_presents[i]] = 0 
                
                if ngram_presents[i] in row.title_without_year_for_words_title:
                    dict_all_4_grams[ngram_presents[i]] = 1
                    flag_update_dict = True

            # Si on traite un nouveau "title" de vin
            # et que le ngram en question est déjà dans le dico,
            # On peut incrémenter le compteur 
            if ngram_presents[i] in dict_all_4_grams and flag_update_dict == False:
                if ngram_presents[i] in row.title_without_year_for_words_title:
                     dict_all_4_grams[ngram_presents[i]] = dict_all_4_grams[ngram_presents[i]] + 1

    # ON NE SERT PAS DE "dict_all_5_grams"
    #
    # print("\n On traite le dictionnaire des 5-grams !")
    # dict_all_5_grams = dict()
    #
    # for row in title_et_ngrams.itertuples():
    #     flag_update_dict = False
    #
    # #     if find_ngrams(row.words_title,5) != []:
    # #         ngram_presents = find_ngrams(row.words_title,5)
    #     if step_3.find_ngrams(row.words_title_cleansed,5) != []:
    #         ngram_presents = step_3.find_ngrams(row.words_title_cleansed,5)
    #
    #
    #     for i in range(len(ngram_presents)):
    #
    #         if ngram_presents[i] not in dict_all_5_grams :
    #             dict_all_5_grams[ngram_presents[i]] = 0
    #
    #             if ngram_presents[i] in row.title_without_year_for_words_title:
    #                 dict_all_5_grams[ngram_presents[i]] = 1
    #                 flag_update_dict = True
    #
    #         # Si on traite un nouveau "title" de vin
    #         # et que le ngram en question est déjà dans le dico,
    #         # On peut incrémenter le compteur
    #         if ngram_presents[i] in dict_all_5_grams and flag_update_dict == False:
    #             if ngram_presents[i] in row.title_without_year_for_words_title:
    #                  dict_all_5_grams[ngram_presents[i]] = dict_all_5_grams[ngram_presents[i]] + 1

    del ngram_presents, row, i

    #--------------------------------------------------------------------------------------------------------------------#
    #--- Nouvelle étape : création de nouveaux dictionnaires avec seulement clés ayant des comptages > 1 ----------------#
    #--- Cela veut dire qu'on va s'intéresser que aux n-grams qui sont présents dans au moins 2 produits ----------------#
    #--------------------------------------------------------------------------------------------------------------------#

    # 29/03/2019: on enlève la contrainte fréquence stritement supérieure à 1
    # lors de cette extraction des n-grams présents dans les titres
    # en vue de faire fonctionner le cas 2 lorsque un nouveau produit arrive
    # dict_all_1_grams_to_update = dict()
    # for key in dict_all_1_grams.keys():
    #     if dict_all_1_grams[key] > 1: 
    #         dict_all_1_grams_to_update[key] = dict_all_1_grams[key] 

    # dict_all_2_grams_to_update = dict()
    # for key in dict_all_2_grams.keys():
    #     if dict_all_2_grams[key] > 1: 
    #         dict_all_2_grams_to_update[key] = dict_all_2_grams[key] 
            
    # dict_all_3_grams_to_update = dict()
    # for key in dict_all_3_grams.keys():
    #     if dict_all_3_grams[key] > 1: 
    #         dict_all_3_grams_to_update[key] = dict_all_3_grams[key] 

    # dict_all_4_grams_to_update = dict()
    # for key in dict_all_4_grams.keys():
    #     if dict_all_4_grams[key] > 1: 
    #         dict_all_4_grams_to_update[key] = dict_all_4_grams[key] 

    # dict_all_5_grams_to_update = dict()
    # for key in dict_all_5_grams.keys():
    #     if dict_all_5_grams[key] > 1: 
    #         dict_all_5_grams_to_update[key] = dict_all_5_grams[key] 

    # df_all_1_grams = pd.DataFrame(sorted(dict_all_1_grams_to_update.items(),key = operator.itemgetter(1),reverse = True),columns = ['un_grams','fréquence'])
    # df_all_2_grams = pd.DataFrame(sorted(dict_all_2_grams_to_update.items(),key = operator.itemgetter(1),reverse = True),columns = ['deux_grams','frequence'])
    # df_all_3_grams = pd.DataFrame(sorted(dict_all_3_grams_to_update.items(),key = operator.itemgetter(1),reverse = True),columns = ['trois_grams','frequence'])
    # df_all_4_grams = pd.DataFrame(sorted(dict_all_4_grams_to_update.items(),key = operator.itemgetter(1),reverse = True),columns = ['quatre_grams','frequence'])

    df_all_1_grams = pd.DataFrame(sorted(dict_all_1_grams.items(),key = operator.itemgetter(1),reverse = True),columns = ['un_grams','fréquence'])
    df_all_2_grams = pd.DataFrame(sorted(dict_all_2_grams.items(),key = operator.itemgetter(1),reverse = True),columns = ['deux_grams','frequence'])
    df_all_3_grams = pd.DataFrame(sorted(dict_all_3_grams.items(),key = operator.itemgetter(1),reverse = True),columns = ['trois_grams','frequence'])
    df_all_4_grams = pd.DataFrame(sorted(dict_all_4_grams.items(),key = operator.itemgetter(1),reverse = True),columns = ['quatre_grams','frequence'])

    #--------------------------------------------------------------------------------------------------------------------#
    #--- REMARQUE: ------------------------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#
    #--- si on extrait tous les n-grams des titres bruts ----------------------------------------------------------------#
    #--- qu'on sélectionne que les n-grams contenant les séparateurs du type ' : ', ' - ' -------------------------------#
    #--- Puis qu'on les nettoie, on obtient des faux n-grams ------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#
    #--- On peut alors à partir des n-grams déjà extraits grace à l'étape "........" ------------------------------------#
    #--- une liste de n-grams plus propre. ------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#

    #--------------------------------------------------------------------------------------------------------------------#
    #--- step_2_extract_xphrases_using_pattern --------------------------------------------------------------------------#
    #--- Ne concerne que les descriptions -------------------------------------------------------------------------------#
    ##-------------------------------------------------------------------------------------------------------------------#
    #--- Création du dataframe "df_descriptions_all_retailers" qui ne contient que les descriptions des produits --------#
    #--------------------------------------------------------------------------------------------------------------------#

    df_descriptions_all_retailers = title_et_ngrams[['xdescription']]

    #--------------------------------------------------------------------------------------------------------------------#
    #--- Grace à la fonction "parsetree" du package Pattern, extraction de : --------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#
    #--- * de la liste de tous les couples "tag" x "entité" présents dans toutes les descriptions des produits ----------#
    #--- * de la liste de toutes les entités présentes dans toutes les descriptions des produits ------------------------#
    #--------------------------------------------------------------------------------------------------------------------#

    print("Step 4: Extraction des chunks dans les descriptions")

    X_phrases_descriptions = []
    liste_entities_already_extracted = []

    for each_text in list(df_descriptions_all_retailers['xdescription']):
        if each_text != "" and each_text != '#':
            #         print ("texte vide ! avec:", each_text)
            couples_tag_entity = step_4.X_phrases_extraction(each_text)
            #         print (couple_tag_entity)
            if couples_tag_entity != []:
                #             print (couple_tag_entity)
                for each in couples_tag_entity:
                    #                 if each not in X_phrases_descriptions:
                    X_phrases_descriptions.append(each)
                    #                 if each[1] not in liste_entities_already_extracted:
                    liste_entities_already_extracted.append(each[1])


    #--------------------------------------------------------------------------------------------------------------------#
    #--- On dédoublonne la liste de tous les couples "tag" x "entité" présents dans toutes les descriptions des produits-#
    #--------------------------------------------------------------------------------------------------------------------#

    # ATTENTION: "nodup_X_phrases_descriptions" ne sert pas
    # C'est juste une liste qui sert pour l'exploration : elle contient le TAG x chunk
    
    k = X_phrases_descriptions
    k.sort()
    nodup_X_phrases_descriptions = list(k for k,_ in itertools.groupby(k))

    #--------------------------------------------------------------------------------------------------------------------#
    #-- On dédoublonne la liste de toutes les entités présentes dans toutes les descriptions des produits ---------------#
    #--------------------------------------------------------------------------------------------------------------------#

    
    k = liste_entities_already_extracted
    k.sort()
    nodup_entities_already_extracted = list(k for k,_ in itertools.groupby(k))

    # ['ADJP', '%,bière blonde']
    # ['ADJP', '&']
    # ['ADJP', '& légumineuses']
    # ['ADJP', ',']
    # ['ADJP', ', active']
    # ['ADJP', ', apéritives et toniques']
    # ['ADJP', ', artisanale']
    # ['ADJP', ', bienfaisantes']
    # ['ADJP', ', biologique']
    # ['ADJP', ', biologiques']
    # ['ADJP', ', blanc']
    # ['ADJP', ', blanche']
    # ['ADJP', ', brut'] ...

    #--------------------------------------------------------------------------------------------------------------------#
    #-- Ci-dessus: illustre bien que si on enlève les stopwords ---------------------------------------------------------#
    #-- On trouve en sortie les entités ---------------------------------------------------------------------------------#
    # -------------------------------------------------------------------------------------------------------------------#

    # --------------------------------------------------------------------------------------------------------------------#
    # -- STOCKER lors de l'exécution du "cas 1": "nodup_entities_already_extracted" --------------------------------------#
    # -- Dans le cas 2 : on a l'extraction des chunks que pour la description du nouveau produit -------------------------#
    # -- Et on met à jour : "nodup_entities_already_extracted" -----------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------#

    ##### Avant d'appliquer : nettoyer la liste dedup_X_phrases_titles avec cleansin_titles + remove stopwords

    # PARTIE TRES COUTEUSE SEULEMENT DANS LE CAS 1
    # for each in nodup_entities_already_extracted:
    #     dedup_X_phrases_descriptions_to_use.append(step_2.remove_stopwords(step_2.cleansing_titles(each)))
    # car pouvait sortir : 'canne','canne','canne','canne'

    # A remplacer par:
    dedup_X_phrases_descriptions_to_use = []

    for each in nodup_entities_already_extracted:
        cleansed_each = step_2.remove_stopwords(step_2.cleansing_titles(each))
        if cleansed_each not in dedup_X_phrases_descriptions_to_use:
            dedup_X_phrases_descriptions_to_use.append(cleansed_each)

    # Cas 1: on lance pour tous les produits

    # Cas 2 : on peut obtenir pour le nouveau produit:
    # - liste_X_phrases_found_in_1_grams_descriptions
    # - liste_X_phrases_found_in_2_grams_descriptions
    # - liste_X_phrases_found_in_3_grams_descriptions
    # - liste_X_phrases_found_in_4_grams_descriptions
    # en se restreignant aux n-grams qui sont contenus dans le titre du nouveau produit:
    #     = lancer la partie ci-dessous avec :
    # - df_all_1_grams
    # - df_all_2_grams
    # - df_all_3_grams
    # - df_all_4_grams
    # relatifs au nouveau produit
    # et avec "nodup_entities_already_extracted" qui concerne tous les produits (avec le nouveau produit)

    # Si on exécute le "cas 1" on crée un .pkl
    # qui va pouvoir etre mis à jour lors du "cas 2"
    # if path_input != None and dict_product == None:
    # 16/04/2019 : ajout cas "all"
    # if path_input != None and method == "all_except_one":

    # 26/04/2019: ajout du paramètre "all_with_filter"
    # if (path_input != None and method == "all_except_one") or (path_input != None and method == "all"):
    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # if (path_input != None and method == "all_except_one") or (path_input != None and method == "all") or (path_input != None and method == "all_with_filter"):

    # 20/05/2019 : le cas "all_except_one", ne sert plus à rien
    # if method == "all_except_one" or method == "all" or method == "all_with_filter":

    # 28/05/2019 : on n'a pas besoin de "all_with_filter" car on peut maintenant utiliser "all" à la place
    # if method == "all" or method == "all_with_filter":
    if method == "all":

        df_chunks_in_descriptions = pd.DataFrame(dedup_X_phrases_descriptions_to_use, columns=['chunk'])
        df_chunks_in_descriptions.to_pickle(path_root + path_output + "/to_update_pkl/df_chunks_in_descriptions.pkl")

    # Si on exécute le "cas 2" on met à jour le dataframe "df_chunks_in_descriptions"
    # elif path_input != None and dict_product != None:
    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # elif path_input != None and method == "new_one":
    elif method == "new_one":
        df_chunks_in_descriptions = pd.read_pickle(path_root + path_output + "/to_update_pkl/df_chunks_in_descriptions.pkl")

        #  Ajout des nouveaux chunks trouvés dans la description du nouveau produit
        df_chunks_in_description_new_product = pd.DataFrame(dedup_X_phrases_descriptions_to_use, columns=['chunk'])
        del dedup_X_phrases_descriptions_to_use
        chunks_temp = list(df_chunks_in_descriptions['chunk']) + list(df_chunks_in_description_new_product['chunk'])
        dedup_X_phrases_descriptions_to_use = list(set(chunks_temp))

        # 07/05/2019 : ajout de la sauvegarde de tous les chunks
        # présents dans toutes les descriptions après chaque exéxution en mode "DELTA"
        df_chunks_in_descriptions = pd.DataFrame(dedup_X_phrases_descriptions_to_use, columns=['chunk'])
        df_chunks_in_descriptions.to_pickle(path_root + path_output + "/to_update_pkl/df_chunks_in_descriptions.pkl")

    # --------------------------------------------------------------------------------------------------------------------#
    # --  On récupère toutes les entités présentes dans toutes les descriptions des produits -----------------------------#
    # -- dans une liste, sans leurs TAGS ---------------------------------------------------------------------------------#
    # -- ATTENTION : ON AVAIT DEJA CETTE LISTE avec "nodup_entities_already_extracted" -----------------------------------#
    # --------------------------------------------------------------------------------------------------------------------#

    # --------------------------------------------------------------------------------------------------------------------#
    # -- NB) J'enlève "d'" du fichier des stopwords ! --------------------------------------------------------------------#
    # -- On avait avant modifification dans le fichier : -----------------------------------------------------------------#
    # -- 187 completement ------------------------------------------------------------------------------------------------#
    # -- 188 d' ----------------------------------------------------------------------------------------------------------#
    # -- 189 d'abord -----------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------#

    # Cas 1
    # if path_input != None and dict_product == None:
    # 16/04/2019 : ajout cas "all"
    # if path_input != None and method == "all_except_one":
    # 26/04/2019: ajout du paramètre "all_with_filter"
    # if (path_input != None and method == "all_except_one") or (path_input != None and method == "all"):

    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # if (path_input != None and method == "all_except_one") or (path_input != None and method == "all") or (path_input != None and method == "all_with_filter"):

    # 20/05/2019 : le cas "all_except_one", ne sert plus à rien
    # if method == "all_except_one" or method == "all" or method == "all_with_filter":

    #  28/05/2019 : on n'a pas besoin de "all_with_filter" car on peut maintenant utiliser "all" à la place
    # if method == "all" or method == "all_with_filter":
    if method == "all":
        print("On fait le cas 1")

        array_X_phrases_descriptions = np.array(dedup_X_phrases_descriptions_to_use, dtype=list)

        array_1_grams = np.array(list(df_all_1_grams['un_grams']), dtype=list)
        array_2_grams = np.array(list(df_all_2_grams['deux_grams']), dtype=list)
        array_3_grams = np.array(list(df_all_3_grams['trois_grams']), dtype=list)
        array_4_grams = np.array(list(df_all_4_grams['quatre_grams']), dtype=list)

        my_intersection_1_grams = [list(array_X_phrases_descriptions[np.where(array_X_phrases_descriptions == each)])
                                   for each in array_1_grams]
        my_intersection_2_grams = [list(array_X_phrases_descriptions[np.where(array_X_phrases_descriptions == each)])
                                   for each in array_2_grams]
        my_intersection_3_grams = [list(array_X_phrases_descriptions[np.where(array_X_phrases_descriptions == each)])
                                   for each in array_3_grams]
        my_intersection_4_grams = [list(array_X_phrases_descriptions[np.where(array_X_phrases_descriptions == each)])
                                   for each in array_4_grams]

        flattened_intersection_1_grams = [item for sublist in my_intersection_1_grams for item in sublist]
        flattened_intersection_2_grams = [item for sublist in my_intersection_2_grams for item in sublist]
        flattened_intersection_3_grams = [item for sublist in my_intersection_3_grams for item in sublist]
        flattened_intersection_4_grams = [item for sublist in my_intersection_4_grams for item in sublist]

        # for row in df_all_1_grams.itertuples():
        #     for X_phrases in array_X_phrases_descriptions :
        #         if X_phrases == row.un_grams and X_phrases not in liste_X_phrases_found_in_1_grams_descriptions:
        #             liste_X_phrases_found_in_1_grams_new_title_all_descriptions.append(X_phrases)

        liste_X_phrases_found_in_1_grams_descriptions = []

        for each in flattened_intersection_1_grams:
            if each not in liste_X_phrases_found_in_1_grams_descriptions and each != '':
                liste_X_phrases_found_in_1_grams_descriptions.append(each)

        liste_X_phrases_found_in_2_grams_descriptions = []

        # for row in df_all_2_grams.itertuples():
        #     for X_phrases in array_X_phrases_descriptions :
        #         if X_phrases == row.deux_grams and X_phrases not in liste_X_phrases_found_in_2_grams_descriptions:
        #             liste_X_phrases_found_in_2_grams_new_title_all_descriptions.append(X_phrases)

        for each in flattened_intersection_2_grams:
            if each not in liste_X_phrases_found_in_2_grams_descriptions and each != '':
                liste_X_phrases_found_in_2_grams_descriptions.append(each)

        liste_X_phrases_found_in_3_grams_descriptions = []

        # for row in df_all_3_grams.itertuples():
        #     for X_phrases in array_X_phrases_descriptions:
        #         if  X_phrases == row.trois_grams  and X_phrases not in liste_X_phrases_found_in_3_grams_descriptions:
        #             liste_X_phrases_found_in_3_grams_new_title_all_descriptions.append(X_phrases)
        for each in flattened_intersection_3_grams:
            if each not in liste_X_phrases_found_in_3_grams_descriptions and each != '':
                liste_X_phrases_found_in_3_grams_descriptions.append(each)

        liste_X_phrases_found_in_4_grams_descriptions = []

        # for row in df_all_4_grams.itertuples():
        #     for X_phrases in array_X_phrases_descriptions:
        #         if X_phrases == row.quatre_grams  and X_phrases not in liste_X_phrases_found_in_4_grams_descriptions:
        #             liste_X_phrases_found_in_4_grams_new_title_all_descriptions.append(X_phrases)
        for each in flattened_intersection_4_grams:
            if each not in liste_X_phrases_found_in_4_grams_descriptions and each != '':
                liste_X_phrases_found_in_4_grams_descriptions.append(each)


        # 10/05/2019 : ces sauvegardes sont inutiles
        # On les met en commentaires
        # df_liste_X_phrases_found_in_1_grams = pd.DataFrame(liste_X_phrases_found_in_1_grams_descriptions,
        #                                                    columns=['un_grams_chunk'])
        # df_liste_X_phrases_found_in_1_grams.to_pickle(
        #     path_root + path_output + "/to_update_pkl/df_liste_X_phrases_found_in_1_grams.pkl")
        #
        # df_liste_X_phrases_found_in_2_grams = pd.DataFrame(liste_X_phrases_found_in_2_grams_descriptions,
        #                                                    columns=['deux_grams_chunk'])
        # df_liste_X_phrases_found_in_2_grams.to_pickle(
        #     path_root + path_output + "/to_update_pkl/df_liste_X_phrases_found_in_2_grams.pkl")
        #
        # df_liste_X_phrases_found_in_3_grams = pd.DataFrame(liste_X_phrases_found_in_3_grams_descriptions,
        #                                                    columns=['trois_grams_chunk'])
        # df_liste_X_phrases_found_in_3_grams.to_pickle(
        #     path_root + path_output + "/to_update_pkl/df_liste_X_phrases_found_in_3_grams.pkl")
        #
        # df_liste_X_phrases_found_in_4_grams = pd.DataFrame(liste_X_phrases_found_in_4_grams_descriptions,
        #                                                    columns=['quatre_grams_chunk'])
        # df_liste_X_phrases_found_in_4_grams.to_pickle(
        #     path_root + path_output + "/to_update_pkl/df_liste_X_phrases_found_in_4_grams.pkl")

    # Cas 2
    # elif path_input != None and dict_product != None:

    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # elif path_input != None and method == "new_one":
    elif method == "new_one":
        print("On fait le cas 2")

        # On fait ici l'intersection entre :
        # - les n-grams obtenus avec le titre du nouveau produit
        # - les chunks obtenus grace aux descriptions
        #   des produits utilisés pour la cas 1 et de la description du nouveau produit

        array_X_phrases_descriptions = np.array(dedup_X_phrases_descriptions_to_use, dtype=list)

        array_1_grams = np.array(list(df_all_1_grams['un_grams']), dtype=list)
        array_2_grams = np.array(list(df_all_2_grams['deux_grams']), dtype=list)
        array_3_grams = np.array(list(df_all_3_grams['trois_grams']), dtype=list)
        array_4_grams = np.array(list(df_all_4_grams['quatre_grams']), dtype=list)

        my_intersection_1_grams = [list(array_X_phrases_descriptions[np.where(array_X_phrases_descriptions == each)]) for each in array_1_grams]
        my_intersection_2_grams = [list(array_X_phrases_descriptions[np.where(array_X_phrases_descriptions == each)]) for each in array_2_grams]
        my_intersection_3_grams = [list(array_X_phrases_descriptions[np.where(array_X_phrases_descriptions == each)]) for each in array_3_grams]
        my_intersection_4_grams = [list(array_X_phrases_descriptions[np.where(array_X_phrases_descriptions == each)]) for each in array_4_grams]

        flattened_intersection_1_grams = [item for sublist in my_intersection_1_grams for item in sublist]
        flattened_intersection_2_grams = [item for sublist in my_intersection_2_grams for item in sublist]
        flattened_intersection_3_grams = [item for sublist in my_intersection_3_grams for item in sublist]
        flattened_intersection_4_grams = [item for sublist in my_intersection_4_grams for item in sublist]

        liste_X_phrases_found_in_1_grams_new_title_all_descriptions = []

        # for row in df_all_1_grams.itertuples():
        #     for X_phrases in array_X_phrases_descriptions :
        #         if X_phrases == row.un_grams and X_phrases not in liste_X_phrases_found_in_1_grams_descriptions:
        #             liste_X_phrases_found_in_1_grams_new_title_all_descriptions.append(X_phrases)

        for each in flattened_intersection_1_grams:
            if each not in liste_X_phrases_found_in_1_grams_new_title_all_descriptions and each != '':
                liste_X_phrases_found_in_1_grams_new_title_all_descriptions.append(each)

        liste_X_phrases_found_in_2_grams_new_title_all_descriptions = []

        # for row in df_all_2_grams.itertuples():
        #     for X_phrases in array_X_phrases_descriptions :
        #         if X_phrases == row.deux_grams and X_phrases not in liste_X_phrases_found_in_2_grams_descriptions:
        #             liste_X_phrases_found_in_2_grams_new_title_all_descriptions.append(X_phrases)

        for each in flattened_intersection_2_grams:
            if each not in liste_X_phrases_found_in_2_grams_new_title_all_descriptions and each != '':
                liste_X_phrases_found_in_2_grams_new_title_all_descriptions.append(each)

        liste_X_phrases_found_in_3_grams_new_title_all_descriptions = []

        # for row in df_all_3_grams.itertuples():
        #     for X_phrases in array_X_phrases_descriptions:
        #         if  X_phrases == row.trois_grams  and X_phrases not in liste_X_phrases_found_in_3_grams_descriptions:
        #             liste_X_phrases_found_in_3_grams_new_title_all_descriptions.append(X_phrases)
        for each in flattened_intersection_3_grams:
            if each not in liste_X_phrases_found_in_3_grams_new_title_all_descriptions and each != '':
                liste_X_phrases_found_in_3_grams_new_title_all_descriptions.append(each)

        liste_X_phrases_found_in_4_grams_new_title_all_descriptions = []

        # for row in df_all_4_grams.itertuples():
        #     for X_phrases in array_X_phrases_descriptions:
        #         if X_phrases == row.quatre_grams  and X_phrases not in liste_X_phrases_found_in_4_grams_descriptions:
        #             liste_X_phrases_found_in_4_grams_new_title_all_descriptions.append(X_phrases)
        for each in flattened_intersection_4_grams:
            if each not in liste_X_phrases_found_in_4_grams_new_title_all_descriptions and each != '':
                liste_X_phrases_found_in_4_grams_new_title_all_descriptions.append(each)

    # Entre la description du nouveau produit (slug = 'lima-chips-aux-lentilles-original-90g-p83002')
    # et tous les n-grams extraits à partir des produits du CAS 1
    # On obtient : 'proteines vegetales' et 'four'
    # Ce qui ne correspond pas à des entités présentes dans le titre du nouveau produit
    # dont le slug est : 'lima-chips-aux-lentilles-original-90g-p83002'

    # DONC ON CONSIDERE QUE : DELTA = "chunks" obtenus pour le "cas 2"(sans les chunks obtenus lors du "cas 1")

    # ON VA OBTENIR TOUS LES PRODUITS QUI PEUVENT MATCHER AVEC LE NOUVEAU PRODUIT
    # en ne considérant que les produits dont le titre nettoyé contient les entités contenues dans "delta"

    # if path_input != None and dict_product == None:
    # 16/04/2019 : ajout cas "all"
    # if path_input != None and method == "all_except_one":

    # 26/04/2019: ajout du paramètre "all_with_filter"
    # if (path_input != None and method == "all_except_one") or (path_input != None and method == "all"):

    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # if (path_input != None and method == "all_except_one") or (path_input != None and method == "all") or (path_input != None and method == "all_with_filter"):

    # 20/05/2019 : le cas "all_except_one", ne sert plus à rien
    # if method == "all_except_one" or method == "all" or method == "all_with_filter":

    #  28/05/2019 : on n'a pas besoin de "all_with_filter" car on peut maintenant utiliser "all" à la place
    # if method == "all" or method == "all_with_filter":
    if method == "all":
        df_to_use_next_step = title_et_ngrams

    # Cas 2 : "liste_X_phrases_found_in_1_grams_descriptions" devient la réunion de :
    # if path_input != None and dict_product != None:
    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # if path_input != None and method == "new_one":
    if method == "new_one":

        #     df_liste_X_phrases_found_in_1_grams =  pd.read_pickle(path_root + path_output + "/to_update_pkl/df_liste_X_phrases_found_in_1_grams.pkl")
        #     liste_X_phrases_found_in_1_grams_descriptions = list(df_liste_X_phrases_found_in_1_grams['un_grams_chunk']) + liste_X_phrases_found_in_1_grams_new_title_all_descriptions + liste_X_phrases_found_in_1_grams_case_1_new_description
        #     liste_X_phrases_found_in_1_grams_descriptions = list(df_liste_X_phrases_found_in_1_grams['un_grams_chunk']) + liste_X_phrases_found_in_1_grams_new_title_all_descriptions
        liste_X_phrases_found_in_1_grams_descriptions = liste_X_phrases_found_in_1_grams_new_title_all_descriptions
        #     df_liste_X_phrases_found_in_2_grams = pd.read_pickle(path_root + path_output + "/to_update_pkl/df_liste_X_phrases_found_in_2_grams.pkl")
        #     liste_X_phrases_found_in_2_grams_descriptions = list(df_liste_X_phrases_found_in_2_grams['deux_grams_chunk']) + liste_X_phrases_found_in_2_grams_new_title_all_descriptions + liste_X_phrases_found_in_2_grams_case_1_new_description
        #     liste_X_phrases_found_in_2_grams_descriptions = list(df_liste_X_phrases_found_in_2_grams['deux_grams_chunk']) + liste_X_phrases_found_in_2_grams_new_title_all_descriptions
        liste_X_phrases_found_in_2_grams_descriptions = liste_X_phrases_found_in_2_grams_new_title_all_descriptions

        #     df_liste_X_phrases_found_in_3_grams = pd.read_pickle(path_root + path_output + "/to_update_pkl/df_liste_X_phrases_found_in_3_grams.pkl")
        #     liste_X_phrases_found_in_3_grams_descriptions = list(df_liste_X_phrases_found_in_3_grams['trois_grams_chunk']) + liste_X_phrases_found_in_3_grams_new_title_all_descriptions + liste_X_phrases_found_in_3_grams_case_1_new_description
        #     liste_X_phrases_found_in_3_grams_descriptions =  list(df_liste_X_phrases_found_in_3_grams['trois_grams_chunk']) + liste_X_phrases_found_in_3_grams_new_title_all_descriptions
        liste_X_phrases_found_in_3_grams_descriptions = liste_X_phrases_found_in_3_grams_new_title_all_descriptions
        #     df_liste_X_phrases_found_in_4_grams = pd.read_pickle(path_root + path_output + "/to_update_pkl/df_liste_X_phrases_found_in_4_grams.pkl")
        #     liste_X_phrases_found_in_4_grams_descriptions = list(df_liste_X_phrases_found_in_4_grams['quatre_grams_chunk']) + liste_X_phrases_found_in_4_grams_new_title_all_descriptions + liste_X_phrases_found_in_4_grams_case_1_new_description
        #     liste_X_phrases_found_in_4_grams_descriptions = list(df_liste_X_phrases_found_in_4_grams['quatre_grams_chunk']) + liste_X_phrases_found_in_4_grams_new_title_all_descriptions
        liste_X_phrases_found_in_4_grams_descriptions = liste_X_phrases_found_in_4_grams_new_title_all_descriptions

        # Calcul du DELTA des chunks entre cas 1 et cas 2
        delta = liste_X_phrases_found_in_1_grams_descriptions + liste_X_phrases_found_in_2_grams_descriptions + liste_X_phrases_found_in_3_grams_descriptions + liste_X_phrases_found_in_4_grams_descriptions
        # df_to_use_next_step = pd.concat([title_et_ngrams, title_et_ngrams_all_slugs])
        df_to_use_next_step = pd.concat([title_et_ngrams, title_et_ngrams_all_slugs_except_one])
        df_to_use_next_step = df_to_use_next_step[df_to_use_next_step['title_without_stopwords_new'].str.contains(step_9.list_entity_to_str(delta))]

    # LA PARTIE CI-DESSOUS EST OBLIGATOIRE:
    # pour savoir identifier les n-grams
    # qui sont présents dans les titres de tous les produits

    # CAS 2: l'étape ci-dessous n'est appliquée que aux slugs dont le découpage peut etre amélioré

    #--------------------------------------------------------------------------------------------------------------------#
    #-- step_3_find_xphrases_in_titles ----------------------------------------------------------------------------------#
    #-- Ici on trouve les entités présentes dans les titres -------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#

    if liste_X_phrases_found_in_1_grams_descriptions != []:
        array_X_phrases_1_grams_descriptions = np.array(liste_X_phrases_found_in_1_grams_descriptions, dtype=list)

        dict_result_1_grams = dict()
        for i, row in enumerate(df_to_use_next_step.itertuples(), 1):
            liste_X_phrases_found = []
            X_phrases_found = dict()

            for X_phrases in array_X_phrases_1_grams_descriptions:
                if (np.char.rfind(np.array(row.title_without_stopwords_new, dtype=str), X_phrases) != -1 and re.search("(^|\s)" + re.escape(X_phrases) + "($|\s)", row.title_without_stopwords_new)):

                    if X_phrases not in liste_X_phrases_found:
                        liste_X_phrases_found.append(X_phrases)
                        X_phrases_found[(row.slug, row.distributeur, row.title_without_stopwords_new)] = liste_X_phrases_found

            if i == 1:
                dict_result_1_grams = X_phrases_found
            else:
                dict_result_1_grams = {**dict_result_1_grams, **X_phrases_found}

        del liste_X_phrases_found, X_phrases_found, X_phrases
        df_entites_X_phrases_1_grams_found = pd.DataFrame(list(dict_result_1_grams.items()), columns=['id', 'entity_X_phrases_1_grams_found'])

    if liste_X_phrases_found_in_2_grams_descriptions != []:
        array_X_phrases_2_grams_descriptions = np.array(liste_X_phrases_found_in_2_grams_descriptions, dtype=list)
        dict_result_2_grams = dict()
        for i, row in enumerate(df_to_use_next_step.itertuples(), 1):
            liste_X_phrases_found = []
            X_phrases_found = dict()

            for X_phrases in array_X_phrases_2_grams_descriptions:
                if (np.char.rfind(np.array(row.title_without_stopwords_new, dtype=str), X_phrases) != -1 and re.search("(^|\s)" + re.escape(X_phrases) + "($|\s)", row.title_without_stopwords_new)):

                    if X_phrases not in liste_X_phrases_found:
                        liste_X_phrases_found.append(X_phrases)
                        X_phrases_found[(row.slug, row.distributeur, row.title_without_stopwords_new)] = liste_X_phrases_found

            if i == 1:
                dict_result_2_grams = X_phrases_found
            else:
                dict_result_2_grams = {**dict_result_2_grams, **X_phrases_found}

        del liste_X_phrases_found, X_phrases_found, X_phrases
        df_entites_X_phrases_2_grams_found = pd.DataFrame(list(dict_result_2_grams.items()), columns=['id', 'entity_X_phrases_2_grams_found'])

    if liste_X_phrases_found_in_3_grams_descriptions != []:
        array_X_phrases_3_grams_descriptions = np.array(liste_X_phrases_found_in_3_grams_descriptions, dtype=list)
        dict_result_3_grams = dict()
        for i, row in enumerate(df_to_use_next_step.itertuples(), 1):

            liste_X_phrases_found = []
            X_phrases_found = dict()

            for X_phrases in array_X_phrases_3_grams_descriptions:
                if (np.char.rfind(np.array(row.title_without_stopwords_new, dtype=str), X_phrases) != -1 and re.search("(^|\s)" + re.escape(X_phrases) + "($|\s)", row.title_without_stopwords_new)):

                    if X_phrases not in liste_X_phrases_found:
                        liste_X_phrases_found.append(X_phrases)
                        X_phrases_found[(row.slug, row.distributeur, row.title_without_stopwords_new)] = liste_X_phrases_found

            if i == 1:
                dict_result_3_grams = X_phrases_found
            else:
                dict_result_3_grams = {**dict_result_3_grams, **X_phrases_found}

        del liste_X_phrases_found, X_phrases_found, X_phrases
        df_entites_X_phrases_3_grams_found = pd.DataFrame(list(dict_result_3_grams.items()), columns=['id', 'entity_X_phrases_3_grams_found'])

    if liste_X_phrases_found_in_4_grams_descriptions != []:
        array_X_phrases_4_grams_descriptions = np.array(liste_X_phrases_found_in_4_grams_descriptions, dtype=list)
        dict_result_4_grams = {}
        for i, row in enumerate(df_to_use_next_step.itertuples(), 1):

            liste_X_phrases_found = []
            X_phrases_found = {}
            for X_phrases in array_X_phrases_4_grams_descriptions:

                if (np.char.rfind(np.array(row.title_without_stopwords_new, dtype=str), X_phrases) != -1 and re.search("(^|\s)" + re.escape(X_phrases) + "($|\s)", row.title_without_stopwords_new)):
                    if X_phrases not in liste_X_phrases_found:
                        liste_X_phrases_found.append(X_phrases)
                        X_phrases_found[(row.slug, row.distributeur, row.title_without_stopwords_new)] = liste_X_phrases_found

            if i == 1:
                dict_result_4_grams = X_phrases_found
            else:
                dict_result_4_grams = {**dict_result_4_grams, **X_phrases_found}

        del liste_X_phrases_found, X_phrases_found, X_phrases
        df_entites_X_phrases_4_grams_found = pd.DataFrame(list(dict_result_4_grams.items()), columns=['id', 'entity_X_phrases_4_grams_found'])

    #--------------------------------------------------------------------------------------------------------------------#
    #------------------------------------- step_4_join_entities_extracted -----------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#

    try:
        df_entites_X_phrases_1_grams_found['slug'] = df_entites_X_phrases_1_grams_found['id'].map(lambda x: x[0])
        try:
            df_entites_X_phrases_2_grams_found['slug'] = df_entites_X_phrases_2_grams_found['id'].map(lambda x: x[0])
            merged_results = pd.merge(df_entites_X_phrases_1_grams_found, df_entites_X_phrases_2_grams_found[['slug', 'entity_X_phrases_2_grams_found']], on='slug', how='left')
        except:
            print("df_entites_X_phrases_2_grams_found n'existe pas")
            merged_results = df_entites_X_phrases_1_grams_found
    except:
        print("df_entites_X_phrases_1_grams_found n'existe pas")
        try:
            df_entites_X_phrases_2_grams_found['slug'] = df_entites_X_phrases_2_grams_found['id'].map(lambda x: x[0])
            merged_results = df_entites_X_phrases_2_grams_found
        except:
            print("df_entites_X_phrases_1_grams_found et df_entites_X_phrases_2_grams_found n'existent pas")

    try:
        df_entites_X_phrases_3_grams_found['slug'] = df_entites_X_phrases_3_grams_found['id'].map(lambda x: x[0])
        merged_results = pd.merge(merged_results, df_entites_X_phrases_3_grams_found[['slug', 'entity_X_phrases_3_grams_found']], on='slug', how='left')
        try:
            df_entites_X_phrases_4_grams_found['slug'] = df_entites_X_phrases_4_grams_found['id'].map(lambda x: x[0])
            merged_results = pd.merge(merged_results, df_entites_X_phrases_4_grams_found[['slug', 'entity_X_phrases_4_grams_found']], on='slug', how='left')
        except:
            print("df_entites_X_phrases_4_grams_found n'existe pas")
    except:
        print("df_entites_X_phrases_3_grams_found n'existe pas")
        try:
            df_entites_X_phrases_4_grams_found['slug'] = df_entites_X_phrases_4_grams_found['id'].map(lambda x: x[0])
            merged_results = pd.merge(merged_results, df_entites_X_phrases_4_grams_found[['slug', 'entity_X_phrases_4_grams_found']], on='slug', how='left')
        except:
            print("df_entites_X_phrases_3_grams_found et df_entites_X_phrases_4_grams_found n'existent pas")

    # all_results = merged_results[['id','slug','entity_X_phrases_1_grams_found', 'entity_X_phrases_2_grams_found','entity_X_phrases_3_grams_found','entity_X_phrases_4_grams_found']]
    all_results = merged_results.fillna("NA")

    # print("all_results avant Step 5", all_results.shape)

    #--------------------------------------------------------------------------------------------------------------------#
    #------------------------------------- step_5_ngrams_overlapped_and_not_overlapped ----------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#

    print ("Step 5: Extraction des entités dans les titres")

    # On crée une colonne avec toutes les "entity_X trouvées"
    all_results['all_entity_X_phrases']= all_results.apply(step_5.all_ngrams_X_phrases, axis = 1)

    # 10/09/2018
    # 1. combinaison des plus ngrams qui ne s'overlappent pas
    #  1.1 possibilité de favoriser les ngrams les plus longs
    #  1.2 possibilité de favoriser les ngrams plus cours
    # 2. si que des inclusions, on prend le plus long ngrams

    # 3. Choix des combinaisons avec somme des fréquences maximum = vraiment appliqué ?

    # all_results[all_results['slug'].str.contains('pur-jus')]

    # all_results.sample(n=10)[['all_entity_X_phrases']]

    all_results['not_overlapped_entity_X_phrases']= all_results['all_entity_X_phrases'].map(step_5.not_overlap_ngrams)

    # import nltk
    # nltk.download('punkt')

    all_results['before_overlaped']= all_results.apply(step_5.remove_ngrams_with_no_overlap, axis = 1)

    all_results['overlapped_entity_X_phrases']= all_results['before_overlaped'].map(step_5.overlap_ngrams)

    # all_results.sample(n=1)

    # On prend le ngrams qui contient tous les autres à partir de "overlapped_entity_X_phrases"
    # pour chaque ngrams de la la liste des ngrams :
    #     si un ngrams donné contient tous les autres ngrams alors je le garde !!!           
    all_results['keep_overlapped_entity_X_phrases']= all_results['overlapped_entity_X_phrases'].map(step_5.keep_ngrams_which_contains_others)                                           

    #--------------------------------------------------------------------------------------------------------------------#
    #------------------------------------- step_6_get_results -----------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------#

    print ("Step 6: Résultats préliminaires")

    all_results['final_result_X_phrases'] = all_results.apply(step_6.final_result, axis = 1)

    # Ajout de la colonne "title" sans l'année

    all_results["title_temp"] = all_results['id'].map(lambda x: x[2] if x != 'NA' else x)
    all_results["title"] = all_results['title_temp'].map(lambda x: re.sub('\d{4}','',x))
    all_results = all_results.drop(['title_temp'], axis =1)

    # Calcul de la différence "title" - "final_result_X_phrases" :
    all_results["difference_title_vs_final_result_X_phrases"] = all_results.apply(step_6.difference_title_vs_final_result_X_phrases, axis = 1)

    # Ajout de l'entité 1_grams si on en a trouvé une 
    all_results["final_result_X_phrases_bis"] = all_results.apply(step_6.add_entity_1_grams, axis = 1)


    #--------------------------------------------------------------------------------------------------------------------#
    #--- 07/02/2019 : AJOUTER l'étape si il existe une entité dans "title_splitted_uppercase_new" qui mappe -------------#
    #--- complètement une ou plusieurs entités de la colonne "final_result_X_phrases_bis" alors -------------------------#
    #--------------------------------------------------------------------------------------------------------------------#
    #-- remplacer ces entités de "final_result_X_phrases_bis" par celle de "title_splitted_uppercase_new" ---------------#
    #-- sinon ajouter l'entité de "title_splitted_uppercase_new" à la liste "final_result_X_phrases_bis" ----------------#
    #--------------------------------------------------------------------------------------------------------------------#

    # On part de "all_results" à merger avec orgc_descriptions[['xslug','xtitle','title_splitted_uppercase_new','title_splitted_guillemets']]
    # a "slug" égal "left join"
    # df_orgc_descriptions_temp = orgc_descriptions[['xslug','xtitle','xbrand','title_splitted_uppercase','title_splitted_guillemets']]
    #  df_orgc_descriptions_temp = orgc_descriptions[['xslug','xtitle','xbrand','breadcrumb','title_splitted_uppercase','title_splitted_guillemets']]
    # df_orgc_descriptions_temp = orgc_descriptions[['xslug','xtitle','xbrand','breadcrumb','xprice','title_splitted_uppercase','title_splitted_guillemets']]

    # if path_input != None and dict_product != None:
    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # if path_input != None and method == "new_one":
    if method == "new_one":
        # orgc_descriptions = pd.concat([orgc_descriptions, orgc_descriptions_all_slugs[list(orgc_descriptions)]])

        # 09/05/2019: on a besoin de "orgc_descriptions"
        # qui contient seulement les nouveaux produits
        orgc_descriptions_new_products = orgc_descriptions
        orgc_descriptions = pd.concat([orgc_descriptions, orgc_descriptions_all_slugs_except_one[list(orgc_descriptions_all_slugs_except_one)]])

    df_orgc_descriptions_temp = orgc_descriptions[['xslug', 'xtitle', 'xbrand', 'breadcrumb', 'xprice', 'title_splitted_uppercase', 'title_splitted_guillemets']]

    df_orgc_descriptions_temp.rename(columns={'xslug': 'slug'}, inplace=True)
    all_results = pd.merge(all_results, df_orgc_descriptions_temp, how="left", on="slug")

    all_results['xbrand_temp'] = all_results['xbrand'].map(lambda x: x if x != '' else "NA")
    all_results = all_results.drop(['xbrand'], axis=1)
    all_results.rename(columns={'xbrand_temp': 'brand'}, inplace=True)

    print ("Step 7: Extraction dans les titres des entités en majuscules")

    # print("all_results au début de Step 7:", all_results.shape)

    # On met en minuscules la colonne ''title_splitted_uppercase'
    all_results["title_temp"] = all_results['title_splitted_uppercase'].map(step_7.strip_and_lower_title_splitted_uppercase)

    all_results = all_results.drop("title_splitted_uppercase", axis =1)
    all_results.rename(columns={'title_temp': 'title_splitted_uppercase'}, inplace=True)

    all_results["words_title_uppercase"] = all_results['title_splitted_uppercase'].map(step_7.split_title_splitted_uppercase)

    all_results["temp_words"] = all_results.apply(step_7.test_presence_words, axis = 1)

    all_results["final_result_X_phrases_with_uppercase_entity"] = all_results.apply(step_7.add_real_entity_uppercase, axis = 1)

    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #--- Si "title_splitted_guillemets" != [] alors ------------------------------------------------------------------------------------------------------#
    #--- Si "final_result_X_phrases_with_uppercase_entity" est différent != [] alors ---------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #--- - enlever les entités de "final_result_X_phrases_with_uppercase_entity" dont les mots sont contenus dans "title_splitted_guillemets" ------------#
    #--- - ajouter la ou les entités de "title_splitted_guillemets" à "final_result_X_phrases_with_uppercase_entity" -------------------------------------#
    #--- Sinon ajouter la ou les entités de "title_splitted_guillemets" à "final_result_X_phrases_with_uppercase_entity" ---------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#

    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #--- On extrait d'abord l'entité entre guillemets de la colonne "final_result_X_phrases_with_uppercase_entity" ---------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#

    print ("Step 8: Extraction dans les titres des entités entre guillemets")

    # extract_entity_guillemets_current_result(['chocolat lait', 'riz complet', 'galettes', '"rice, choc"', '100g'])
    all_results['temp_entity_without_guillemets'] = all_results['final_result_X_phrases_with_uppercase_entity'].map(step_8.extract_remove_guillemets)

    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #--- On utilise maintenant les colonnes --------------------------------------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #--- * temp_entity_without_guillemets ----------------------------------------------------------------------------------------------------------------#
    #--- * title_splitted_guillemets ---------------------------------------------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#

    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #--- ** ATTENTION ** ---------------------------------------------------------------------------------------------------------------------------------#
    #--- On applique maintenant le meme process que pour les entités en majuscules -----------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#

    # On met en minuscules la colonne ''title_splitted_guillemets'
    all_results["title_temp"] = all_results['title_splitted_guillemets'].map(step_7.strip_and_lower_title_splitted_uppercase)
    all_results = all_results.drop("title_splitted_guillemets", axis =1)
    all_results.rename(columns={'title_temp': 'title_splitted_guillemets'}, inplace=True)

    all_results["words_title_guillemets"] = all_results['title_splitted_guillemets'].map(step_7.split_title_splitted_uppercase)

    all_results["temp_words_guillemets"] = all_results.apply(step_8.test_presence_words_guillemets, axis = 1)

    all_results["final_result_X_phrases_with_uppercase_and_guillemets_entity"] = all_results.apply(step_8.add_real_entity_guillemets, axis = 1)

    # On regarde le % de titres, parmi les ... produits, dont le découpage en entités permet de mapper complètement tous les mots des titres dans les millésimes
    # df_temp = all_results[['id','slug','xtitle','brand','final_result_X_phrases_with_uppercase_and_guillemets_entity']]
    # df_temp = all_results[['id','slug','xtitle','brand','breadcrumb','final_result_X_phrases_with_uppercase_and_guillemets_entity']]
    df_temp = all_results[['id', 'slug', 'xtitle', 'brand', 'breadcrumb', 'xprice', 'final_result_X_phrases_with_uppercase_and_guillemets_entity']]

    df_temp['title_without_year'] = all_results['id'].map(lambda x: x[2]).map(lambda x: re.sub('\d{4}', '', x))
    df_temp = df_temp.fillna("NA")

    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    # 12/02/2019 : On remplace l'indicateur "découpage entier" -------------------------------------------------------------------------------------------#
    #--- par un score de confiance ayant la déf suivante : -----------------------------------------------------------------------------------------------#
    #--- soit N le nombre de mots présents dans un titre donné -------------------------------------------------------------------------------------------#
    #--- taux de confiance = 100 % si (nombre de mots total présents dans les entités extraite/N)*100 = 100 ----------------------------------------------#
    #--- et si les entités extraites sont partagées par au moins 2 produits ------------------------------------------------------------------------------#
    #--- Et: ---------------------------------------------------------------------------------------------------------------------------------------------#
    #--- taux de confiance = x % si (nombre de mots total présents dans les entités extraites/N)*100 = x -------------------------------------------------#
    #--- et si les entités extraites sont partagées par au moins 2 produits ------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#

    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #--- On ne calcule plus le confidence score ici<br> --------------------------------------------------------------------------------------------------#
    #--- Mais plus bas avec les dictionnaire -------------------------------------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#

    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #--- A LA PLACE du filtre avec indicateur Oui/Non des titres entièrement découpés<br> ----------------------------------------------------------------#
    #--- On peut maintenant choisir une valeur du score de confiance afin d'avoir des chances<br> --------------------------------------------------------#
    #--- de tomber sur des couples qui matchent. ---------------------------------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#

    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #--- ATTENTION : on n'a plus les titres bruts : les récupérer ----------------------------------------------------------------------------------------#
    #--- pour les mapper jusqu'au résultat final ---------------------------------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#

    print ("Step 9: Liste des entités trouvées transformées en chaine de caractères")

    # On dédoublonne les entités dans la liste "final_result_X_phrases_with_uppercase_and_guillemets_entity"
    # et on enlève la valeur ''
    # 05/03/2019 : on en profite pour enlever le mot "bio" parmi les entités trouvées
    df_temp['nodup_final_result_X_phrases_with_uppercase_and_guillemets_entity'] = df_temp['final_result_X_phrases_with_uppercase_and_guillemets_entity'].map(step_9.nodup_entities)

    # df_with_x_confidence_rate = filter_confidence_score(60)
    df_with_x_no_confidence_rate = step_9.no_filter_confidence_score(df_temp)
    # df_with_x_confidence_rate['confidence_score'].describe()

    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Ce n'est pas fini : extraire les "slugs" qui n'ont pas de group by suivant "str_result"<br> ------------------------------------------------------#
    #-- a partir de leur "str_result", extraire toutes les combinaisons d'entités possibles<br> ----------------------------------------------------------#
    #-- Puis faire un group by suivant chaque autre découpage possible des titres<br> --------------------------------------------------------------------#
    #-- Cette méthode a l'air très lourde en calculs:<br> ------------------------------------------------------------------------------------------------#
    #-- il vaut mieux extraire la liste des "entités" à partir de "str_result" ? <br> --------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Autre méthode : ----------------------------------------------------------------------------------------------------------------------------------#
    #-- - On boucle sur chaque entité de la colonne "str_result" -----------------------------------------------------------------------------------------#
    #-- - On extrait les slugs/titres de distributeurs différents et de meme marque, qui contiennent cette entité ----------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- exemple : fromage bio|carrefour bio --------------------------------------------------------------------------------------------------------------#
    #-- On extrait les slugs/titres de distributeurs différents et de meme marque, qui contiennent : -----------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- * fromage bio|carrefour bio ----------------------------------------------------------------------------------------------------------------------#
    #-- * fromage bio ------------------------------------------------------------------------------------------------------------------------------------#
    #-- * carrefour bio ----------------------------------------------------------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- On ajoute le résultat dans une liste ou dictionnaire sous la forme [['entité',[[slug,titre,distributeur], ...,]] ---------------------------------#
    #-- {'entité',[[slug,titre,distributeur], ...,] ------------------------------------------------------------------------------------------------------#
     #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- AFIN d'obtenir la totalité des résultats ---------------------------------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#

    #---------------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Création du dictionnaire temporaire qui contient  <br> -----------------------------------------------------------------------------------------------#
    #-- * comme clé = l'entité -------------------------------------------------------------------------------------------------------------------------------#
    #-- * comme valeur la liste : [['slug','titre qui contient l'entité','distributeur','brand'], ...,['titre qui contient l'entité','distributeur','brand']]-#
    #---------------------------------------------------------------------------------------------------------------------------------------------------------#

    #---------------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- On travaille seulement avec les colonnes -------------------------------------------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------------------------------------------------------------------------------#

    # df_extraction_variant_nb_entities = df_with_x_no_confidence_rate[['slug','xtitle','brand','str_result','liste_id']]
    # df_extraction_variant_nb_entities = df_with_x_no_confidence_rate[['slug','xtitle','brand','breadcrumb','str_result','liste_id']]
    df_extraction_variant_nb_entities = df_with_x_no_confidence_rate[['slug','xtitle','brand','breadcrumb','xprice','str_result','liste_id']]

    #---------------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Extraction des combinaisons de une seule entité, présentes dans les titres ---------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------------------------------------------------------------------------------#

    print ("Step 10: Extraction des combinaisons de une seule entité,deux entités, trois entités, quatres entités et cinq entités présentes dans les titres")

    df_extraction_variant_nb_entities['str_result_one_entity'] = df_extraction_variant_nb_entities['str_result'].map(step_10.extraction_one_entity)

    #---------------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- ATTENTION : les confidence score sont en fait a calculer par entité ----------------------------------------------------------------------------------#
    #-- On les calcule maintenant pour chaque produit --------------------------------------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------------------------------------------------------------------------------#

    #---------------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Alimentation du dictionnaire "dict_results_by_one_entity_temp" ---------------------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------------------------------------------------------------------------------#

    dict_results_by_one_entity_temp = {}

    for row in df_extraction_variant_nb_entities.itertuples():
    # for entity in df_extraction_variant_nb_entities['str_result_one_entity']:
    #     temp = []
        for each in row.str_result_one_entity:
    #         print (each)
            if each not in dict_results_by_one_entity_temp.keys() and each in row.liste_id[2]:
                temp_slug_xtitle_distrib_brand = []
                dict_results_by_one_entity_temp[each] = []
    #             print (row.slug,"\n")  
                temp_slug_xtitle_distrib_brand.append(row.slug)
                temp_slug_xtitle_distrib_brand.append(row.xtitle)

                temp_slug_xtitle_distrib_brand.append(row.liste_id[1])
                temp_slug_xtitle_distrib_brand.append(row.brand)
                temp_slug_xtitle_distrib_brand.append(row.breadcrumb)
                temp_slug_xtitle_distrib_brand.append(row.xprice)
                temp_slug_xtitle_distrib_brand.append(row.liste_id[2])
    #             temp_slug_xtitle_distrib_brand.append(row.confidence_score)
    #             print ("1ère alim du dico avec la clé:", each, "avec valeur :", temp_slug_xtitle_distrib_brand,"\n")
                # Ajout du "confidence_score"
                temp_slug_xtitle_distrib_brand.append(len(each.split(' '))/len(row.liste_id[2].split(' ')))
                dict_results_by_one_entity_temp[each].append(temp_slug_xtitle_distrib_brand)
            
            elif each in dict_results_by_one_entity_temp.keys() and each in row.liste_id[2]:
                temp_slug_xtitle_distrib_brand = []
                #             print (row.slug,"\n")
                temp_slug_xtitle_distrib_brand.append(row.slug)
                temp_slug_xtitle_distrib_brand.append(row.xtitle)
                temp_slug_xtitle_distrib_brand.append(row.liste_id[1])
                temp_slug_xtitle_distrib_brand.append(row.brand)
                temp_slug_xtitle_distrib_brand.append(row.breadcrumb)
                temp_slug_xtitle_distrib_brand.append(row.xprice)
                temp_slug_xtitle_distrib_brand.append(row.liste_id[2])
    #             temp_slug_xtitle_distrib_brand.append(row.confidence_score)
    #             print ("Nouvelle alim dico avec la clé:", each, "avec valeur :", dict_temp[each],"\n")
                # Ajout du "confidence_score"
                temp_slug_xtitle_distrib_brand.append(len(each.split(' '))/len(row.liste_id[2].split(' ')))
                dict_results_by_one_entity_temp[each].append(temp_slug_xtitle_distrib_brand) 

    #---------------------------------------------------------------------------------------------------------------------------------------------------------#           
    #-- On ne garde dans le dictionnaire que les produits de distributeurs différents et de meme marque ------------------------------------------------------#
    #---------------------------------------------------------------------------------------------------------------------------------------------------------# 

    # Avant on met le dictionnaire dans un dataframe
    # df_results_by_one_entity_temp = pd.DataFrame.from_dict(dict_results_by_one_entity_temp,orient='index')
    # df_results_by_one_entity_temp.T
    # PAS FACILE APRES

    #---------------------------------------------------------------------------------------------------------------------------------------------------------# 
    #-- On ne garde dans le dictionnaire que les produits de distributeurs différents et de meme marque ------------------------------------------------------# 
    #-- cette fois, on travaille avec le dictionnaire --------------------------------------------------------------------------------------------------------# 
    #---------------------------------------------------------------------------------------------------------------------------------------------------------# 

    dict_results_by_one_entity = {}
    for k in dict_results_by_one_entity_temp.keys():
        dict_results_by_one_entity[k] = []
        # boucle sur chaque produit
        for l in range(0,len(dict_results_by_one_entity_temp[k])):
            for m in range(0,len(dict_results_by_one_entity_temp[k])):
                # Si on a 2 produits de distributeurs différents et de meme marque
                if l != m and dict_results_by_one_entity_temp[k][l][2] != dict_results_by_one_entity_temp[k][m][2] and dict_results_by_one_entity_temp[k][l][3] == dict_results_by_one_entity_temp[k][m][3]:
    #                 Ajout des 2 produits dans le dictionnaire
                    dict_results_by_one_entity[k].append([dict_results_by_one_entity_temp[k][l],dict_results_by_one_entity_temp[k][m]])


    # for each in dict_results_by_one_entity['chocolat noir']:
    #     print ("moyenne pour : ",each[0], "et", each[1])
    #     print((each[0][5] + each[1][5])/2)

    #--------------------------------------------------------------------------------------------------------------------------------------------------# 
    #------------- Il manque le score = moyenne des scores --------------------------------------------------------------------------------------------#
    #------------- On supprime les entrées du dictionnaire avec valeurs == [] -------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    for key in [ k for (k,v) in dict_results_by_one_entity.items() if not v ]:
        del dict_results_by_one_entity[key]
    # ou 
    # dict_results_by_one_entity = dict( [ (k,v) for (k,v) in dict_results_by_one_entity.items() if v] 

    #--------------------------------------------------------------------------------------------------------------------------------------------------# 
    #-- On calcule le score moyen par couple de produits ----------------------------------------------------------------------------------------------# 
    #-- ATTENTION: il y a une erreur dans le calcul des scores de chaque produit ----------------------------------------------------------------------# 
    #-- C'EST A CORRIGER en amont ---------------------------------------------------------------------------------------------------------------------# 
    #--------------------------------------------------------------------------------------------------------------------------------------------------# 

    # dict_results_by_one_entity_with_scores_computed = {}
    # for k in dict_results_by_one_entity.keys():
    #     dict_results_by_one_entity_with_scores_computed[k] = []
    #     # Boucle sur chaque couple de produits
    #     for each_couple in dict_results_by_one_entity[k]:
    #         print (each_couple)

    #--------------------------------------------------------------------------------------------------------------------------------------------------# 
    #-- Maintenant on calcule les scores pour chaque produit de chaque couple de produits -------------------------------------------------------------# 
    #--------------------------------------------------------------------------------------------------------------------------------------------------# 

    # for k in dict_results_by_one_entity.keys():
    # #     dict_results_by_one_entity_with_scores_computed[k] = []
    #     # Boucle sur chaque couple de produits
    #     print (k)

    #--------------------------------------------------------------------------------------------------------------------------------------------------# 
    #-- ON FAIT QUOI avec cette entité '' ? -----------------------------------------------------------------------------------------------------------# 
    #-- On la supprime du dictionnaire ----------------------------------------------------------------------------------------------------------------# 
    #--------------------------------------------------------------------------------------------------------------------------------------------------# 

    if '' in dict_results_by_one_entity.keys():
        del dict_results_by_one_entity['']

    # dict_results_by_one_entity_with_scores_computed = {}
    # for k in dict_results_by_one_entity.keys():
    # #     print (k)
    #     dict_results_by_one_entity_with_scores_computed[k] = []
    #     # Boucle sur chaque couple de produits
    #     for each_couple in dict_results_by_one_entity[k]:
    # #         print (each_couple)
    # #         print ("Moyenne des scores pour : ",each_couple[0], "et", each_couple[1])
    # #         print((each_couple[0][5] + each_couple[1][5])/2)
    #         each_couple.append((each_couple[0][5] + each_couple[1][5])/2)
    #         dict_results_by_one_entity_with_scores_computed[k].append(each_couple)

    #--------------------------------------------------------------------------------------------------------------------------------------------------# 
    #-- Comment restituer proprement ? <br> -----------------------------------------------------------------------------------------------------------#
    #-- Comment mettre tous les couples de produits à plat cad faire une ligne  <br> ------------------------------------------------------------------#
    #-- pour chaque couple de produits  <br>
    #-- pour chaque entité qui est présente dans les titres "nettoyés" <br>
    #-- On veut donc autant de lignes par entité, qu'il y a de couples de produits
    #--------------------------------------------------------------------------------------------------------------------------------------------------# 

    # 24/04/2019: correction car le dictionnaire peut etre vide
    # ce qui conduit à une erreur
    if len(dict_results_by_one_entity) != 0:
        df_temp = pd.DataFrame.from_dict(dict_results_by_one_entity, orient='index')
        df_results_by_one_entity = df_temp.stack().to_frame()
        df_results_by_one_entity.rename(columns={0: 'couples'}, inplace=True)
        del df_temp
    else:
        print("Le dataframe dict_results_by_one_entity ne peut pas etre créé")

    #--------------------------------------------------------------------------------------------------------------------------------------------------# 
    #-- Extraction des combinaisons de 2 entités, présentes dans les titres ---------------------------------------------------------------------------# 
    #--------------------------------------------------------------------------------------------------------------------------------------------------# 

    df_extraction_variant_nb_entities['str_result_two_entities'] = df_extraction_variant_nb_entities['str_result_one_entity'].map(step_10.extraction_two_entities)

    # df_extraction_variant_nb_entities[df_extraction_variant_nb_entities['slug']  == 'chocolat-noir-cafe-amande-bio-ethiquable-3760091727619']

    # for row in df_extraction_variant_nb_entities.itertuples():
    #     for each in row.str_result_two_entities:
    #         for entity in each:
    #             if entity in row.liste_id[2]:
    #                 print (entity,"présente dans",row.liste_id[2])

    # A MAJ pour 2 entités
    dict_results_by_two_entity_temp = {}

    for row in df_extraction_variant_nb_entities.itertuples():
        for each in row.str_result_two_entities:
    #         print (each)
            sum_number_of_words = []
            tot = 0
            if each not in dict_results_by_two_entity_temp.keys():
                
                for entity in each:
                    
                    if entity in row.liste_id[2]:   
                        temp_slug_xtitle_distrib_brand = []
                        dict_results_by_two_entity_temp[each] = []
            #             print (row.slug,"\n")  
                        temp_slug_xtitle_distrib_brand.append(row.slug)
                        temp_slug_xtitle_distrib_brand.append(row.xtitle)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[1])
                        temp_slug_xtitle_distrib_brand.append(row.brand)
                        temp_slug_xtitle_distrib_brand.append(row.breadcrumb)
                        temp_slug_xtitle_distrib_brand.append(row.xprice)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[2])
            #             print ("1ère alim du dico avec la clé:", each, "avec valeur :", temp_slug_xtitle_distrib_brand,"\n")
                        # Ajout du "confidence_score"tot = 
                        tot = len(entity.split(' ')) + tot
                        sum_number_of_words.append(tot)
    #                     sum_number_of_words = len(entity.split(' ')) + sum_number_of_words
                    
                            
    #                     temp_slug_xtitle_distrib_brand.append(sum_number_of_words/len(row.liste_id[2].split(' ')))
                        if len(each) == len(sum_number_of_words):
                            temp_slug_xtitle_distrib_brand.append(max(sum_number_of_words)/len(row.liste_id[2].split(' ')))
                            dict_results_by_two_entity_temp[each].append(temp_slug_xtitle_distrib_brand)
            
            elif each in dict_results_by_two_entity_temp.keys():
                
                for entity in each:
                    
                    if entity in row.liste_id[2]:  
                        temp_slug_xtitle_distrib_brand = []
                        temp_slug_xtitle_distrib_brand.append(row.slug)
                        temp_slug_xtitle_distrib_brand.append(row.xtitle)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[1])
                        temp_slug_xtitle_distrib_brand.append(row.brand)
                        temp_slug_xtitle_distrib_brand.append(row.breadcrumb)
                        temp_slug_xtitle_distrib_brand.append(row.xprice)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[2])
            #             temp_slug_xtitle_distrib_brand.append(row.confidence_score)
            #             print ("Nouvelle alim dico avec la clé:", each, "avec valeur :", dict_temp[each],"\n")
                        # Ajout du "confidence_score"
                        tot = len(entity.split(' ')) + tot
                        sum_number_of_words.append(tot)
    #                     if each == ('petits pots', '4 mois') and row.liste_id[2] == 'petits pots poire provence 4 mois 2x130g':
    #                         print (row.liste_id[2],each, sum_number_of_words)
    #                         print (sum_number_of_words)
    #                         print (max(sum_number_of_words)/len(row.liste_id[2].split(' ')))
                        if len(each) == len(sum_number_of_words):
                            # if each == ('carotte', '6m') and row.liste_id[2] == 'petit pot carotte courge butternut & poulet 6m 2x200g bio':
                            #     print (row.liste_id[2],each, sum_number_of_words)
                            #     print (max(sum_number_of_words)/len(row.liste_id[2].split(' ')))
                            temp_slug_xtitle_distrib_brand.append(max(sum_number_of_words)/len(row.liste_id[2].split(' ')))
                            dict_results_by_two_entity_temp[each].append(temp_slug_xtitle_distrib_brand) 



    # dict_results_by_two_entity_temp[('fruits bio', 'muesli')]


    # On ne garde dans le dictionnaire que les produits de distributeurs différents et de meme marque
    # cette fois, on travaille avec le dictionnaire

    # dict_results_by_two_entity_temp[('carotte', '6m')]

    #--------------------------------------------------------------------------------------------------------------------------------------------------# 
    #-- Pour chaque clé de "dict_results_by_two_entity_temp", on dédoublonne --------------------------------------------------------------------------# 
    #-- suivant les 5ières composantes de "dict_results_by_two_entity_temp" ---------------------------------------------------------------------------# 
    #--------------------------------------------------------------------------------------------------------------------------------------------------# 

    dict_results_by_two_entity = {}
    for k in dict_results_by_two_entity_temp.keys():
        dict_results_by_two_entity[k] = []
        # boucle sur chaque produit
        for l in range(0,len(dict_results_by_two_entity_temp[k])):
            for m in range(0,len(dict_results_by_two_entity_temp[k])):
                # Si on a 2 produits de distributeurs différents et de meme marque
                if l != m and dict_results_by_two_entity_temp[k][l][2] != dict_results_by_two_entity_temp[k][m][2] and dict_results_by_two_entity_temp[k][l][3] == dict_results_by_two_entity_temp[k][m][3]:
    #                 Ajout des 2 produits dans le dictionnaire
                    dict_results_by_two_entity[k].append([dict_results_by_two_entity_temp[k][l],dict_results_by_two_entity_temp[k][m]])

    #--------------------------------------------------------------------------------------------------------------------------------------------------#                
    #-- On supprime les entrées du dictionnaire avec valeurs == [] ------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    for key in [ k for (k,v) in dict_results_by_two_entity.items() if not v ]:
        del dict_results_by_two_entity[key]

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- ON FAIT QUOI avec cette entité '' ? -----------------------------------------------------------------------------------------------------------#
    #-- On la supprime du dictionnaire ----------------------------------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    # dict_results_by_two_entity[('','')]

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- On n'a pas ces cas là : OK --------------------------------------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    # 24/04/2019: correction car le dictionnaire peut etre vide
    # ce qui conduit à une erreur

    if len(dict_results_by_two_entity) != 0:
        df_temp = pd.DataFrame.from_dict(dict_results_by_two_entity, orient='index')
        df_results_by_two_entity = df_temp.stack().to_frame()
        df_results_by_two_entity.rename(columns={0: 'couples'}, inplace=True)
        del df_temp
    else:
        print("Le dataframe df_results_by_two_entity ne peut pas etre créé")


    # df_results_by_two_entity.sample(n=10)
    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Extraction des combinaison de 3 entités, présentes dans les titres ----------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    df_extraction_variant_nb_entities['str_result_three_entities'] = df_extraction_variant_nb_entities['str_result_one_entity'].map(step_10.extraction_three_entities)

    # df_extraction_variant_nb_entities[df_extraction_variant_nb_entities['slug']  == 'chocolat-noir-cafe-amande-bio-ethiquable-3760091727619']

    # MAJ pour 3 entités
    dict_results_by_three_entity_temp = {}

    for row in df_extraction_variant_nb_entities.itertuples():
        for each in row.str_result_three_entities:
    #         print (each)
            sum_number_of_words = []
            tot = 0
            if each not in dict_results_by_three_entity_temp.keys() :
                
                for entity in each:
                    
                    if entity in row.liste_id[2]:   
                        temp_slug_xtitle_distrib_brand = []
                        dict_results_by_three_entity_temp[each] = []
            #             print (row.slug,"\n")  
                        temp_slug_xtitle_distrib_brand.append(row.slug)
                        temp_slug_xtitle_distrib_brand.append(row.xtitle)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[1])
                        temp_slug_xtitle_distrib_brand.append(row.brand)
                        temp_slug_xtitle_distrib_brand.append(row.breadcrumb)
                        temp_slug_xtitle_distrib_brand.append(row.xprice)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[2])
            #             print ("1ère alim du dico avec la clé:", each, "avec valeur :", temp_slug_xtitle_distrib_brand,"\n")
                        # Ajout du "confidence_score"
                        tot = len(entity.split(' ')) + tot
                        sum_number_of_words.append(tot)
    #                     sum_number_of_words = len(entity.split(' ')) + sum_number_of_words
    #                     temp_slug_xtitle_distrib_brand.append(sum_number_of_words/len(row.liste_id[2].split(' ')))
                        if len(each) == len(sum_number_of_words):
                            temp_slug_xtitle_distrib_brand.append(max(sum_number_of_words)/len(row.liste_id[2].split(' ')))
                            dict_results_by_three_entity_temp[each].append(temp_slug_xtitle_distrib_brand)
            
            elif each in dict_results_by_three_entity_temp.keys():
                
                for entity in each:
                    
                    if entity in row.liste_id[2]:  
                        temp_slug_xtitle_distrib_brand = []
                        temp_slug_xtitle_distrib_brand.append(row.slug)
                        temp_slug_xtitle_distrib_brand.append(row.xtitle)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[1])
                        temp_slug_xtitle_distrib_brand.append(row.brand)
                        temp_slug_xtitle_distrib_brand.append(row.breadcrumb)
                        temp_slug_xtitle_distrib_brand.append(row.xprice)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[2])
            #             temp_slug_xtitle_distrib_brand.append(row.confidence_score)
            #             print ("Nouvelle alim dico avec la clé:", each, "avec valeur :", dict_temp[each],"\n")
                        # Ajout du "confidence_score"
                        tot = len(entity.split(' ')) + tot
                        sum_number_of_words.append(tot)
    #                     if each == ('sel bio', 'noix', 'cajou') and row.liste_id[2] == 'noix cajou grillees a sec sel bio 100g':
    #                         print (row.liste_id[2],each, sum_number_of_words)
                        if len(each) == len(sum_number_of_words):
    #                             print (sum_number_of_words)
    #                             print (max(sum_number_of_words)/len(row.liste_id[2].split(' ')))
                            temp_slug_xtitle_distrib_brand.append(max(sum_number_of_words)/len(row.liste_id[2].split(' ')))
                            dict_results_by_three_entity_temp[each].append(temp_slug_xtitle_distrib_brand) 


    dict_results_by_three_entity = {}
    for k in dict_results_by_three_entity_temp.keys():
        dict_results_by_three_entity[k] = []
        # boucle sur chaque produit
        for l in range(0,len(dict_results_by_three_entity_temp[k])):
            for m in range(0,len(dict_results_by_three_entity_temp[k])):
                # Si on a 2 produits de distributeurs différents et de meme marque
                if l != m and dict_results_by_three_entity_temp[k][l][2] != dict_results_by_three_entity_temp[k][m][2] and dict_results_by_three_entity_temp[k][l][3] == dict_results_by_three_entity_temp[k][m][3]:
    #                 Ajout des 2 produits dans le dictionnaire
                    dict_results_by_three_entity[k].append([dict_results_by_three_entity_temp[k][l],dict_results_by_three_entity_temp[k][m]])


    for key in [ k for (k,v) in dict_results_by_three_entity.items() if not v ]:
        del dict_results_by_three_entity[key]

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Calcul des scores correct ? -------------------------------------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    # 24/04/2019: correction car le dictionnaire peut etre vide
    # ce qui conduit à une erreur

    # dict_results_by_three_entity = pd.DataFrame.from_dict(dict_results_by_three_entity,orient='index')
    # df_results_by_three_entity = dict_results_by_three_entity.stack().to_frame()
    # df_results_by_three_entity.rename(columns={0: 'couples'}, inplace=True)

    if len(dict_results_by_three_entity) != 0:
        df_temp = pd.DataFrame.from_dict(dict_results_by_three_entity, orient='index')
        df_results_by_three_entity = df_temp.stack().to_frame()
        df_results_by_three_entity.rename(columns={0: 'couples'}, inplace=True)
        del df_temp
    else:
        print("Le dataframe df_results_by_three_entity ne peut pas etre créé")

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Extraction des combinaison de 4 entités, présentes dans les titres ----------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    df_extraction_variant_nb_entities['str_result_four_entities'] = df_extraction_variant_nb_entities['str_result_one_entity'].map(step_10.extraction_four_entities)


    # MAJ pour 4 entités
    dict_results_by_four_entity_temp = {}

    for row in df_extraction_variant_nb_entities.itertuples():
        for each in row.str_result_four_entities:
    #         print (each)
            sum_number_of_words = []
            tot = 0
            if each not in dict_results_by_four_entity_temp.keys() :
                
                for entity in each:
                    
                    if entity in row.liste_id[2]:   
                        temp_slug_xtitle_distrib_brand = []
                        dict_results_by_four_entity_temp[each] = []
            #             print (row.slug,"\n")  
                        temp_slug_xtitle_distrib_brand.append(row.slug)
                        temp_slug_xtitle_distrib_brand.append(row.xtitle)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[1])
                        temp_slug_xtitle_distrib_brand.append(row.brand)
                        temp_slug_xtitle_distrib_brand.append(row.breadcrumb)
                        temp_slug_xtitle_distrib_brand.append(row.xprice)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[2])
            #             print ("1ère alim du dico avec la clé:", each, "avec valeur :", temp_slug_xtitle_distrib_brand,"\n")
                        # Ajout du "confidence_score"
                        tot = len(entity.split(' ')) + tot
                        sum_number_of_words.append(tot)
                        if len(each) == len(sum_number_of_words):
                            temp_slug_xtitle_distrib_brand.append(max(sum_number_of_words)/len(row.liste_id[2].split(' ')))
                            dict_results_by_four_entity_temp[each].append(temp_slug_xtitle_distrib_brand)
            
            elif each in dict_results_by_four_entity_temp.keys():
                
                for entity in each:
                    
                    if entity in row.liste_id[2]:  
                        temp_slug_xtitle_distrib_brand = []
                        temp_slug_xtitle_distrib_brand.append(row.slug)
                        temp_slug_xtitle_distrib_brand.append(row.xtitle)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[1])
                        temp_slug_xtitle_distrib_brand.append(row.brand)
                        temp_slug_xtitle_distrib_brand.append(row.breadcrumb)
                        temp_slug_xtitle_distrib_brand.append(row.xprice)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[2])
            #             temp_slug_xtitle_distrib_brand.append(row.confidence_score)
            #             print ("Nouvelle alim dico avec la clé:", each, "avec valeur :", dict_temp[each],"\n")
                        # Ajout du "confidence_score"
                        tot = len(entity.split(' ')) + tot
                        sum_number_of_words.append(tot)
    #                     if each == ('20 sachets', 'the') and row.liste_id[2] == 'the vert merveille de baies 20 sachets bio':
    #                         print (row.liste_id[2],each, sum_number_of_words)
    #                         print (sum_number_of_words)
    #                         print (max(sum_number_of_words)/len(row.liste_id[2].split(' ')))
                        if len(each) == len(sum_number_of_words):
                            temp_slug_xtitle_distrib_brand.append(max(sum_number_of_words)/len(row.liste_id[2].split(' ')))
                            dict_results_by_four_entity_temp[each].append(temp_slug_xtitle_distrib_brand) 

    # dict_results_by_four_entity_temp

    dict_results_by_four_entity = {}
    for k in dict_results_by_four_entity_temp.keys():
        dict_results_by_four_entity[k] = []
        # boucle sur chaque produit
        for l in range(0,len(dict_results_by_four_entity_temp[k])):
            for m in range(0,len(dict_results_by_four_entity_temp[k])):
                # Si on a 2 produits de distributeurs différents et de meme marque
                if l != m and dict_results_by_four_entity_temp[k][l][2] != dict_results_by_four_entity_temp[k][m][2] and dict_results_by_four_entity_temp[k][l][3] == dict_results_by_four_entity_temp[k][m][3]:
    #                 Ajout des 2 produits dans le dictionnaire
                    dict_results_by_four_entity[k].append([dict_results_by_four_entity_temp[k][l],dict_results_by_four_entity_temp[k][m]])

    for key in [ k for (k,v) in dict_results_by_four_entity.items() if not v ]:
        del dict_results_by_four_entity[key]

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Calcul des scores corrects ? ------------------------------------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    # 24/04/2019: correction car le dictionnaire peut etre vide
    # ce qui conduit à une erreur

    # dict_results_by_four_entity = pd.DataFrame.from_dict(dict_results_by_four_entity,orient='index')
    # df_results_by_four_entity = dict_results_by_four_entity.stack().to_frame()
    # df_results_by_four_entity.rename(columns={0: 'couples'}, inplace=True)
    if len(dict_results_by_four_entity) != 0:
        df_temp = pd.DataFrame.from_dict(dict_results_by_four_entity, orient='index')
        df_results_by_four_entity = df_temp.stack().to_frame()
        df_results_by_four_entity.rename(columns={0: 'couples'}, inplace=True)
        del df_temp
    else:
        print("Le dataframe df_results_by_four_entity ne peut pas etre créé")

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Jusqu'à combien d'entités utilise-t-on ? ------------------------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#


    # verif_nb_max_entities = df_extraction_variant_nb_entities
    # verif_nb_max_entities['len_str_result_four_entities'] = verif_nb_max_entities.str_result_four_entities.map(lambda x:len(x))
    # verif_nb_max_entities[verif_nb_max_entities.len_str_result_four_entities > 1]
    # verif_nb_max_entities['len_splitted_str_result'] = verif_nb_max_entities['str_result'].map(lambda x: len(x.split('|')))
    # verif_nb_max_entities[['len_splitted_str_result']].describe()
    # verif_nb_max_entities[verif_nb_max_entities.len_splitted_str_result == 16]

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Difficile pour l'instant de choisir jusqu'à combien d'entités aller ---------------------------------------------------------------------------#
    #-- Mais on peut voir sur un histogramme la distribution de "len_splitted_str_result" -------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    # import numpy as np
    # import matplotlib.pyplot as plt

    # plt.hist(verif_nb_max_entities['len_splitted_str_result'])
    # plt.show()

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Ci-dessous c'est un exemple avec 5 entités : --------------------------------------------------------------------------------------------------#
    #-- Comment trouver que : -------------------------------------------------------------------------------------------------------------------------#
    #--   20 sachets|vert matcha|the|supreme|bio    donne -------------------------------------------------------------------------------------------------------------------------#
    #-- [[pukka-the-vert-matcha-supreme-bio-20-sachets-p100327, gwz, the vert matcha supreme bio 20 sachets, 100.0, Pukka], [the-vert-matcha-supreme-20inf, ntr, the vert matcha supreme 20 sachets bio, 100.0, Pukka]] ----------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- On continue avec 5 entités --------------------------------------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    df_extraction_variant_nb_entities['str_result_five_entities'] = df_extraction_variant_nb_entities['str_result_one_entity'].map(step_10.extraction_five_entities)


    # MAJ pour 4 entités
    dict_results_by_five_entity_temp = {}

    for row in df_extraction_variant_nb_entities.itertuples():
        for each in row.str_result_five_entities:
    #         print (each)
            sum_number_of_words = []
            tot = 0
            if each not in dict_results_by_five_entity_temp.keys() :
                
                for entity in each:
                    
                    if entity in row.liste_id[2]:   
                        temp_slug_xtitle_distrib_brand = []
                        dict_results_by_five_entity_temp[each] = []
            #             print (row.slug,"\n")  
                        temp_slug_xtitle_distrib_brand.append(row.slug)
                        temp_slug_xtitle_distrib_brand.append(row.xtitle)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[1])
                        temp_slug_xtitle_distrib_brand.append(row.brand)
                        temp_slug_xtitle_distrib_brand.append(row.breadcrumb)
                        temp_slug_xtitle_distrib_brand.append(row.xprice)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[2])
            #             print ("1ère alim du dico avec la clé:", each, "avec valeur :", temp_slug_xtitle_distrib_brand,"\n")
                        # Ajout du "confidence_score"
                        tot = len(entity.split(' ')) + tot
                        sum_number_of_words.append(tot)
                        if len(each) == len(sum_number_of_words):
                            temp_slug_xtitle_distrib_brand.append(max(sum_number_of_words)/len(row.liste_id[2].split(' ')))
                            dict_results_by_five_entity_temp[each].append(temp_slug_xtitle_distrib_brand)
            
            elif each in dict_results_by_five_entity_temp.keys():
                
                for entity in each:
                    
                    if entity in row.liste_id[2]:  
                        temp_slug_xtitle_distrib_brand = []
                        temp_slug_xtitle_distrib_brand.append(row.slug)
                        temp_slug_xtitle_distrib_brand.append(row.xtitle)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[1])
                        temp_slug_xtitle_distrib_brand.append(row.brand)
                        temp_slug_xtitle_distrib_brand.append(row.breadcrumb)
                        temp_slug_xtitle_distrib_brand.append(row.xprice)
                        temp_slug_xtitle_distrib_brand.append(row.liste_id[2])
            #             temp_slug_xtitle_distrib_brand.append(row.confidence_score)
            #             print ("Nouvelle alim dico avec la clé:", each, "avec valeur :", dict_temp[each],"\n")
                        # Ajout du "confidence_score"
                        tot = len(entity.split(' ')) + tot
                        sum_number_of_words.append(tot)
    #                     if each == ('20 sachets', 'the') and row.liste_id[2] == 'the vert merveille de baies 20 sachets bio':
    #                         print (row.liste_id[2],each, sum_number_of_words)
    #                         print (sum_number_of_words)
    #                         print (max(sum_number_of_words)/len(row.liste_id[2].split(' ')))
                        if len(each) == len(sum_number_of_words):
                            temp_slug_xtitle_distrib_brand.append(max(sum_number_of_words)/len(row.liste_id[2].split(' ')))
                            dict_results_by_five_entity_temp[each].append(temp_slug_xtitle_distrib_brand) 


    dict_results_by_five_entity = {}
    for k in dict_results_by_five_entity_temp.keys():
    #     print (k)
        dict_results_by_five_entity[k] = []
        # boucle sur chaque produit
        for l in range(0,len(dict_results_by_five_entity_temp[k])):
            for m in range(0,len(dict_results_by_five_entity_temp[k])):
                # Si on a 2 produits de distributeurs différents et de meme marque
                if l != m and dict_results_by_five_entity_temp[k][l][2] != dict_results_by_five_entity_temp[k][m][2] and dict_results_by_five_entity_temp[k][l][3] == dict_results_by_five_entity_temp[k][m][3]:
    #                 Ajout des 2 produits dans le dictionnaire
                    dict_results_by_five_entity[k].append([dict_results_by_five_entity_temp[k][l],dict_results_by_five_entity_temp[k][m]])

    for key in [ k for (k,v) in dict_results_by_five_entity.items() if not v ]:
        del dict_results_by_five_entity[key]

    # 24/04/2019: correction car le dictionnaire peut etre vide
    # ce qui conduit à une erreur
    if len(dict_results_by_five_entity) != 0:
        df_temp = pd.DataFrame.from_dict(dict_results_by_five_entity, orient='index')
        df_results_by_five_entity = df_temp.stack().to_frame()
        df_results_by_five_entity.rename(columns={0: 'couples'}, inplace=True)
    else:
        print("Le dataframe df_results_by_five_entity ne peut pas etre créé")

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- On fait la restitution : ---------------------------------------------------------------------------------------------------------------------#
    #-- on rassemble : ---------------------------------------------------------------------------------------------------------------------#
    #-- - df_results_by_one_entity ---------------------------------------------------------------------------------------------------------------------#
    #-- - df_results_by_two_entity ---------------------------------------------------------------------------------------------------------------------#
    #-- - df_results_by_three_entity ---------------------------------------------------------------------------------------------------------------------#
    #-- - df_results_by_four_entity ---------------------------------------------------------------------------------------------------------------------#
    #-- - df_results_by_five_entity ---------------------------------------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    # 24/04/2019: correction car le dictionnaire peut etre vide
    # ce qui conduit à une erreur
    # all_results = pd.concat([df_results_by_one_entity, df_results_by_two_entity,df_results_by_three_entity,df_results_by_four_entity,df_results_by_five_entity])

    # print ("df_results_by_one_entity:", df_results_by_one_entity.shape)
    # print("df_results_by_one_entity:", df_results_by_two_entity.shape)
    # print("df_results_by_one_entity:", df_results_by_three_entity.shape)
    # print("df_results_by_one_entity:", df_results_by_four_entity.shape)
    # print("df_results_by_one_entity:", df_results_by_five_entity.shape)

    try:
        all_results = df_results_by_one_entity
        try:
            all_results = pd.concat([all_results, df_results_by_two_entity])
            try:
                all_results = pd.concat([all_results, df_results_by_three_entity])
                try:
                    all_results = pd.concat([all_results, df_results_by_four_entity])
                    try:
                        all_results = pd.concat([all_results, df_results_by_five_entity])
                    except:
                        print("Le dataframe df_results_by_five_entity n'existe pas")
                except:
                    print("Le dataframe df_results_by_four_entity n'existe pas")
            except:
                print("Le dataframe df_results_by_three_entity n'existe pas")
        except:
            print("Le dataframe df_results_by_two_entity n'existe pas")
    except:
        print("Le dataframe df_results_by_one_entity n'existe pas")

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- On crée les colonnes : ------------------------------------------------------------------------------------------------------------------------#
    #-- xtitle, distributeur, URLS, brand, confidence_score -------------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#


    all_results['slug_one'] = all_results['couples'].map(lambda x: x[0][0])
    all_results['slug_two'] = all_results['couples'].map(lambda x: x[1][0])

    all_results['xtitle_one'] = all_results['couples'].map(lambda x: x[0][1])
    all_results['xtitle_two'] = all_results['couples'].map(lambda x: x[1][1])
    all_results['distributeur_one'] = all_results['couples'].map(lambda x: x[0][2])
    all_results['distributeur_two'] = all_results['couples'].map(lambda x: x[1][2])
    all_results['brand_one'] = all_results['couples'].map(lambda x: x[0][3])
    all_results['brand_two'] = all_results['couples'].map(lambda x: x[1][3])

    # 26/03/2019: Extraction des breadcrumb des couples de produits
    all_results['breadcrumb_one'] = all_results['couples'].map(lambda x: x[0][4])
    all_results['breadcrumb_two'] = all_results['couples'].map(lambda x: x[1][4])

    # 02/04/2019: Extraction des prix des couples de produits
    all_results['price_one'] = all_results['couples'].map(lambda x: x[0][5])
    all_results['price_two'] = all_results['couples'].map(lambda x: x[1][5])

    print ("Step 11: Restitution finale")

    dict_slug_to_url = dict(zip(orgc_descriptions.xslug,orgc_descriptions.xurl))

    def urls(x):
    
        resultat = []
        for each in x:
            element = []
            element.append(dict_slug_to_url[each[0]])
            resultat.append(element)
        return resultat

    # all_results['URLS'] = all_results['couples'].map(step_11.urls)
    all_results['URLS'] = all_results['couples'].map(urls)
    all_results['URL_one'] = all_results['URLS'].map(lambda x:x[0][0])
    all_results['URL_two'] = all_results['URLS'].map(lambda x:x[1][0])
    all_results = all_results.drop("URLS", axis =1)

    print ("all_results avant idx_of_url:", all_results.shape)

    # if path_input != None and dict_product != None:
    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # if path_input != None and method == "new_one":
    if method == "new_one":
        # all_results = all_results[(all_results['slug_one'] == list(dict_one_product.keys())[0][0]) | (all_results['slug_two'] == list(dict_one_product.keys())[0][0])]
        # 09/05/2019: on doit filtrer grace aux URLS
        # présents dans "orgc_descriptions"

        # Extraction grace aux URLS distincts dans "orgc_descriptions"
        # idx_of_url = orgc_descriptions[orgc_descriptions['xurl'] == url_product].index.values.astype(int)[0]
        # slug_of_url = orgc_descriptions[orgc_descriptions['xurl'] == url_product].loc[idx_of_url, 'xslug']
        # all_results = all_results[(all_results['slug_one'] == slug_of_url) | (all_results['slug_two'] == slug_of_url)]

        all_results = all_results[(all_results['slug_one'].isin(list(orgc_descriptions_new_products['xslug']))) | (all_results['slug_two'].isin(list(orgc_descriptions_new_products['xslug'])))]

        # 09/05/2019: on doit filtrer grace aux URLS
        # del idx_of_url, slug_of_url

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Calcul du "confidence_score" pour chaque produit ----------------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    # 28/03/2019 : l'ajout du breadcrumb impacte le calcul du score
    # all_results['confidence_score'] = all_results['couples'].map(lambda x: (x[0][5] + x[1][5])/2)
    all_results['confidence_score'] = all_results['couples'].map(lambda x: (x[0][-1] + x[1][-1])/2)

    # 10/04/2019: on filtre les couples dont la similarité s est supérieure ou égale à s
    # if s != None:
    # 26/04/2019: ajout du cas "all_with_filter"
    # if threshold != None:

    #  28/05/2019 : on n'a pas besoin de "all_with_filter" car on peut maintenant utiliser "all" à la place
    # if threshold != None and method != "all_with_filter":
    if threshold != None and (method == "all" or method == "new_one"):

        # print ("type de threshold: ",type(threshold))
        all_results = all_results[all_results['confidence_score'] >= threshold]

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Tri décroissant suivant le "confidence_score" -------------------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    all_results =  all_results.sort_values(['confidence_score'], ascending = False)


    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- ON SAUVE les résultats (il manque encore l'exhaustivité des combinaisons dans ces résultats) --------------------------------------------------#
    #-- Et il n'y a pas les résultats à titres égaux --------------------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    # data_folder = "/home/hapax94/Documents/vincent/jupyter/carrefour_bio/output"
    # all_results.to_pickle(data_folder + '/all_results_BIO_with_five_entities_020319.pkl')
    # all_results = pd.read_pickle(data_folder + '/all_results_BIO_with_five_entities_020319.pkl')

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- On extrait les couples de slugs pour vérifier si il y a des couples en doublons ---------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    # On crée la colonne 'id_entities' grace à l'index du dataframe "all_results"
    all_results.reset_index(level=0, inplace=True)
    all_results.rename(columns={'level_0': 'id_entities'}, inplace=True)

    # all_results = all_results.drop("id_couple_slugs_1", axis =1)
    # all_results = all_results.drop("id_couple_slugs_2", axis =1)

    all_results['liste_of_slugs'] = all_results.apply(step_11.list_of_slugs, axis = 1)

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- On extrait tous les mots contenus dans "liste_of_slugs" ---------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    all_results['words_in_couples'] = all_results['liste_of_slugs'].map(step_11.split_into_words)

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- On dédoublonne les couples de produits grace a la liste des mots présents dans les slugs  -----------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    all_results = all_results.drop_duplicates(['words_in_couples'], keep='first')

    # all_results = all_results.set_index('id_entities')

    # all_results = all_results.drop("slug_one", axis =1)
    # all_results = all_results.drop("slug_two", axis =1)
    all_results = all_results.drop("liste_of_slugs", axis =1)
    all_results = all_results.drop("words_in_couples", axis =1)

    # On trie par "id_entities", "slug_one", "slug_two" et "confidence_score"
    # all_results.reset_index(level=0, inplace=True)
    all_results =  all_results.sort_values(['confidence_score','id_entities'], ascending = False)


    # 28/03/2019 : on va garder que les couples ayant des scores maximum
    # df_temp_groupby_slug_one_and_slug_two = all_results.groupby(['slug_one','slug_two'])[['confidence_score']].max().reset_index()

    # df_resultat_final = pd.merge(df_temp_groupby_slug_one_and_slug_two,all_results[['id_entities',
    # 'couples',
    # 'slug_one',                                                                        
    # 'slug_two',
    # 'xtitle_one',
    # 'xtitle_two',
    # 'distributeur_one',
    # 'distributeur_two',
    # 'brand_one',
    # 'brand_two',
    # 'breadcrumb_one',
    # 'breadcrumb_two',
    # 'price_one',
    # 'price_two',                                                                                                                                      
    # 'URL_one',
    # 'URL_two',
    # 'confidence_score']], on = ['slug_one','slug_two','confidence_score'], how = "inner")

    # df_resultat_final = df_resultat_final.sort_values(['confidence_score'], ascending = False)
    # --------------------------------------------------------------------------------------------------------------------------------------------------#
    # -- On transforme maintenant suivant: -------------------------------------------------------------------------------------------------------------#
    # -- crf, gwz -------------------------------------------------------------------------------------------------------------#
    # -- crf,ntr -------------------------------------------------------------------------------------------------------------#
    # -- crf,wbe -------------------------------------------------------------------------------------------------------------#
    # -- ntr,gwz -------------------------------------------------------------------------------------------------------------#
    # -- ntr,wbe -------------------------------------------------------------------------------------------------------------#
    # -- gwz,wbe -------------------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------------------------------------#

    all_results['slug_one_new'] = all_results.apply(step_11.slug_one_transform, axis=1)
    all_results['slug_two_new'] = all_results.apply(step_11.slug_two_transform, axis=1)

    all_results['xtitle_one_new'] = all_results.apply(step_11.xtitle_one_transform, axis=1)
    all_results['xtitle_two_new'] = all_results.apply(step_11.xtitle_two_transform, axis=1)

    all_results['distributeur_one_new'] = all_results.apply(step_11.distributeur_one_transform, axis=1)
    all_results['distributeur_two_new'] = all_results.apply(step_11.distributeur_two_transform, axis=1)

    all_results['brand_one_new'] = all_results.apply(step_11.brand_one_transform, axis=1)
    all_results['brand_two_new'] = all_results.apply(step_11.brand_two_transform, axis=1)

    all_results['breadcrumb_one_new'] = all_results.apply(step_11.breadcrumb_one_transform, axis=1)
    all_results['breadcrumb_two_new'] = all_results.apply(step_11.breadcrumb_two_transform, axis=1)

    all_results['price_one_new'] = all_results.apply(step_11.price_one_transform, axis=1)
    all_results['price_two_new'] = all_results.apply(step_11.price_two_transform, axis=1)

    all_results['url_one_new'] = all_results.apply(step_11.url_one_transform, axis=1)
    all_results['url_two_new'] = all_results.apply(step_11.url_two_transform, axis=1)

    all_results = all_results.drop("slug_one", axis=1)
    all_results = all_results.drop("slug_two", axis=1)
    all_results.rename(columns={'slug_one_new': 'slug_one'}, inplace=True)
    all_results.rename(columns={'slug_two_new': 'slug_two'}, inplace=True)

    all_results = all_results.drop("xtitle_one", axis=1)
    all_results = all_results.drop("xtitle_two", axis=1)
    all_results.rename(columns={'xtitle_one_new': 'xtitle_one'}, inplace=True)
    all_results.rename(columns={'xtitle_two_new': 'xtitle_two'}, inplace=True)

    all_results = all_results.drop("distributeur_one", axis=1)
    all_results = all_results.drop("distributeur_two", axis=1)
    all_results.rename(columns={'distributeur_one_new': 'distributeur_one'}, inplace=True)
    all_results.rename(columns={'distributeur_two_new': 'distributeur_two'}, inplace=True)

    all_results = all_results.drop("brand_one", axis=1)
    all_results = all_results.drop("brand_two", axis=1)
    all_results.rename(columns={'brand_one_new': 'brand_one'}, inplace=True)
    all_results.rename(columns={'brand_two_new': 'brand_two'}, inplace=True)

    all_results = all_results.drop("breadcrumb_one", axis=1)
    all_results = all_results.drop("breadcrumb_two", axis=1)
    all_results.rename(columns={'breadcrumb_one_new': 'breadcrumb_one'}, inplace=True)
    all_results.rename(columns={'breadcrumb_two_new': 'breadcrumb_two'}, inplace=True)

    all_results = all_results.drop("price_one", axis=1)
    all_results = all_results.drop("price_two", axis=1)
    all_results.rename(columns={'price_one_new': 'price_one'}, inplace=True)
    all_results.rename(columns={'price_two_new': 'price_two'}, inplace=True)

    all_results = all_results.drop("URL_one", axis=1)
    all_results = all_results.drop("URL_two", axis=1)
    all_results.rename(columns={'url_one_new': 'URL_one'}, inplace=True)
    all_results.rename(columns={'url_two_new': 'URL_two'}, inplace=True)

    # 18/04/2019 : NOUVEAU CODE
    # permet d'obtenir les couples en prenant le max par couple de distributeurs

    # Faire un groupby par rapport à :
    # - 'slug_one','distributeur_one','distributeur_two' en prenant le max(confidence_score)
    # - 'slug_two','distributeur_one','distributeur_two' en prenant le max(confidence_score)

    # df_temp_groupby_1 = all_results.groupby(['slug_one', 'distributeur_one', 'distributeur_two'])[['confidence_score']].max().reset_index()
    # df_temp_groupby_2 = all_results.groupby(['slug_two', 'distributeur_one', 'distributeur_two'])[['confidence_score']].max().reset_index()

    # # df_resultat_final_1 = pd.merge(df_temp_groupby_slug_one_and_slug_two,all_results[['id_entities',
    # df_resultat_final_1 = pd.merge(df_temp_groupby_1, all_results[['id_entities',
    #                                                                'couples',
    #                                                                'slug_one',
    #                                                                'slug_two',
    #                                                                'xtitle_one',
    #                                                                'xtitle_two',
    #                                                                'distributeur_one',
    #                                                                'distributeur_two',
    #                                                                'brand_one',
    #                                                                'brand_two',
    #                                                                'breadcrumb_one',
    #                                                                'breadcrumb_two',
    #                                                                'price_one',
    #                                                                'price_two',
    #                                                                'URL_one',
    #                                                                'URL_two',
    #                                                                #  'confidence_score']], on = ['slug_one','slug_two','confidence_score'], how = "inner")
    #                                                                'confidence_score']],
    #                                on=['slug_one', 'distributeur_one', 'distributeur_two', 'confidence_score'],
    #                                how="inner")

    # # df_resultat_final_2 = pd.merge(df_temp_groupby_slug_one_and_slug_two,all_results[['id_entities',
    # df_resultat_final_2 = pd.merge(df_temp_groupby_2, all_results[['id_entities',
    #                                                                'couples',
    #                                                                'slug_one',
    #                                                                'slug_two',
    #                                                                'xtitle_one',
    #                                                                'xtitle_two',
    #                                                                'distributeur_one',
    #                                                                'distributeur_two',
    #                                                                'brand_one',
    #                                                                'brand_two',
    #                                                                'breadcrumb_one',
    #                                                                'breadcrumb_two',
    #                                                                'price_one',
    #                                                                'price_two',
    #                                                                'URL_one',
    #                                                                'URL_two',
    #                                                                #  'confidence_score']], on = ['slug_one','slug_two','confidence_score'], how = "inner")
    #                                                                'confidence_score']],
    #                                on=['slug_two', 'distributeur_one', 'distributeur_two', 'confidence_score'],
    #                                how="inner")

    # df_resultat_final = pd.concat([df_resultat_final_1[['slug_one',
    #                                                     'slug_two',
    #                                                     'distributeur_one',
    #                                                     'distributeur_two',
    #                                                     'confidence_score',
    #                                                     'id_entities',
    #                                                     'couples',
    #                                                     'xtitle_one',
    #                                                     'xtitle_two',
    #                                                     'brand_one',
    #                                                     'brand_two',
    #                                                     'breadcrumb_one',
    #                                                     'breadcrumb_two',
    #                                                     'price_one',
    #                                                     'price_two',
    #                                                     'URL_one',
    #                                                     'URL_two']],
    #                                df_resultat_final_2[['slug_one',
    #                                                     'slug_two',
    #                                                     'distributeur_one',
    #                                                     'distributeur_two',
    #                                                     'confidence_score',
    #                                                     'id_entities',
    #                                                     'couples',
    #                                                     'xtitle_one',
    #                                                     'xtitle_two',
    #                                                     'brand_one',
    #                                                     'brand_two',
    #                                                     'breadcrumb_one',
    #                                                     'breadcrumb_two',
    #                                                     'price_one',
    #                                                     'price_two',
    #                                                     'URL_one',
    #                                                     'URL_two']]])

    # # ATTENTION: on dédoublonne
    # df_resultat_final = df_resultat_final.drop_duplicates(['slug_one',
    #                                                        'slug_two',
    #                                                        'distributeur_one',
    #                                                        'distributeur_two',
    #                                                        'confidence_score'], keep='first')

    # --------------------------------------------------------------------------------------------------------------------------------------------------#
    # -- 18/04/2019: travailler PLUTOT suivant la clé des couples 'slug_one' + 'slug_two' --------------------------------------------------------------#
    # -- OU PLUTOT trouver les clés 'slug_one' + "score max" -------------------------------------------------------------------------------------------#
    # -- ET les clés 'slug_two' + "score max" ----------------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------------------------------------#

    # --------------------------------------------------------------------------------------------------------------------------------------------------#
    # -- On traite chaque cas séparément : -------------------------------------------------------------------------------------------------------------#
    # -- crf, gwz --------------------------------------------------------------------------------------------------------------------------------------#
    # -- crf,ntr ---------------------------------------------------------------------------------------------------------------------------------------#
    # -- crf,wbe ---------------------------------------------------------------------------------------------------------------------------------------#
    # -- ntr,gwz ---------------------------------------------------------------------------------------------------------------------------------------#
    # -- ntr,wbe ---------------------------------------------------------------------------------------------------------------------------------------#
    # -- gwz,wbe ---------------------------------------------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------------------------------------#

    all_results_crf_gwz = all_results[(all_results['distributeur_one'] == 'crf') & (all_results['distributeur_two'] == 'gwz')]
    all_results_crf_ntr = all_results[(all_results['distributeur_one'] == 'crf') & (all_results['distributeur_two'] == 'ntr')]
    all_results_crf_wbe = all_results[(all_results['distributeur_one'] == 'crf') & (all_results['distributeur_two'] == 'wbe')]
    all_results_ntr_gwz = all_results[(all_results['distributeur_one'] == 'ntr') & (all_results['distributeur_two'] == 'gwz')]
    all_results_ntr_wbe = all_results[(all_results['distributeur_one'] == 'ntr') & (all_results['distributeur_two'] == 'wbe')]
    all_results_gwz_wbe = all_results[(all_results['distributeur_one'] == 'gwz') & (all_results['distributeur_two'] == 'wbe')]

    df_to_join_one = all_results_crf_gwz.groupby(['slug_one'])[['confidence_score']].max().reset_index()
    df_to_join_two = all_results_crf_gwz.groupby(['slug_two'])[['confidence_score']].max().reset_index()

    df_crf_gwz_with_score_max_one = pd.merge(all_results_crf_gwz, df_to_join_one, on=['slug_one', 'confidence_score'],how="inner")
    df_crf_gwz_with_score_max_two = pd.merge(all_results_crf_gwz, df_to_join_two, on=['slug_two', 'confidence_score'],how="inner")

    # jointure entre "df_crf_gwz_with_score_max_one" et "df_crf_gwz_with_score_max_two"
    # à 'slug_one', 'slug_two' et 'confidence_score' égaux
    df_resultat_crf_gwz = pd.merge(df_crf_gwz_with_score_max_one,df_crf_gwz_with_score_max_two[['slug_one', 'slug_two', 'confidence_score']],on=['slug_one', 'slug_two', 'confidence_score'], how='inner')

    df_to_join_one = all_results_crf_ntr.groupby(['slug_one'])[['confidence_score']].max().reset_index()
    df_to_join_two = all_results_crf_ntr.groupby(['slug_two'])[['confidence_score']].max().reset_index()
    df_crf_ntr_with_score_max_one = pd.merge(all_results_crf_ntr, df_to_join_one, on=['slug_one', 'confidence_score'],how="inner")
    df_crf_ntr_with_score_max_two = pd.merge(all_results_crf_ntr, df_to_join_two, on=['slug_two', 'confidence_score'],how="inner")
    df_resultat_crf_ntr = pd.merge(df_crf_ntr_with_score_max_one,df_crf_ntr_with_score_max_two[['slug_one', 'slug_two', 'confidence_score']],on=['slug_one', 'slug_two', 'confidence_score'], how='inner')

    df_to_join_one = all_results_crf_wbe.groupby(['slug_one'])[['confidence_score']].max().reset_index()
    df_to_join_two = all_results_crf_wbe.groupby(['slug_two'])[['confidence_score']].max().reset_index()
    df_crf_wbe_with_score_max_one = pd.merge(all_results_crf_wbe, df_to_join_one, on=['slug_one', 'confidence_score'],how="inner")
    df_crf_wbe_with_score_max_two = pd.merge(all_results_crf_wbe, df_to_join_two, on=['slug_two', 'confidence_score'],how="inner")
    df_resultat_crf_wbe = pd.merge(df_crf_wbe_with_score_max_one,df_crf_wbe_with_score_max_two[['slug_one', 'slug_two', 'confidence_score']],on=['slug_one', 'slug_two', 'confidence_score'], how='inner')

    df_to_join_one = all_results_ntr_gwz.groupby(['slug_one'])[['confidence_score']].max().reset_index()
    df_to_join_two = all_results_ntr_gwz.groupby(['slug_two'])[['confidence_score']].max().reset_index()
    df_ntr_gwz_with_score_max_one = pd.merge(all_results_ntr_gwz, df_to_join_one, on=['slug_one', 'confidence_score'],how="inner")
    df_ntr_gwz_with_score_max_two = pd.merge(all_results_ntr_gwz, df_to_join_two, on=['slug_two', 'confidence_score'],how="inner")
    df_resultat_ntr_gwz = pd.merge(df_ntr_gwz_with_score_max_one,df_ntr_gwz_with_score_max_two[['slug_one', 'slug_two', 'confidence_score']],on=['slug_one', 'slug_two', 'confidence_score'], how='inner')

    df_to_join_one = all_results_ntr_wbe.groupby(['slug_one'])[['confidence_score']].max().reset_index()
    df_to_join_two = all_results_ntr_wbe.groupby(['slug_two'])[['confidence_score']].max().reset_index()
    df_ntr_wbe_with_score_max_one = pd.merge(all_results_ntr_wbe, df_to_join_one, on=['slug_one', 'confidence_score'],how="inner")
    df_ntr_wbe_with_score_max_two = pd.merge(all_results_ntr_wbe, df_to_join_two, on=['slug_two', 'confidence_score'],how="inner")
    df_resultat_ntr_wbe = pd.merge(df_ntr_wbe_with_score_max_one,df_ntr_wbe_with_score_max_two[['slug_one', 'slug_two', 'confidence_score']],on=['slug_one', 'slug_two', 'confidence_score'], how='inner')

    df_to_join_one = all_results_gwz_wbe.groupby(['slug_one'])[['confidence_score']].max().reset_index()
    df_to_join_two = all_results_gwz_wbe.groupby(['slug_two'])[['confidence_score']].max().reset_index()
    df_gwz_wbe_with_score_max_one = pd.merge(all_results_gwz_wbe, df_to_join_one, on=['slug_one', 'confidence_score'],how="inner")
    df_gwz_wbe_with_score_max_two = pd.merge(all_results_gwz_wbe, df_to_join_two, on=['slug_two', 'confidence_score'],how="inner")
    df_resultat_gwz_wbe = pd.merge(df_gwz_wbe_with_score_max_one,df_gwz_wbe_with_score_max_two[['slug_one', 'slug_two', 'confidence_score']],on=['slug_one', 'slug_two', 'confidence_score'], how='inner')

    df_resultat_final = pd.concat([df_resultat_crf_gwz, df_resultat_crf_ntr, df_resultat_crf_wbe, df_resultat_ntr_gwz, df_resultat_ntr_wbe,df_resultat_gwz_wbe]).sort_values('confidence_score', ascending=False)

    # 18/04/2019: pas besoin de trier ici, car on le fait à la fin pour le résultat final
    # df_resultat_final = df_resultat_final.sort_values(['confidence_score'], ascending=False)

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- Ci-dessous, c'est un résultat sans utiliser l'information "contenance" des produits<br> -------------------------------------------------------#
    #-- * qui est des fois renseignée dans la colonne "xsubtitle" de certains distributeurs -----------------------------------------------------------#
    #-- * ou des fois est renseignée dans la colonne "xsubtitle" mais il s'agit plutot d'une description avec plein d'infos ---------------------------#
    #-- * ou des fois cette contenance est renseignée non pas dans la colonne "xsubtitle" mais dans une colonne "xcustom" -----------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #--- On pourrait donc mieux matcher les produits BIO, grace à la contenance des produits<br> ------------------------------------------------------#
    #--- à condtion d'avoir cette contenance renseignée proprement pour tous les produits. ------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- NB) La colonne "confidence_score" se base sur le fait que les entités trouvées par le chunking<br> --------------------------------------------#
    #-- restituées dans la colonne "str_result", permettent de mapper à hauteur de x %, les titres des produits. --------------------------------------#
    #-- Pour chaque ensemble de produits qui matchent, on fait ensuite la moyenne de ces scores<br> ---------------------------------------------------#
    #-- pour obtenir un "confidence_score" de matching. -----------------------------------------------------------------------------------------------#
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
    #-- On peut aussi utiliser les prix:<br>
    #-- On peut définir un seuil de différence entre les 2 prix d'un couple de produits<br>
    #--
    #-- Exemple : <br>
    #-- Si différence = 30 % du prix le plus bas alors écarter ces couples<br>
    #-- Ce seuil peut varier suivant si le prix est très bas, assez bas, assez élevé ou très élevé:<br>
    #-- on peut utiliser des quartiles pour les prix de tous les produits BIO<br>
    #-- Par exemple :
    #-- * Si 2 prix ne sont pas compris dans le meme quartile le plus bas :
    #--    appliquer "Si différence >= 20 % du prix le plus bas alors écarter ces couples"
    #--    avec le prix le plus bas qui appartient au 1er quartile
    #-- * Si 2 prix sont compris dans le meme quartile assez bas :
    #--    appliquer "Si différence >= 30 % du prix le plus bas alors écarter ces couples"
    #--   avec le prix le plus bas qui appartient au 2ème quartile
    #-- * Si 2 prix sont compris dans le meme quartile assez élevé :
    #--    appliquer "Si différence >= 35 % du prix assez élevé alors écarter ces couples"
    #--    avec le prix le plus bas qui appartient au 3ème quartile
    #-- * Si 2 prix sont compris dans le meme quartile très élevé :
    #--    appliquer "Si différence >= 40 % du prix très élevé alors écarter ces couples"
    #--    avec le prix le plus bas qui appartient au 4ème quartile
    #--------------------------------------------------------------------------------------------------------------------------------------------------#

    #****************************************************************************************************
    #**** On peut aussi compléter les résultats grace aux produits qui ont des titres nettoyés égaux ****
    #****************************************************************************************************

    # if path_input != None and dict_product == None:
    # 16/04/2019 : ajout cas "all"
    # if path_input != None and method == "all_except_one":
    # 26/04/2019: ajout du paramètre "all_with_filter"
    # if (path_input != None and method == "all_except_one") or (path_input != None and method == "all"):
    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # if (path_input != None and method == "all_except_one") or (path_input != None and method == "all") or (path_input != None and method == "all_with_filter"):

    # 20/05/2019 : le cas "all_except_one", ne sert plus à rien
    # if method == "all_except_one" or method == "all" or method == "all_with_filter":

    # 24/05/2019 : on n'a pas besoin de "all_with_filter" car on peut maintenant utiliser "all" à la place
    # if method == "all" or method == "all_with_filter":
    if method == "all":

    # 04/02/2019 : ajout de "str_result" suivant les titres égaux
        df_temp_bis = title_et_ngrams[['slug','distributeur','title_without_stopwords_new']]

        # On récupère : 'xtitle', 'xurl','xbrand' grace au dataframe "orgc_descriptions"

        # temp_xtitle_xurl_xbrand =  orgc_descriptions[['xslug','xtitle', 'xurl','xbrand']]
        # temp_xtitle_xurl_xbrand =  orgc_descriptions[['xslug','xtitle', 'xurl','xbrand','breadcrumb']]
        temp_xtitle_xurl_xbrand =  orgc_descriptions[['xslug','xtitle', 'xurl','xbrand','breadcrumb','xprice']]

        temp_xtitle_xurl_xbrand.rename(columns={'xslug': 'slug'}, inplace=True)

        df_temp_bis = pd.merge(df_temp_bis,temp_xtitle_xurl_xbrand, on = "slug", how = "inner")

        df_temp_bis = df_temp_bis.fillna("NA")

        # Sortir les lignes en doublons suivant "title"
        unique_titles = df_temp_bis['title_without_stopwords_new'].unique().tolist()

        liste_duptitles = []
        for title in unique_titles:
            count_title = 0
            for row in df_temp_bis.itertuples():
                if title in row.title_without_stopwords_new:
                    count_title += 1
                if count_title == 2:
                    liste_duptitles.append(title)

        # Mise en évidence de produits identiques avec distributeurs différents
        # et avec marques égales
        # df_same_titles = df_temp_bis[df_temp_bis['title_without_stopwords_new'].isin(list(set(liste_duptitles)))].sort_values(['title_without_stopwords_new','distributeur'])[['slug','xtitle','title_without_stopwords_new','distributeur','xurl','xbrand']]
        # df_same_titles = df_temp_bis[df_temp_bis['title_without_stopwords_new'].isin(list(set(liste_duptitles)))].sort_values(['title_without_stopwords_new','distributeur'])[['slug','xtitle','title_without_stopwords_new','distributeur','xurl','xbrand','breadcrumb']]
        df_same_titles = df_temp_bis[df_temp_bis['title_without_stopwords_new'].isin(list(set(liste_duptitles)))].sort_values(['title_without_stopwords_new','distributeur'])[['slug','xtitle','title_without_stopwords_new','distributeur','xurl','xbrand','breadcrumb','xprice']]
        df_temp = pd.merge(df_same_titles,df_same_titles, how = "inner", on = "title_without_stopwords_new")


        df_resultat_bis = df_temp[df_temp['distributeur_x'] != df_temp['distributeur_y']]
        df_resultat_bis = df_resultat_bis[df_resultat_bis['xbrand_x'] == df_resultat_bis['xbrand_y']]


        #--------------------------------------------------------------------------------------------------------------------------------------------------#
        #-- On met : --------------------------------------------------------------------------------------------------------------------------------------#
        #--    - la colonne "title_without_stopwords_new" en index ----------------------------------------------------------------------------------------#
        #--    - on crée la colonne de la forme [[slug,distributeur,brand,xtitle]] ------------------------------------------------------------------------#
        #--    - on renomme les colonnes title,distributeur, brand, URL -----------------------------------------------------------------------------------#
        #--    - enfin on crée la colonne "score" égale à 1 -----------------------------------------------------------------------------------------------#
        #-- Puis on concatène les résultats ---------------------------------------------------------------------------------------------------------------#
        #-- Puis export vers Excel ------------------------------------------------------------------------------------------------------------------------#
        #--------------------------------------------------------------------------------------------------------------------------------------------------#


        df_resultat_bis = df_resultat_bis.set_index('title_without_stopwords_new')

        del df_resultat_bis.index.name

        df_resultat_bis['couples'] = df_resultat_bis.apply(step_11.create_couples, axis = 1)

        #--------------------------------------------------------------------------------------------------------------------------------------------------#
        #-- on renomme les colonnes slug, title, distributeur, brand, URL ----------------------------------------------------------------------------------------#
        #-- en slug_one slug_two xtitle_one    xtitle_two    distributeur_one    distributeur_two    brand_one    brand_two    URL_one -------------------------------------------#
        #--------------------------------------------------------------------------------------------------------------------------------------------------#

        df_resultat_bis.rename(columns={'xtitle_x': 'xtitle_one'}, inplace=True)
        df_resultat_bis.rename(columns={'xtitle_y': 'xtitle_two'}, inplace=True)
        df_resultat_bis.rename(columns={'distributeur_x': 'distributeur_one'}, inplace=True)
        df_resultat_bis.rename(columns={'distributeur_y': 'distributeur_two'}, inplace=True)
        df_resultat_bis.rename(columns={'xbrand_x': 'brand_one'}, inplace=True)
        df_resultat_bis.rename(columns={'xbrand_y': 'brand_two'}, inplace=True)
        df_resultat_bis.rename(columns={'xurl_x': 'URL_one'}, inplace=True)
        df_resultat_bis.rename(columns={'xurl_y': 'URL_two'}, inplace=True)

        df_resultat_bis.rename(columns={'slug_x': 'slug_one'}, inplace=True)
        df_resultat_bis.rename(columns={'slug_y': 'slug_two'}, inplace=True)

        df_resultat_bis.rename(columns={'breadcrumb_x': 'breadcrumb_one'}, inplace=True)
        df_resultat_bis.rename(columns={'breadcrumb_y': 'breadcrumb_two'}, inplace=True)

        df_resultat_bis.rename(columns={'xprice_x': 'price_one'}, inplace=True)
        df_resultat_bis.rename(columns={'xprice_y': 'price_two'}, inplace=True)

        # df_resultat_bis = df_resultat_bis[['couples','slug_one','slug_two','xtitle_one','xtitle_two','distributeur_one','distributeur_two','brand_one','brand_two','URL_one','URL_two']]
        # df_resultat_bis = df_resultat_bis[['couples','slug_one','slug_two','xtitle_one','xtitle_two','distributeur_one','distributeur_two','brand_one','brand_two','breadcrumb_one','breadcrumb_two','URL_one','URL_two']]
        df_resultat_bis = df_resultat_bis[['couples','slug_one','slug_two','xtitle_one','xtitle_two','distributeur_one','distributeur_two','brand_one','brand_two','breadcrumb_one','breadcrumb_two','price_one', 'price_two','URL_one','URL_two']]
        #--------------------------------------------------------------------------------------------------------------------------------------------------#
        #-- ATTENTION les lignes sont doublonnées ---------------------------------------------------------------------------------------------------------#
        #--------------------------------------------------------------------------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------------------------------------------------------------------------#
        #-- On dédoublonne suivant l'index ----------------------------------------------------------------------------------------------------------------#
        #--------------------------------------------------------------------------------------------------------------------------------------------------#

        df_resultat_bis = df_resultat_bis[~df_resultat_bis.index.duplicated(keep='first')]

        #--------------------------------------------------------------------------------------------------------------------------------------------------#
        #-- Ajout de la colonne "confidence_score" et "id_entities" ---------------------------------------------------------------------------------------#
        #--------------------------------------------------------------------------------------------------------------------------------------------------#

        df_resultat_bis['confidence_score'] = 1
        df_resultat_bis['id_entities'] = df_resultat_bis.index

        # df_resultat_bis = df_resultat_bis[['id_entities','couples','slug_one','slug_two','xtitle_one','xtitle_two','distributeur_one','distributeur_two','brand_one','brand_two','URL_one','URL_two','confidence_score']]
        # df_resultat_bis = df_resultat_bis[['id_entities','couples','slug_one','slug_two','xtitle_one','xtitle_two','distributeur_one','distributeur_two','brand_one','brand_two','breadcrumb_one','breadcrumb_two','URL_one','URL_two','confidence_score']]
        df_resultat_bis = df_resultat_bis[['id_entities','couples','slug_one','slug_two','xtitle_one','xtitle_two','distributeur_one','distributeur_two','brand_one','brand_two','breadcrumb_one','breadcrumb_two','price_one','price_two','URL_one','URL_two','confidence_score']]

    # ATTENTION les 2 dataframes à concaténer ci-après, doivent avoir les colonnes dans le meme ordre
    # df_resultat_final = df_resultat_final[['id_entities','couples','slug_one','slug_two','xtitle_one','xtitle_two','distributeur_one','distributeur_two','brand_one','brand_two','breadcrumb_one','breadcrumb_two','URL_one','URL_two','confidence_score']]
    df_resultat_final = df_resultat_final[['id_entities','couples','slug_one','slug_two','xtitle_one','xtitle_two','distributeur_one','distributeur_two','brand_one','brand_two','breadcrumb_one','breadcrumb_two','price_one','price_two','URL_one','URL_two','confidence_score']]

        #--------------------------------------------------------------------------------------------------------------------------------------------------#
        #-- On concatène les résultats --------------------------------------------------------------------------------------------------------------------#
        #--------------------------------------------------------------------------------------------------------------------------------------------------#

    # 16/04/2019 : ajout cas "all"
    # if path_input != None and method == "all_except_one":

    # 26/04/2019: ajout du paramètre "all_with_filter"
    # if (path_input != None and method == "all_except_one") or (path_input != None and method == "all"):

    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # if (path_input != None and method == "all_except_one") or (path_input != None and method == "all") or (path_input != None and method == "all_with_filter"):

    # 20/05/2019 : le cas "all_except_one", ne sert plus à rien
    # if method == "all_except_one" or method == "all" or method == "all_with_filter":

    # 28/05/2019 : on n'a pas besoin de "all_with_filter" car on peut maintenant utiliser "all" à la place
    # if method == "all" or method == "all_with_filter":
    if method == "all":

        all_results_final = pd.concat([df_resultat_final, df_resultat_bis])

        # NOUVEAU : 15/04/2019
        #   Doublons possibles entre le résultat final et le résultat final
        all_results_final['liste_of_slugs'] = all_results_final.apply(step_11.list_of_slugs, axis=1)
        all_results_final['words_in_couples'] = all_results_final['liste_of_slugs'].map(step_11.split_into_words)
        all_results_final = all_results_final.drop_duplicates(['words_in_couples'], keep='first')
        all_results_final = all_results_final.drop("liste_of_slugs", axis=1)
        all_results_final = all_results_final.drop("words_in_couples", axis=1)

        #--------------------------------------------------------------------------------------------------------------------------------------------------#
        #-- Tri décroissant suivant "confidence_score" ----------------------------------------------------------------------------------------------------#
        #--------------------------------------------------------------------------------------------------------------------------------------------------#

        all_results_final = all_results_final.sort_values(['confidence_score'], ascending = False)

        # all_results_final.head(n=60)

        #*******************************************************************
        #**** Export vers Excel : résultat à envoyer à Hervé le 25/03/2019 *
        #*******************************************************************

    # if path_input != None and dict_product == None:
    # 16/04/2019 : ajout cas "all"

    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # if path_input != None and method == "all_except_one":

    # 20/05/2019 : le cas "all_except_one", ne sert plus à rien
    # if method == "all_except_one":
    #     if threshold != None:
    #         #output_file_name = 'all_results_BIO_SCRIPT_CONSOLE_with_exhaust_and_titles_equal_' + datetime.datetime.today().strftime("%d%m%y") + '_ALL_PRODUCTS_without_new_product_' + str(threshold) + '.xlsx'
    #         # output_file_name = 'all_results_BIO_with_exhaust_and_titles_equal_' + datetime.datetime.today().strftime("%Y%m%d") + '_' + method + '_' +  str(threshold) + '.xlsx'
    #         output_file_name = 'all_results_BIO_with_exhaust_and_titles_equal_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + '_' + method + '_' + str(threshold) + '.xlsx'
    #         # Sauvegarde en .pkl pour 3ème cas
    #         # all_results_final.to_pickle(path_root + path_output + "/to_extract_all_except_one/all_except_one_results_final_" + method + '_' + str(threshold) + '.pkl')
    #     else:
    #         # output_file_name = 'all_results_BIO_SCRIPT__CONSOLE_with_exhaust_and_titles_equal_' + datetime.datetime.today().strftime("%d%m%y") + '_ALL_PRODUCTS_without_new_product.xlsx'
    #         # output_file_name = 'all_results_BIO_with_exhaust_and_titles_equal_' + datetime.datetime.today().strftime("%Y%m%d") + '_' +  method + '.xlsx'
    #         output_file_name = 'all_results_BIO_with_exhaust_and_titles_equal_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + '_' + method + '.xlsx'
    #         # Sauvegarde en .pkl pour 3ème cas
    #         # all_results_final.to_pickle(path_root + path_output + "/to_extract_all_except_one/all_except_one_results_final_" + method + '.pkl')
    #     all_results_final.to_excel(path_root + path_output + '/' + output_file_name, index=False)

    # elif path_input != None and dict_product != None:
    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # elif path_input != None and method == "new_one":

    # 20/05/2019 : le cas "all_except_one", ne sert plus à rien
    # elif method == "new_one":
    if method == "new_one":
        if threshold != None:
            # output_file_name = 'all_results_BIO_SCRIPT_CONSOLE_with_exhaust_' + datetime.datetime.today().strftime("%d%m%y") + '_NEW_PRODUCT_' + str(threshold) + '.xlsx'
            # output_file_name = 'all_results_BIO_with_exhaust_' + datetime.datetime.today().strftime("%Y%m%d") + '_' +  method + '_' +  str(threshold) + '.xlsx'
            output_file_name = 'all_results_BIO_with_exhaust_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + '_' + method + '_' + str(threshold) + '.xlsx'
            # Sauvegarde en .pkl pour 3ème cas
            df_resultat_final.to_pickle(path_root + path_output + "/to_extract_new_one/all_results_final_" + method + '_' + str(threshold) + '.pkl')
        else:
            # output_file_name = 'all_results_BIO_SCRIPT_CONSOLE_with_exhaust_' + datetime.datetime.today().strftime("%d%m%y") + '_NEW_PRODUCT.xlsx'
            # output_file_name = 'all_results_BIO_with_exhaust_' + datetime.datetime.today().strftime("%Y%m%d") + '_' +  method + '.xlsx'
            output_file_name = 'all_results_BIO_with_exhaust_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + '_' + method + '.xlsx'
            # Sauvegarde en .pkl pour 3ème cas
            df_resultat_final.to_pickle(path_root + path_output + "/to_extract_new_one/all_results_final_" + method + '.pkl')
        df_resultat_final.to_excel(path_root + path_output + '/' + output_file_name, index=False)

    # 15/04/2019: ajout du cas lancement pour "all"
    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # elif path_input != None and method == "all":

    # 28/05/2019 : on n'a pas besoin de "all_with_filter" car on peut maintenant utiliser "all" à la place
    # elif method == "all":
    else:
        if threshold != None:
            # output_file_name = 'all_results_BIO_with_exhaust_and_titles_equal_' + datetime.datetime.today().strftime("%Y%m%d") + '_' +  method + '_' +  str(threshold) + '.xlsx'
            output_file_name = 'all_results_BIO_with_exhaust_and_titles_equal_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + '_' + method + '_' + str(threshold) + '.xlsx'
        else:
            # output_file_name = 'all_results_BIO_with_exhaust_and_titles_equal_' + datetime.datetime.today().strftime("%Y%m%d") + '_' + method + '.xlsx'
            output_file_name = 'all_results_BIO_with_exhaust_and_titles_equal_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + '_' + method + '.xlsx'

        # Sauvegarde en .pkl pour le 4ème cas
        all_results_final.to_pickle(path_root + path_output + "/to_extract_all/all_results_final_" + method + '.pkl')
        all_results_final.to_excel(path_root + path_output + '/' + output_file_name, index=False)

    # 26/04/2019: ajout du paramètre "all_with_filter"
    # 06/05/2019: on n'utilise plus le paramètre "path_input"
    # elif path_input != None and method == "all_with_filter":

    # 28/05/2019 : on n'a pas besoin de "all_with_filter" car on peut maintenant utiliser "all" à la place
    # On met en commentaires ci-dessous :
    # elif method == "all_with_filter":

        # output_file_name = 'all_results_BIO_with_exhaust_and_titles_equal_' + datetime.datetime.today().strftime("%Y%m%d") + '_' + method + '.xlsx'
        # output_file_name = 'all_results_BIO_with_exhaust_and_titles_equal_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + '_' + method + '.xlsx'

        # Sauvegarde en .pkl
        # all_results_final.to_pickle(path_root + path_output + "/to_extract_all/all_results_final_" + method + '.pkl')
        # all_results_final.to_excel(path_root + path_output + '/' + output_file_name, index=False)

# if __name__== "__main__":
#     # main(path_input_files, dict_one_product, 0.75)
#     # main(path_input_files, url_one_product, threshold_value,  method_chosen)
#
#     parser = argparse.ArgumentParser(description='test arguments')
#     parser.add_argument("-pi", "--path_input_files", help="path input file", required=True)
#     # 19/04/2019: pour permettre le lancement du cas "all", on met ce paramètre à None par défaut
#     # parser.add_argument("-u", "--url_one_product", help="url du nouveau produit", required=True)
#     parser.add_argument("-u", "--url_one_product", help="url du nouveau produit", default = None)
#     # parser.add_argument("-s", "--threshold_value", help="seuil de similarité", type=float, required=True)
#     parser.add_argument("-s", "--threshold_value", help="seuil de similarité", type=float, default = None)
#     # parser.add_argument("-m", "--method_chosen", help="lancer pour tous les produits excepté un ou seulement pour le nouveau produit", choices=["all_except_one","new_one"], default="all_except_one")
#     parser.add_argument("-m", "--method_chosen", help="lancer pour tous les produits excepté un ou seulement pour le nouveau produit", choices=["all_except_one", "new_one","all"], default="all")
#
#     args = parser.parse_args()
#
#     matching_products_with_threshold(args.path_input_files, args.url_one_product, args.threshold_value,args.method_chosen)
     





