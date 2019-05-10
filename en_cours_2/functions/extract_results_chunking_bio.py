# A faire au début, pour utiliser "%autoreload" :
# %load_ext autoreload
# %autoreload


# Toutes les librairies utiles
import pandas as pd
import argparse
import datetime
import json
import os

# Chemin des données source et chemin des données en sortie
# path_root = "/home/hapax94/Documents/vincent/jupyter"
# path_output = "/carrefour_bio/output/SCRIPT"

path_root = os.getcwd().replace("/carrefour_chunking_bio/scripts",'')
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
# method_chosen = "new_one"
# method_chosen = "all"

# NB Le paramètre "path_input_files" est à None pour les 2 cas
# path_input_files = None

# NB Le paramètre "url_one_product" vaut:
# - None pour le 1er cas
# - None ou est renseigné pour le 2ème cas, cf ci-dessous des valeurs d'URL

# url_one_product = None
# url_one_product = "https://www.greenweez.com/lima-chips-aux-lentilles-original-90g-p83002"
# url_one_product = "https://www.greenweez.com/bio-planete-huile-d-olive-bio-vierge-extra-douce-1l-p71410"
# url_one_product = 'https://www.greenweez.com/babybio-bols-tendresse-de-legumes-riz-12-mois-2x200gr-p6877'

# NB Le paramètre "threshold_value" peut valoir:
# - None
# - etre renseigné
# dans le 2 cas

# threshold_value = None
# threshold_value = 0.75

# NB Le paramètre "format_output_file" permet de choisir entre:
# - .json
# - .json et .xlsx
# pour le format du fichier de sortie

# 21/04/2019 : Plus besoin de ce paramètre "format_output_file"
# format_output_file = "json"

#-----------------------------------------------------------------------------------------------------------#
#-- On laisse la création des .xlsx dans le .py étape 1 ----------------------------------------------------#
#-- Et on crée les .json dane .py étape 2 ------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

# def main(path_input, dict_product, s):
# def extract_matched_products(path_input, url_product, threshold,  method, format_output):

# 25/04/2019: ajout du 5ème paramètre "to_filter" par défaut à False
# def extract_matched_products(path_input, url_product, threshold, method):

# version plus simple car on n'a pas besoin pour l'instant de filtrer suivant une URL et un seuil
# def extract_matched_products(url_product, threshold, method, to_filter):

# 26/04/2019: ajout du paramètre "all_with_filter"
# def extract_matched_products(method):
def extract_matched_products(url_product, threshold, method):

    # 17/04/2019 : ajout du cas, extraction suite au lancement pour "all"
    # if path_input == None and method == "extract_in_all_couples":
    # if (path_input == None and method == "new_one") or (path_input == None and method == "all"):
    if method == "new_one" or method == "all":

        # Code python a ajouter qui permet d'extraire
        # que les produits qui matchent avec l'URL utilisé en paramètre d'entrée

        # Lecture du .pkl contenant tous les produits qui matchent
        if method == "new_one":
            all_products_matched = pd.read_pickle(path_root + path_output + "/to_extract_new_one/all_results_final_" + method + '.pkl')
        elif method== "all":
            all_products_matched = pd.read_pickle(path_root + path_output + "/to_extract_all/all_results_final_" + method + '.pkl')

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
        with open(path_root + path_output + '/result_' + datetime.datetime.today().strftime("%Y%m%d") + '_' + method + '_' + str(nb_couples) + '_couples.json','w') as file:
            json.dump(dict_result, file, sort_keys=True, indent=4)
        del dict_result

    # 26/04/2019: ajout du paramètre "all_with_filter"
    if method == "all_with_filter":
        all_products_matched = pd.read_pickle(path_root + path_output + "/to_extract_all/all_results_final_" + method + '.pkl')

        if threshold != None and url_product == None:
            # Filtre de tous les couples suivant le seuil
            results_products_matched = all_products_matched[all_products_matched['confidence_score'] >= threshold]

        elif threshold == None and url_product != None:
             # Filtre de tous les couples qui contiennent cet URL
            results_products_matched = all_products_matched[(all_products_matched['URL_one'] == url_product) | (all_products_matched['URL_two'] == url_product)]

        elif threshold != None and url_product != None:

            # Filtre de tous les couples d'abord suivant le seuil
            filter_all_products_matched = all_products_matched[all_products_matched['confidence_score'] >= threshold]
            # Filtre de tous les couples suivant l'URL
            results_products_matched = filter_all_products_matched[(filter_all_products_matched['URL_one'] == url_product) | (filter_all_products_matched['URL_two'] == url_product)]

            del filter_all_products_matched

        # print("On passe ici avant .json")
        dict_result = {}
        nb_couples = 0

        if results_products_matched.shape[0] != 0:
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
            # with open(path_root + path_output + '/result_' + datetime.datetime.today().strftime("%Y%m%d") + '_for_all_products_' + str(nb_couples) + '_couples.json', 'w') as file:
            if threshold != None and url_product == None:
                output_file_name = '/result_' + datetime.datetime.today().strftime("%Y%m%d") + '_' + method + '_for_threshold_' + str(threshold)  + '_' + str(nb_couples) + '_couples.json'
            elif threshold == None and url_product != None:
                output_file_name = '/result_' + datetime.datetime.today().strftime("%Y%m%d") + '_' + method + '_for_url_one_product_' + str(nb_couples) + '_couples.json'
            elif threshold != None and url_product != None:
                output_file_name = '/result_' + datetime.datetime.today().strftime("%Y%m%d") + '_' + method + '_for_url_one_product_and_threshold_' + str(threshold) + '_' + str(nb_couples) + '_couples.json'
            with open(path_root + path_output + output_file_name, 'w') as file:
                json.dump(dict_result, file, sort_keys=True, indent=4)
            del dict_result

# if __name__== "__main__":
#     # main(path_input_files, dict_one_product, 0.75)
#     # main(path_input_files, url_one_product, threshold_value,  method_chosen)
#
#     parser = argparse.ArgumentParser(description='test arguments')
#     # parser.add_argument("-pi", "--path_input_files", help="path input file", required=True)
#     parser.add_argument("-pi", "--path_input_files", help="path input file", default=None)
#     # 19/04/2019: pour permettre le lancement du cas "all", on met ce paramètre à None par défaut
#     # parser.add_argument("-u", "--url_one_product", help="url du nouveau produit", required=True)
#     parser.add_argument("-u", "--url_one_product", help="url du nouveau produit", default=None)
#     # parser.add_argument("-s", "--threshold_value", help="seuil de similarité", type=float, required=True)
#     parser.add_argument("-s", "--threshold_value", help="seuil de similarité", type=float, default=None)
#     # parser.add_argument("-m", "--method_chosen", help="lancer pour tous les produits excepté un ou seulement pour le nouveau produit", choices=["all_except_one","new_one"], default="all_except_one")
#     parser.add_argument("-m", "--method_chosen", help="lancer pour tous les produits excepté un ou seulement pour le nouveau produit", choices=["all_except_one", "new_one", "all"], default="all")
#     # Non finalement on sort par défaut un fichier de sortie .json
#
#     # 21/04/2019 : Plus besoin de ce paramètre "format_output_file"
#     # parser.add_argument("-f", "--format_output_file", help="json or both json + xlsx", choices=["json", "json_and_xlsx"], default="json")
#
#     args = parser.parse_args()
#
#    # extract_matched_products(args.path_input_files, args.url_one_product, args.threshold_value, args.method_chosen,args.format_output_file)
#     extract_matched_products(args.path_input_files, args.url_one_product, args.threshold_value, args.method_chosen)
     





