#--------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- Lanceur chunking et création json -----------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

# Toutes les librairies utiles
# import pandas as pd
# import operator
# import numpy as np
# import re
# import itertools
# import datetime
# import argparse
# import os
import argparse
# import datetime
# import json
# import os

# Toutes les fonctions utiles
# from functions import fun_step_1_create_df as step_1
# from functions import fun_step_2_data_cleansing as step_2
# from functions import fun_step_3_ngrams as step_3
# from functions import fun_step_4_chunks as step_4
#
# from functions import fun_step_5_ngrams_overlapped_and_not_overlapped as step_5
# from functions import fun_step_6_get_preliminary_results as step_6
#
# from functions import fun_step_7_extract_upper_entities as step_7
# from functions import fun_step_8_extract_double_quotes_entities as step_8
#
# from functions import fun_step_9_entities_found_to_str as step_9
# from functions import fun_step_10_extract_combined_one_two_three_four_five_entities as step_10
#
# from functions import fun_step_11_couples_final as step_11
#
# # Toutes les fonctions
from functions import chunking_bio as chunking
from functions import extract_results_chunking_bio as extract_to_json
#
# # Option pour afficher entièrement le contenu des colonnes
# pd.set_option('display.max_colwidth',-1)


# Chemin des données source et chemin des données en sortie
# path_root = "/home/hapax94/Documents/vincent/jupyter"
# path_root = os.getcwd().replace("/carrefour_chunking_bio/scripts",'')
# path_output = "/carrefour_chunking_bio/output"

if __name__== "__main__":

    parser = argparse.ArgumentParser(description='test arguments')

    # 06/05/2019: on met en commentaires
    # plus besoin de ce paramètre pour un vrai fonctionnement en Prod
    # parser.add_argument("-pi", "--path_input_files", help="path input file", required=True)

    # 19/04/2019: pour permettre le lancement du cas "all", on met ce paramètre à None par défaut
    # parser.add_argument("-u", "--url_one_product", help="url du nouveau produit", required=True)
    parser.add_argument("-u", "--url_one_product", help="url du nouveau produit", default = None)
    # parser.add_argument("-s", "--threshold_value", help="seuil de similarité", type=float, required=True)
    parser.add_argument("-s", "--threshold_value", help="seuil de similarité", type=float, default = None)
    # parser.add_argument("-m", "--method_chosen", help="lancer pour tous les produits excepté un ou seulement pour le nouveau produit", choices=["all_except_one","new_one"], default="all_except_one")

    # 26/04/2019: ajout du paramètre "all_with_filter"
    # parser.add_argument("-m", "--method_chosen", help="lancer pour tous les produits excepté un ou seulement pour le nouveau produit", choices=["all_except_one", "new_one","all"], default="all")


    # 29/05/2019: les valeurs possibles sont simplement "all" et "new_one"
    # parser.add_argument("-m", "--method_chosen", help="lancer pour tous les produits excepté un ou seulement pour le nouveau produit", choices=["all_except_one", "new_one", "all","all_with_filter"], default="all")
    parser.add_argument("-m", "--method_chosen",help="lancer pour tous les produits excepté un ou seulement pour le nouveau produit", choices=["all", "new_one"], default="all")

    # 25/04/2019: ajout du 5ème paramètre "to_filter" par défaut à False
    # version plus simple car on n'a pas besoin pour l'instant de filtrer suivant une URL et un seuil
    # parser.add_argument('-tf', '--to_filter_bool', help="filtre authorisé pour étape 2", action='store_true')

    args = parser.parse_args()

    print ("ETAPE 1 : chunking en cours \n")

    # 26/04/2019 : on empeche le lancement du matching avec "all" en filtrant avec une URL

    # 29/05/2019: on peut utiliser "all" et filtrer suivant une URL
    if args.method_chosen == "all" and args.url_one_product != None:
        # print('La méthode "all" doit etre lancée avec une URL non renseignée')
        # print('Arret du script')
        # exit()
        print('La méthode "all" va etre lancée avec url_one_product = ', args.url_one_product)
        print("ATTENTION: le filtre utilisant cette URL sera utilisé seulement pour l'ETAPE 2 de création du .json \n")

    # 29/05/2019: les valeurs possibles sont simplement "all" et "new_one" et "all_with_filter" n'existe plus
    # On met en commentaires ci-dessous:
    # if args.method_chosen == "all_with_filter" and args.url_one_product != None:
    #     print('La méthode "all_with_filter" va etre lancée avec url_one_product = ',args.url_one_product)
    #     print("ATTENTION: le filtre utilisant cette URL sera utilisé seulement pour l'ETAPE 2 de création du .json \n")

    # 16/05/2019 : plus besoin de ce paramètre "path_input_files" pour un vrai fonctionnement en PROD
    # chunking.matching_products_with_threshold(args.path_input_files, args.url_one_product, args.threshold_value,args.method_chosen)
    chunking.matching_products_with_threshold(args.url_one_product, args.threshold_value,args.method_chosen)

    # 20/05/2019 : le cas "all_except_one", ne sert plus à rien
    # if args.method_chosen == "all_except_one":
    #     print('\n Pas de création des .json dans le cas "all_except_one" \n')

    # 26/04/2019: ajout du paramètre "all_with_filter"
    # elif  args.method_chosen == "new_one" or args.method_chosen == "all":

    # 20/05/2019 : le cas "all_except_one", ne sert plus à rien
    # elif args.method_chosen == "new_one" or args.method_chosen == "all" or args.method_chosen == "all_with_filter":

    # 29/05/2019 : on n'utilise plus "all_with_filter"
    # if args.method_chosen == "new_one" or args.method_chosen == "all" or args.method_chosen == "all_with_filter":
    if args.method_chosen == "new_one" or args.method_chosen == "all":
        print("\n ETAPE 2 : création des .json \n")
        # extract_to_json.extract_matched_products(args.path_input_files, args.url_one_product, args.threshold_value, args.method_chosen)

        # print("args.url_one_product", args.url_one_product)
        # print("args.threshold_value", args.threshold_value)
        # print("args.method_chosen", args.method_chosen)
        # print ("args.to_filter_bool", args.to_filter_bool)

        # version plus simple car on n'a pas besoin pour l'instant de filtrer suivant une URL et un seuil
        # extract_to_json.extract_matched_products(args.url_one_product, args.threshold_value, args.method_chosen, args.to_filter_bool)

        # 26/04/2019: ajout du paramètre "all_with_filter"
        # extract_to_json.extract_matched_products(args.method_chosen)
        extract_to_json.extract_matched_products(args.url_one_product, args.threshold_value, args.method_chosen)



