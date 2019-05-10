# A faire au début, pour utiliser "%autoreload" :
# %load_ext autoreload
# %autoreload


# Toutes les librairies utiles
import pandas as pd
# import operator

# import numpy as np
# import re

# import itertools

import datetime
import json

# # Toutes les fonctions utiles
# # from functions import fun_create_df_cleansing_titles_find_ngrams as fc
# # from functions import fun_create_df_find_ngrams as fc
# from functions import fun_step_1_create_df as step_1
# from functions import fun_step_2_data_cleansing as step_2
# from functions import fun_step_3_ngrams as step_3
# from functions import fun_step_4_chunks as step_4

# from functions import fun_step_5_ngrams_overlapped_and_not_overlapped as step_5
# from functions import fun_step_6_get_preliminary_results as step_6

# from functions import fun_step_7_extract_upper_entities as step_7
# from functions import fun_step_8_extract_double_quotes_entities as step_8

# from functions import fun_step_9_entities_found_to_str as step_9
# from functions import fun_step_10_extract_combined_one_two_three_four_five_entities as step_10

# from functions import fun_step_11_couples_final as step_11

# # Option pour afficher entièrement le contenu des colonnes
# pd.set_option('display.max_colwidth',-1)


# NB) On mettra en paramètres du script "main_chunking_bio.py" :

# - path_input_files
# - dict_one_product

# Chemin des données source et chemin des données en sortie
path_root = "/home/hapax94/Documents/vincent/jupyter"
# path_output = "/carrefour_chunking_bio/output/SCRIPT"
path_output = "/carrefour_chunking_bio/output"


# IL Y A 2 CAS :
#  1er cas : on sort dans un fichier .json ou .json + .xlsx les couples de produits
#  qui matchent avec l'URL du "nouveau produit".

#  Ces couples de produits sont :
# - obtenus lors de l'étape 1 de création des couples avec le script Python "main_chunking_bio.py"
# - présents dans le .pkl du répertoire : path_root + path_output + "/to_extract_new_one"
# - sous la forme : clé = URL, valeur = [[URL_1, distribu_1,score_1],[[URL_2, distrib_2,score_2],... ]

# 2ème cas: on sort dans un fichier .json ou .json + .xlsx la totalité des couples de produits
#  qui matchent.

# Ces couples de produits sont :
# - obtenus lors de l'étape 1 de création des couples avec le script Python "main_chunking_bio.py"
# - présents dans le .pkl du répertoire : path_root + path_output + "/to_extract_all"
# - sous la forme : clé = URL, valeur = [[URL_1, distribu_1,score_1],[[URL_2, distrib_2,score_2],... ]

# NB Le paramètre "method_chosen" permet de choisir le cas 1 ou le cas 2
# method_chosen = "extract_in_all_except_one"


# method_chosen = "all"
method_chosen = "new_one"

# NB Le paramètre "path_input_files" est à None pour les 2 cas

# 09/05/2019 : plus besoin de "path_input_files"
# path_input_files = None

# NB Le paramètre "url_one_product" vaut:
# - None pour le 1er cas
# - None ou est renseigné pour le 2ème cas, cf ci-dessous des valeurs d'URL

url_one_product = None
# url_one_product = "https://www.greenweez.com/lima-chips-aux-lentilles-original-90g-p83002"
# url_one_product = "https://www.greenweez.com/bio-planete-huile-d-olive-bio-vierge-extra-douce-1l-p71410"
# url_one_product = 'https://www.greenweez.com/babybio-bols-tendresse-de-legumes-riz-12-mois-2x200gr-p6877'

# NB Le paramètre "threshold_value" peut valoir:
# - None
# - etre renseigné
# dans les 2 cas

threshold_value = None
# threshold_value = 0.75

# NB Le paramètre "format_output_file" permet de choisir entre:
# - .json
# - .json et .xlsx
# pour le format du fichier de sortie

#-----------------------------------------------------------------------------------------------------------#
#-- On laisse la création des .xlsx dans le .py étape 1 ----------------------------------------------------#
#-- Et on crée les .json dane .py étape 2 ------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

# 21/04/2019 : Plus besoin de ce paramètre "format_output_file"
# format_output_file = "json"

# def main(path_input, dict_product, s):
# def main(path_input, url_product, threshold,  method, format_output):

