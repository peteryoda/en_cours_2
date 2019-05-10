import re
import unicodedata

import nltk
from nltk.tokenize import word_tokenize
import pandas as pd

import re

# 07/05/2019 
# data_folder = "/home/hapax94/Documents/vincent/jupyter/carrefour_bio/notebooks/data"
data_folder = "/home/hapax94/Documents/vincent/jupyter/carrefour_chunking_bio/data"

# UTILISEE
def cleansing_titles(my_str):
    
    # ATTENTION, on garde les majuscules pour le moment
    # On pourra les enlever, après avoir splitté les titres
#     my_str = (my_str.strip()).lower()
    
    # ATTENTION, cette fois on garde d'abord les '"'
#     my_str = my_str.replace('"','').replace(" ' ",'')
    my_str = my_str.replace(" ' ",'')
    
    my_str = my_str.replace("''",'')
    
    # Enlever les blancs inutiles
    my_str = re.sub(re.compile(r'\s+'), ' ',my_str)
    
    # 07/02/2019 : suppression des parenthèses
    my_str = my_str.replace("(",'')
    my_str = my_str.replace(")",'')
    
    # Enlever les accents
    my_str = unicodedata.normalize('NFD', my_str).encode('ascii', 'ignore').decode('ascii')
    
    return my_str

# UTILISEE
def remove_stopwords(x):

    df_all_stopwords_dedup_titles = pd.read_csv(data_folder + "/stopwords/all_stopwords_dedup_for_titles_without_letters_cleansed.csv", names=['word'])
    
    # 10/11/2018 : problème avec les "d'", extrait : "d'" et "''"
    # word_tokens = word_tokenize(x)
    word_tokens = x.split(' ')
#     print (word_tokens)

    filtered_liste = []
    
    for w in word_tokens:
        
        if w not in list(df_all_stopwords_dedup_titles['word']):
            filtered_liste.append(w)
    
    # On reconstitue le title
    filtered = ' '.join(filtered_liste)

    del filtered_liste
    
    return filtered

# UTILISEE
def remove_year(x):
    # 12/02/2018 : on enlève les années
    filtered = re.sub('\d{4}','',x)
          
    return(filtered.strip())

# UTILISEE
# 05/02/2019 : nouvelle fonction qui extrait les mots en majuscules
def split_words_uppercase(x): 
    resultat = []
#     for temp in [each.strip()for each in re.findall(r"(\s|^)\b[A-Z\s]+\b(\s|$)", x)]:
#     for each in re.findall(r"(\s|^)\b[A-Z\s]+\b(\s|$)", x):
    for each in re.findall(r"\b[A-Z(\s|\')]+\b", x):
#         print (each)

        if each.strip() != '' and each.strip() != "'" and each.strip() != "(" and each.strip() != ")":
            #   on vérifie si le caractère qui suit "each"
            #   est une minuscule dans ce cas on n'ajoute pas "each"
#             print (x[x.find(each)+len(each)].isupper())
            if x.find(each)+len(each) < len(x) and x[x.find(each)+len(each)].isupper():
#                 print ("Le caractère après" , each, "est", x[x.find(each)+len(each)])
                resultat.append(each.strip())
            elif x.find(each)+len(each) == len(x):
                resultat.append(each.strip())
        
    return resultat

# UTILISEE
# 29/01/2019 : nouvelle fonction qui extrait les entités qui sont entre guillemets
def split_words_guillemets(x):
    pattern_guillemets = r'(?<=\").+?(?=\")'
    resultat = [each.replace('"','') for each in re.findall(pattern_guillemets,x)]
    
    return resultat

# UTILISEE
# 29/01/2019: on se sert des entités trouvées grace aux fonctions "split_words_uppercase" et "split_words_guillemets"
# pour splitter les titres
def split_title(x):

    if x.find(' , ') > 0 :
        splitted_title = x.split(' , ')
    elif x.find(' : ') > 0 :
        splitted_title = x.split(' : ')
    elif x.find(' - ') > 0 :
        splitted_title = x.split(' - ')
    
    else:
         splitted_title = x
    
    return splitted_title

# def split_title_uppercase(df):
    
#     if df.title_splitted_uppercase != [] and df.title_without_stopwords.find(df.title_splitted_uppercase[0]) > 0 :
#         splitted_title = df.title_without_stopwords.split(df.title_splitted_uppercase[0])     
#     else:
#         splitted_title = df.title_without_stopwords
#     # A la fin, on ne garde que les éléments splittés différents de ''
#     resultat = [each for each in splitted_title if each != '']
    
#     return resultat
    
# def split_title_guillemets(df):
#     if df.title_splitted_guillemets != [] and each.find(df.title_splitted_guillemets[0]) > 0 :
#         splitted_title = each.replace('"','').split(df.title_splitted_guillemets[0])
#     else:
#         splitted_title = df.title_without_stopwords
#     # A la fin, on ne garde que les éléments splittés différents de ''
#     resultat = [each for each in splitted_title if each != '']
       
#     return resultat

# PAS UTILISEE
# def year_in_title(x):
#     pattern_year = re.compile('\d{4}')
#     year_extracted = pattern_year.findall(x)
#     return year_extracted

# UTILISEE
def remove_separateurs(my_str):    
    # On garde les tirets "-" car permet de récupérer les mots tels que 'savigny-les-beaune'
#     my_str = re.sub('\s*[-,:]\s*',' ',my_str)
    my_str = re.sub('\s*[,:]\s*',' ',my_str)
    return my_str

# UTILISEE
def remove_year(x):
    # 12/02/2018 : on enlève les années
    filtered = re.sub('\d{4}','',x)
          
    return filtered.strip()


# PAS UTILISEE
# Sert surtout pour enlever les "' " qui peuvent être présents 

# def cleansing_words(x):
#     cleansed_words = []
#     for each_word in x:
#         # On laisse .strip() par sécurité
#         cleansed_words.append(re.sub("^'\s",'',re.sub("\s'$",'',each_word.strip())))
#     return cleansed_words

# UTILISEE
def cleansing_words_after_split(x):
    cleansed_words = []
    for each_word in x:
        # On laisse .strip() par sécurité
        cleansed_words.append(re.sub("^'\s",'',re.sub("\s'$",'',each_word.strip().lower())))
    return cleansed_words

# UTILISEE QUE POUR LE VIN
# 22/03/2019 : ajout fonction spécifique au VIN 
# Concerne seulement les distributeurs "wac" et "mll"

# def regexp_point_manquant(x):
#     pattern_1 = "(?<=([a-z]|[A-Z]))\s\s(?=[A-Z])"
#     pattern_2 = "(?<=(Description))\s(?=[A-Z])"
#     pattern_3 = "(?<=(Le domaine))\s(?=[A-Z])"
    
#     replacement = ". "

#     resultat = re.sub(pattern_1,replacement,x)
#     resultat = re.sub(pattern_2,replacement,resultat)
#     resultat = re.sub(pattern_3,replacement,resultat)
    
#     return resultat

# UTILISEE QUE POUR LE VIN
# 22/03/2019 : ajout fonction spécifique au VIN 
# Concerne seulement les distributeurs "wac" et "mll"

# def specific_wac_mll(df): 
    
#     df['description_regexp'] = df['description'].map(regexp_point_manquant)
#     df = df.drop("description", axis =1)
#     df.rename(columns={'description_regexp': 'description'}, inplace=True)
    
#     return df