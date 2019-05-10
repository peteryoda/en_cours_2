def final_result(df):
    
    temp1 = []
    temp2 = []
    
#     print ("On traite : ",df['slug'])
    
    if df['keep_overlapped_entity_X_phrases'] != []:
        if df['keep_overlapped_entity_X_phrases'][0] not in temp1:
            temp1.append(df['keep_overlapped_entity_X_phrases'][0])
     
    if  df['not_overlapped_entity_X_phrases'] != []:
        if temp1 != []:   
            for each in df['not_overlapped_entity_X_phrases']:
#                 print ("each:",each)
#                 print ("temp1",temp1)

                if each == temp1[0]:
                    resultat = df['not_overlapped_entity_X_phrases']
                else:
                    temp2.append(each)

                    temp2.append(temp1[0])
                    resultat = temp2

        else:
            resultat = df['not_overlapped_entity_X_phrases']
    else :
        resultat = df['keep_overlapped_entity_X_phrases']
        
    del temp1, temp2
    
    return resultat

import re
def difference_title_vs_final_result_X_phrases(df):
    temp = df['title'].strip()
    for each in df['final_result_X_phrases']:
        if each in temp:
#             print ("title: ", df['title'])
#             print ("each: ",each)
            # Si on trouve each au début du titre ou si on trouve each à la fin du titre
#             print(exec("'"+"^" + each + "'"))
            if re.search('^' + each , temp):
#                 print ("au début !", each)
                temp = re.sub(each,'',temp).strip()
            elif re.search(each + '$', temp):
#                 print ("en fin !", each)
                temp = re.sub(each,'',temp).strip()
#             print ("temp :",temp,"\n")
            else:
#                 print ("au milieu !", each)
                temp = re.sub(each,'-',temp).strip()
                
#         print ("\n")
            
    resultat = temp
    return resultat

import nltk
from nltk.tokenize import word_tokenize

def add_entity_1_grams(df):
    
    resultat = []
    
    # if df['difference_title_vs_final_result_X_phrases'] != '' and len(word_tokenize(df['difference_title_vs_final_result_X_phrases'])) == 1:
    if df['difference_title_vs_final_result_X_phrases'] != '' and len(df['difference_title_vs_final_result_X_phrases'].split(' ')) == 1:
        for each in df['final_result_X_phrases']:
#             print (each)
            resultat.append(each)
        resultat.append(df['difference_title_vs_final_result_X_phrases'])
    elif df['difference_title_vs_final_result_X_phrases'] == '': 
        for each in df['final_result_X_phrases']:
            resultat.append(each)
    # elif len(word_tokenize(df['difference_title_vs_final_result_X_phrases'])) > 1:
    elif len(df['difference_title_vs_final_result_X_phrases'].split(' '))> 1:
        # if '-' not in word_tokenize(df['difference_title_vs_final_result_X_phrases']):
        if '-' not in df['difference_title_vs_final_result_X_phrases'].split(' '):
            for each in df['final_result_X_phrases']:
#                 print (each)
                resultat.append(each)
                
        else:
            for each in df['final_result_X_phrases']:
#                 print (each)
                resultat.append(each)
            # for each in word_tokenize(df['difference_title_vs_final_result_X_phrases']):
            for each in df['difference_title_vs_final_result_X_phrases'].split(' '):
                if each != '-':  
                    resultat.append(each)
    
        
    return resultat

def remove_year_to_liste(x):
    
    resultat = []
    for each_entity in x:
        filtered = re.sub('\d{4}','',each_entity)
        if filtered == each_entity:
            resultat.append(each_entity)
          
    return resultat

import numpy as np
def error_estimation(df):
    count = 0
    for entity_truth in df['label_new_with_entity_clean_without_year']:
        for entity_found in df['final_result_X_phrases']:
            if entity_truth == entity_found:
                count += 1
    resultat = round(count/len(df['label_new_with_entity_clean_without_year'])*100,2)

    return resultat

# Fonction pour calculer le nombre de vins retrouvés à hauteur de X %
def number_of_wines_predicted(df,X):

    resultat = (len(df[df['%_entités_trouvées_1'] >= X])/len(df))*100
    return resultat

# Fonction pour calculer le nombre de vins retrouvés à hauteur de X %
def number_of_wines_predicted_2(df,X):
    resultat = (len(df[df['%_entités_trouvées_2'] >= X])/len(df))*100
    return resultat

import numpy as np
def error_estimation_2(df):
    count = 0
    for entity_truth in df['label_new_with_entity_clean_without_year']:
        for entity_found in df['final_result_X_phrases_bis']:
            if entity_truth == entity_found:
                count += 1
    resultat = round(count/len(df['label_new_with_entity_clean_without_year'])*100,2)

    return resultat