# 09/05/2019 : plus besoin de "path_input"
# def main(path_input, url_product, threshold, method):
def main(url_product, threshold, method):

    # 17/04/2019 : ajout du cas, extraction suite au lancement pour "all"
    # if path_input == None and method == "extract_in_all_couples":

    # 09/05/2019 : plus besoin de "path_input"
    # if (path_input == None and method == "new_one") or (path_input == None and method == "all"):
    if method == "new_one" or method == "all":

        # Code python a ajouter qui permet d'extraire
        # que les produits qui matchent avec l'URL utilisé en paramètre d'entrée

        # Lecture du .pkl contenant tous les produits qui matchent
        if method == "new_one":
            print ("Création de all_products_matched avec new_one")
            all_products_matched = pd.read_pickle(path_root + path_output + "/to_extract_new_one/all_results_final_" + method + '.pkl')
        elif method == "all":
            print("Création de all_products_matched avec all")
            all_products_matched = pd.read_pickle(path_root + path_output + "/to_extract_all/all_results_final_" + method + '.pkl')

        if url_product != None:

            if threshold == None and url_product != None:
                # Sortie 1 = on extrait tous les couples
                # qui matchent avec l'URL en paramètre d'entrée

                # Filtre de tous les couples qui contiennent cet URL
                results_products_matched = all_products_matched[(all_products_matched['URL_one'] == url_product) | (all_products_matched['URL_two'] == url_product)]
                output_file_name = '/result_SCRIPT_PYCHARM_' + datetime.datetime.today().strftime("%Y%m%d") + '_for_url_one_product.json'
            elif threshold != None and url_product != None:
                # Sortie 2 = on extrait tous les couples
                # qui matchent avec l'URL en paramètre d'entrée

                # Filtre de tous les couples qui contiennent cet URL
                filter_all_products_matched = all_products_matched[all_products_matched['confidence_score'] >= threshold]

                results_products_matched = filter_all_products_matched[(filter_all_products_matched['URL_one'] == url_product) | (filter_all_products_matched['URL_two'] == url_product)]
                output_file_name = '/result_SCRIPT_PYCHARM_' + datetime.datetime.today().strftime("%Y%m%d") + '_for_url_one_product_' + str(threshold) + '.json'
                del filter_all_products_matched

            dict_result = {}
            dict_result[url_product] = []

            if results_products_matched.shape[0] != 0:
                for row in results_products_matched.itertuples():
                    if url_product == row.URL_one:
                        dict_result[url_product].append(row.URL_two)
                        dict_result[url_product].append(row.confidence_score)

                    elif url_product == row.URL_two:
                        dict_result[url_product].append(row.URL_one)
                        dict_result[url_product].append(row.confidence_score)

                with open(path_root + path_output + output_file_name, 'w') as file:
                    json.dump(dict_result, file, sort_keys=True, indent=4)
                del dict_result

            else:
                print("ATTENTION: aucun produit ne matche avec l'URL: ", url_product)

        else:
            # On crée un dictionnaire qui contient tous les sets de produits
            # qui matchent en utilisant comme clé "URL_one"
            # 24/04/2019 : ajout de ce cas
            if threshold == None:
                dict_result = {}
                nb_couples = 0

                for row in all_products_matched.itertuples():
                    if row.URL_one not in dict_result.keys():
                        dict_result[row.URL_one] = []
                        dict_result[row.URL_one].append(row.URL_two)
                        dict_result[row.URL_one].append(row.distributeur_two)
                        dict_result[row.URL_one].append(row.confidence_score)
                        nb_couples += 1
                    else:
                        #   print (row.URL_one,"présent déjà dans dict_result.keys()")
                        dict_result[row.URL_one].append(row.URL_two)
                        dict_result[row.URL_one].append(row.distributeur_two)
                        dict_result[row.URL_one].append(row.confidence_score)
                        nb_couples += 1

                print ("Création du .json")
                with open(path_root + path_output + '/result_SCRIPT_PYCHARM_' + datetime.datetime.today().strftime("%Y%m%d") + '_for_all_products_' + str(nb_couples) + '_couples.json','w') as file:
                    json.dump(dict_result, file, sort_keys=True, indent=4)
                del dict_result


            else:

                # Filtre de tous les couples
                results_products_matched = all_products_matched[all_products_matched['confidence_score'] >= threshold]

                dict_result = {}
                nb_couples = 0

                for row in results_products_matched.itertuples():

                    if row.URL_one not in dict_result.keys():
                        dict_result[row.URL_one] = []
                        dict_result[row.URL_one].append(row.URL_two)
                        dict_result[row.URL_one].append(row.distributeur_two)
                        dict_result[row.URL_one].append(row.confidence_score)
                        nb_couples += 1

                    else:

                        #   print (row.URL_one,"présent déjà dans dict_result.keys()")
                        dict_result[row.URL_one].append(row.URL_two)
                        dict_result[row.URL_one].append(row.distributeur_two)
                        dict_result[row.URL_one].append(row.confidence_score)
                        nb_couples += 1

                with open(path_root + path_output + '/result_SCRIPT_PYCHARM_' + datetime.datetime.today().strftime("%Y%m%d") + '_for_all_products_' + str(nb_couples) + '_couples_' + str(threshold) + '.json','w') as file:
                    json.dump(dict_result, file, sort_keys=True, indent=4)

                del dict_result

if __name__== "__main__":
    # main(path_input_files, dict_one_product, 0.75)
    # main(path_input_files, url_one_product, threshold_value,  method_chosen)

    # 21/04/2019 : Plus besoin de ce paramètre "format_output_file"
    # main(path_input_files, url_one_product, threshold_value, method_chosen, format_output_file)

    # 09/05/2019 : plus besoin de "path_input_files"
    # main(path_input_files, url_one_product, threshold_value, method_chosen)
    main(url_one_product, threshold_value, method_chosen)
     





