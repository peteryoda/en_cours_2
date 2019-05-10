import pandas as pd

#-------------------------------------------------------------------------------------------------------------------------#
# ------------------ 1. Fonction import des dataframes à partir des fichiers source .csv ---------------------------------#
#-------------------------------------------------------------------------------------------------------------------------#

def create_df(name_df, path, encoding_value):

    # dict_of_dfs est un dictionnaire pour stocker tous les dataframes
    # dict_of_dfs = dict()
    
    # path = '/home/hapax94/Documents/vincent/fichiers_générés_par_Hervé_181217/wac_181217/wac/'

    # 10/05/2019 : on doit définir automatiquement les "name_df" = noms des fichiers .csv
    # présents dans le répertoire "path"


    all_file = path + name_df + '.csv'

    liste_tuples = []
    
    idx_last_slash = all_file.rfind("/") + 1
    idx_dot = all_file.index(".")
    name_file = all_file[idx_last_slash:idx_dot]

    # print ("name_file:",name_file)

    # On prend la dernière partie après le dernier "_"
    which_file = name_file.split('_')[-1]

    # print("name_file", name_file)
    which_type = name_file.split('_')[0]
    
    # print ("which_file", which_file)
    
    if  which_file == 'descriptions' and which_type == 'wine':
    	# 12/02/2017 : on appelle "label" plutot "title"
        # list_of_columns = ['slug','fil_ariane','label','url', 'description','image_url']
        if name_file == 'wine_figaro_descriptions':
            list_of_columns = ['description']
        else:    
            list_of_columns = ['slug','fil_ariane','title','url', 'description','image_url']
        
    elif which_file == 'descriptions' and which_type == 'smart':
        list_of_columns = ['slug','rayon0','rayon1','rayon2','title','description']
    elif which_file == 'properties' and which_type == 'wine':
        # ATTENTION ! ajout de last_col pour pouvoir charger le fichier 
#         list_of_columns = ['label','not_relevant_index','property', 'property_label']
        list_of_columns = ['slug','not_relevant_index','property', 'property_label','last_col']
        # print ("list_of_columns:",list_of_columns)
    
    elif which_file == 'categories' and which_type == 'wine':
        list_of_columns = ['slug','category','count','description', 'fil_ariane','category_url']
        
    elif which_file == 'variants' and which_type == 'wine':
        # "xslug|xnum|xtype|xoption|xprice|xavailability|xend_date|xper_price|xcro_price|xloy_price"
        list_of_columns = ['slug','not_relevant_index','type','option', 
                           'price','availability','end_date','price_per_unit','cro_price','loy_price']
    # 09/01/2018 : ajout cas fichier "footprints"
    elif which_file == 'footprints' and which_type == 'wine':
        # list_of_columns = ['slug', 'distributeur', 'label', 'option', 'price', 'cro_price', 'url','undefined','region', 'appellation', 'millesime', 'color', 'size', 'image_url']
        list_of_columns = ['slug', 'distributeur', 'title', 'option', 'price', 'cro_price', 'url','undefined','region', 
                           'appellation', 'millesime', 'color', 'size', 'image_url']

    # 23/01/2019 : données "Bio"
    elif which_type == 'orgc':
        
        if  which_file == 'category':
            list_of_columns = ['xid','xbreadcrumb','xtitle','xslug', 'xcount','xdescription','xmeta_title','xmeta_description', 'xmeta_keywords', 'xapi', 'xweb', 'xcrawled_at', 'xurl', 'xrun']
        
        elif which_file == 'offer':
            list_of_columns = ['xid','xnum','xoffer_num','xbrand','xtitle','xvariant','xseller','xprice','xstock','xgtin','xsku','xquality','xshipping','xpromo','xpremium','xextra_price','xentry_price','xbest_offer','xbest_price','xfull_price','xunit_pricing','xseller','xslug','ximg','xbreadcrumb','xsubtitle','xprize','xgrade','xgrades','xcustom1','xcustom2','xcustom3','xcustom4','xcustom5','xcustom6','xcustom7','xcustom8','xapi','xweb','xcrawled_at','xurl','xrun']

        elif which_file == 'product':
            list_of_columns = ['xid','xtitle','xbrand','xbreadcrumb','xsubtitle','xdescription','xslug','ximg','xmeta_title','xmeta_description','xmeta_keywords','xapi','xweb','xcrawled_at','xurl','xrun']

    liste_tuples = []
    file = open(all_file, 'r',encoding=encoding_value) 

    # print ("which_type", which_type)
    if which_type == 'wine':
        line_number = 0
    elif which_type == 'smart':
        line_number = 1
    elif which_type == 'orgc':
        line_number = 0

    for line in file:
        line_number = line_number + 1
        if (line_number == 1 and which_type == 'wine') or (line_number == 2 and which_type == 'smart'):
            nb_sep = line.count('\t')

            # print("Nb de séparateurs tabulation sur la 1ère ligne: ",nb_sep)
         
        # 09/05/2019: ATTENTION, on distingue si une fin de ligne se termine
#         par '\t\n' ou bien simplement par '\n'
#         line_without_eof = line.replace('\t\n','')
        if '\t\n' in line:
            line_without_eof = line.replace('\t\n','')
        elif '\n' in line:
            line_without_eof = line.replace('\n','')
           
        line_splitted = line_without_eof.split('\t')

        # if line_number == 2:
        #     print("line_without_eof", line_without_eof)
        #     print("line_splitted", line_splitted)
        
        if (line_number == 1 and which_type == 'wine') or (line_number == 2 and which_type == 'smart'):
            print(line_splitted)
            # 10/01/2018 pour les fichiers Pricing 
            # print("Nb de champs sur la 1ère ligne: ",nb_sep - 1)

            # print("Nb de champs sur la 1ère ligne: ",nb_sep)
        
        if (line_number >= 1 and which_type == 'wine') or (line_number >= 3 and which_type == 'smart'):
            liste_tuples.append(line_splitted)

        # 23/01/2019 : pour les données "Bio", les fichiers contiennent les noms des colonnes
        # donc la lecture des fichiers ne commencent qu'à la 2ème ligne
        if which_type == 'orgc' and line_number != 1:
            
            # if line_number == 2:
            #     print(line_splitted)
            
            liste_tuples.append(line_splitted)
        
#         if line_number == 1:
#             print("Données de la 1ère ligne pour", name_df, " : ", liste_tuples)
        
    # Enfin on transforme la liste en dataframe grâce à item tuples

    # print ("liste_tuples", liste_tuples)
    df_out = pd.DataFrame.from_records(liste_tuples,columns = list_of_columns)
    #dict_of_dfs[name_df] = temp_df

    file.close() 

    #return(dict_of_dfs[name_df])
    return df_out


