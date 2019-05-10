# import pandas as pd

# import re
# import unicodedata

# Pour extraire les "chunks" 
from pattern.fr import parsetree

#-----------------------------------------------------------------------------------------------------------------------------#
# ------------------------------ Fonction qui extrait les n grams ------------------------------------------------------------#
# --------------------------- * Input *: un texte et un paramètre n ----------------------------------------------------------#
#---------------------------- * Output *: les n grams ------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------#

# import nltk
# from nltk.tokenize import word_tokenize

# def find_ngrams(input_list,ngrams_indice):
        
#     ngram_list = []
#     ngrams_indice = ngrams_indice - 1
#     print (input_list)
#     # print ("word_tokenize(input_list)",word_tokenize(input_list))
#     for i in range(len(word_tokenize(input_list)) - ngrams_indice):
#         to_append = ''
# #         print ("valeur de i:",i)
#         for k in range(ngrams_indice + 1):
# #             print("valeur de k:",k)
#             if k < ngrams_indice: 
#                 to_append = to_append + word_tokenize(input_list)[i+k]  + " "
#             else:
# #                 print ('to_append: ',to_append)
#                 to_append = to_append + word_tokenize(input_list)[i+k]

#         ngram_list.append((to_append))
    
#     return ngram_list

# UTILISEE

def find_ngrams(input_list,ngrams_indice):
        
    ngram_list = []
    ngrams_indice = ngrams_indice - 1
    
    for i in range(len(input_list)-ngrams_indice):
        to_append = ''
#         print ("valeur de i:",i)
        
        for k in range(ngrams_indice + 1):
#             print("valeur de k:",k)
            if k < ngrams_indice:
                
                to_append = to_append + input_list[i+k]  + " "
            else:
#                 print ('to_append: ',to_append)
                to_append = to_append + input_list[i+k]

        ngram_list.append((to_append))
    
    return(ngram_list)
