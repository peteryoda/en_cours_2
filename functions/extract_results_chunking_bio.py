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


# method_chosen = "all"
# method_chosen = "new_one"

# NB Le paramètre "path_input_files" est à None pour les 2 cas

# 09/05/2019 : plus besoin de "path_input_files"
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
# dans les 2 cas

# threshold_value = None
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
# def extract_matched_products(path_input, url_product, threshold,  method, format_output):

# 25/04/2019: ajout du 5ème paramètre "to_filter" par défaut à False
# def extract_matched_products(path_input, url_product, threshold, method):

# 26/04/2019: ajout du paramètre "all_with_filter"
# def extract_matched_products(method):
def extract_matched_products(url_product, threshold, method):

    # 17/04/2019 : ajout du cas, extraction suite au lancement pour "all"
    # if path_input == None and method == "extract_in_all_couples":
    # 09/05/2019 : plus besoin de "path_input"
    # if (path_input == None and method == "new_one") or (path_input == None and method == "all"):
    if method == "new_one" or method == "all":

        # Code python a ajouter qui permet d'extraire
        # que les produits qui matchent avec l'URL utilisé en paramètre d'entrée

        # Lecture du .pkl contenant tous les produits qui matchent
        if method == "new_one":
            if threshold != None:
                print("Création de all_products_matched avec new_one et avec threshold égal à ", str(threshold))
                all_products_matched = pd.read_pickle(path_root + path_output + "/to_extract_new_one/all_results_final_" + method + '_' + str(threshold) + '.pkl')
            else:
                print ("Création de all_products_matched avec new_one")
                all_products_matched = pd.read_pickle(path_root + path_output + "/to_extract_new_one/all_results_final_" + method + '.pkl')

        elif method == "all":
            print("Création de all_products_matched avec all")
            all_products_matched = pd.read_pickle(path_root + path_output + "/to_extract_all/all_results_final_" + method + '.pkl')

        # 24/05/2019: on enlève la possibilité de filtrer suivant le threshold, car on peut filtrer dejà avec le threshold dans le .py de la 1ère partie

        # - pour "all", on laisse la possibilité de filtrer suivant une URL (remplace la fonctionnalité "all_with_filter")
        # - pour "new_one", on enlève la possibilité de filtrer suivant une URL

        # 28/05/2019: filtrer avec une URL ne concerne que le cas "all" (ancien "all_with_filter")
        if url_product != None:

            # if threshold == None and url_product != None:
            if method == "all":

                # Sortie 1 = on extrait tous les couples
                # qui matchent avec l'URL en paramètre d'entrée

                # Filtre de tous les couples qui contiennent cet URL
                results_products_matched = all_products_matched[(all_products_matched['URL_one'] == url_product) | (all_products_matched['URL_two'] == url_product)]
                # output_file_name = '/result_' + datetime.datetime.today().strftime("%Y%m%d") + '_for_url_one_product.json'
                # output_file_name = '/result_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + '_' + method + '_for_url_one_product.json'
                # 27/05/2019: noms des fichiers .json tenant compte de "method" et "threshold"
                if threshold != None:
                    output_file_name = '/result_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + '_' + method + '_' + str(threshold) + '_for_url_one_product.json'
                else:
                    output_file_name = '/result_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + method + '_for_url_one_product.json'

            # 28/05/2019: cette condition change avec :
            # elif threshold != None and url_product != None:
            # elif method == "new_one":
            #
            #     # Sortie 2 = on extrait tous les couples
            #     # qui matchent avec l'URL en paramètre d'entrée

            #     # Filtre de tous les couples qui contiennent cet URL
            #     # 24/05/2019 : pour "new_one", on enlève la possibilité de filtrer suivant le threshold, car on peut filtrer dejà avec le threshold dans le .py de la 1ère partie
            #     filter_all_products_matched = all_products_matched[all_products_matched['confidence_score'] >= threshold]

            #     results_products_matched = filter_all_products_matched[(filter_all_products_matched['URL_one'] == url_product) | (filter_all_products_matched['URL_two'] == url_product)]
            #     results_products_matched = all_products_matched[(all_products_matched['URL_one'] == url_product) | (all_products_matched['URL_two'] == url_product)]
            #     # output_file_name = '/result_' + datetime.datetime.today().strftime("%Y%m%d") + '_for_url_one_product_' + str(threshold) + '.json'
            #     output_file_name = '/result_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + _for_url_one_product_' + str(threshold) + '.json'
            #     del filter_all_products_matched

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

            # 24/05/2019 : pour "new_one", on enlève la possibilité de filtrer suivant le threshold, car on peut filtrer dejà avec le threshold dans le .py de la 1ère partie

            # On crée un dictionnaire qui contient tous les sets de produits
            # qui matchent en utilisant comme clé "URL_one"
            # 24/04/2019 : ajout de ce cas

            # if threshold == None:
            #     dict_result = {}
            #     nb_couples = 0

            #     for row in all_products_matched.itertuples():
            #         if row.URL_one not in dict_result.keys():
            #             dict_result[row.URL_one] = []
            #             dict_result[row.URL_one].append(row.URL_two)
            #             dict_result[row.URL_one].append(row.distributeur_two)
            #             dict_result[row.URL_one].append(row.confidence_score)
            #             nb_couples += 1
            #         else:
            #             #   print (row.URL_one,"présent déjà dans dict_result.keys()")
            #             dict_result[row.URL_one].append(row.URL_two)
            #             dict_result[row.URL_one].append(row.distributeur_two)
            #             dict_result[row.URL_one].append(row.confidence_score)
            #             nb_couples += 1

            #     print("Création du .json")
            #     # with open(path_root + path_output + '/result_' + datetime.datetime.today().strftime("%Y%m%d") + '_for_all_products_' + str(nb_couples) + '_couples.json', 'w') as file:
            #     with open(path_root + path_output + '/result_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + '_' +  method + '_' +  str(nb_couples) + '_couples.json', 'w') as file:
            #         json.dump(dict_result, file, sort_keys=True, indent=4)
            #     del dict_result


            # else:

            #     # Filtre de tous les couples
            #     results_products_matched = all_products_matched[all_products_matched['confidence_score'] >= threshold]

            #     dict_result = {}
            #     nb_couples = 0

            #     for row in results_products_matched.itertuples():

            #         if row.URL_one not in dict_result.keys():
            #             dict_result[row.URL_one] = []
            #             dict_result[row.URL_one].append(row.URL_two)
            #             dict_result[row.URL_one].append(row.distributeur_two)
            #             dict_result[row.URL_one].append(row.confidence_score)
            #             nb_couples += 1

            #         else:

            #             #   print (row.URL_one,"présent déjà dans dict_result.keys()")
            #             dict_result[row.URL_one].append(row.URL_two)
            #             dict_result[row.URL_one].append(row.distributeur_two)
            #             dict_result[row.URL_one].append(row.confidence_score)
            #             nb_couples += 1

            #     # with open(path_root + path_output + '/result_' + datetime.datetime.today().strftime("%Y%m%d") + '_for_all_products_' + str(nb_couples) + '_couples_' + str(threshold) + '.json','w') as file:
            #     with open(path_root + path_output + '/result_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + '_' +  method + '_' +  str(nb_couples) + '_couples_' + str(threshold) + '.json','w') as file:
            #         json.dump(dict_result, file, sort_keys=True, indent=4)

            #     del dict_result

            # 24/05/2019 : pour "new_one", on enlève la possibilité de filtrer suivant le threshold, car on peut filtrer dejà avec le threshold dans le .py de la 1ère partie
            ###### NOUVEAU CODE ##########

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

            print("Création du .json")

            # with open(path_root + path_output + '/result_SCRIPT_PYCHARM_' + datetime.datetime.today().strftime("%Y%m%d") + '_for_all_products_' + str(nb_couples) + '_couples.json','w') as file:

            # 27/05/2019: noms des fichiers .json tenant compte de "method" et "threshold"
            if threshold != None:
                output_file_name = '/result_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + '_' + method + '_' + str(threshold) + '_' + str(nb_couples) + '_couples.json'
            else:
                output_file_name = '/result_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + '_' + method + '_' + str(nb_couples) + '_couples.json'

            # with open(path_root + path_output + '/result_SCRIPT_PYCHARM_' + datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + '_for_all_products_' + str(nb_couples) + '_couples.json', 'w') as file:
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
     





