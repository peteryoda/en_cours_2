# def all_ngrams_X_phrases(df):
    
# # 04/10/2018 ATTENTION: on dirait qu'utiliser les 1-grams est utile pour les smartphones
#     all_ngrams_X_phrases = []
    
#     # 24/03/2019 : on ajoute un test d'existence de la colonne 'entity_X_phrases_1_grams_found'
#     # SERT SEULEMENT POUR LES SMARTPHONES ET LE BIO ,  
# #     if  'entity_X_phrases_1_grams_found' in list(df) and type(df['entity_X_phrases_1_grams_found']) == list:
#     if type(df['entity_X_phrases_1_grams_found']) == list:
#         for each in df['entity_X_phrases_1_grams_found']:
#             all_ngrams_X_phrases.append(each)
#     # SERT SEULEMENT POUR LES SMARTPHONES ET LE BIO ?
#     if type(df['entity_X_phrases_2_grams_found']) == list:
#         for each in df['entity_X_phrases_2_grams_found']:
#             all_ngrams_X_phrases.append(each)
#     if type(df['entity_X_phrases_3_grams_found']) == list:
#         for each in df['entity_X_phrases_3_grams_found']:
#             all_ngrams_X_phrases.append(each)
#     if type(df['entity_X_phrases_4_grams_found']) == list:
#         for each in df['entity_X_phrases_4_grams_found']:
#             all_ngrams_X_phrases.append(each)
    
#     return all_ngrams_X_phrases

def all_ngrams_X_phrases(df):
    
# 04/10/2018 ATTENTION: on dirait qu'utiliser les 1-grams est utile pour les smartphones
    all_ngrams_X_phrases = []
    
    # 24/03/2019 : on ajoute un test d'existence de la colonne 'entity_X_phrases_1_grams_found'
    # SERT SEULEMENT POUR LES SMARTPHONES ET LE BIO ,  
#     if  'entity_X_phrases_1_grams_found' in list(df) and type(df['entity_X_phrases_1_grams_found']) == list:
    try:
        if type(df['entity_X_phrases_1_grams_found']) == list:
            for each in df['entity_X_phrases_1_grams_found']:
                all_ngrams_X_phrases.append(each)
    except:
        # print ("Colonne entity_X_phrases_1_grams_found absente dans", df)
        print("Pas d'entité 1-grams trouvée dans ", df['id'])
    # SERT SEULEMENT POUR LES SMARTPHONES ET LE BIO ?
    try: 
        if type(df['entity_X_phrases_2_grams_found']) == list:
            for each in df['entity_X_phrases_2_grams_found']:
                all_ngrams_X_phrases.append(each)
    except:
        # print ("Colonne entity_X_phrases_2_grams_found absente dans", df)
        print("Pas d'entité 2-grams trouvée dans ", df['id'])
        
    try:
        if type(df['entity_X_phrases_3_grams_found']) == list:
            for each in df['entity_X_phrases_3_grams_found']:
                all_ngrams_X_phrases.append(each)
    except:
        # print ("Colonne entity_X_phrases_3_grams_found absente dans", df)
        print("Pas d'entité 3-grams trouvée dans ", df['id'])
        
    try:
        if type(df['entity_X_phrases_4_grams_found']) == list:
            for each in df['entity_X_phrases_4_grams_found']:
                all_ngrams_X_phrases.append(each)
    except:
        # print ("Colonne entity_X_phrases_4_grams_found absente dans", df)
        print("Pas d'entité 4-grams trouvée dans ", df['id'])


    
    return all_ngrams_X_phrases

import nltk
from nltk.tokenize import word_tokenize

# test = [['brasserie', 38, '1_grams'], ['33cl', 16, '1_grams'], ['red', 5, '1_grams'], ['delirium', 4, '1_grams'], ['huyghe', 3, '1_grams'], ['33cl brasserie', 4, '2_grams']]
# test = [['brasserie', 38, '1_grams'], ['33cl', 16, '1_grams'], ['red', 5, '1_grams'], ['delirium', 4, '1_grams'], ['huyghe', 3, '1_grams']]
# test = [["bouchard pere & fils", 87, "4_grams"], ["clos vougeot grand cru", 34, "4_grams"], ["& fils clos vougeot", 11, "4_grams"], ["fils clos vougeot grand", 11, "4_grams"], ["pere & fils clos", 11, "4_grams"]]
# test = [["beaune 1er cru clos", 22, "4_grams"], ["1er cru clos roi", 8, "4_grams"], ["domaine chanson pere fils", 7, "4_grams"]]
def not_overlap_ngrams(x):
    ngrams_with_no_overlap = []
    
    if len(x) > 1:
        for i in range(len(x)):

            if len(x) > 1:
                # 10/11/2018
                # words_i = word_tokenize(x[i])
                words_i = x[i].split(' ')
                # print (words_i)

                cpt_no_overlap = 0
                for j in range(len(x)):

                    if j!=i :
        #                 print ("\n Un autre ngram est :",x[j][0])
                        words_j = word_tokenize(x[j])
        #                 print (words_j)
                        intersection_words_i_j = [x for x in words_i if x in set(words_j)]

                        # Si aucun mot n'est en commun => on incrémente un compteur
                        if intersection_words_i_j == []:
        #                     print ("Aucun mot en commun !")
                            cpt_no_overlap += 1
        #                     print ("La valeur de cpt est : ",cpt_no_overlap)
        #                     print ("La valeur à atteindre est :",len(x) - 1)
                            if cpt_no_overlap == len(x) - 1:
                            # Le ngram concerné ne s'overlappe avec aucun autre ngram, on le garde
                                ngrams_with_no_overlap.append(x[i])
                    
    # 10/11/2018
    elif x != []:
    # else:
        # print (x)
        
        ngrams_with_no_overlap.append(x[0])

    return(ngrams_with_no_overlap)


def remove_ngrams_with_no_overlap(df): 
    all_ngrams_modified = []
#     print ("\n******** DEBUT **********")
#     print ("Le ngram qui ne s'overlappe avec aucun autre ngram est:", df['not_overlapped_entity_X_phrases'])
    
    if df['not_overlapped_entity_X_phrases'] != [] and df['all_entity_X_phrases'] != []:
        ngrams_not_overlaped = sorted([each for each in df['not_overlapped_entity_X_phrases']])
        ngrams_X_phrases = sorted([each for each in df['all_entity_X_phrases']])
    
        if ngrams_not_overlaped == ngrams_X_phrases:
            all_ngrams_modified = []
        else :
            for each in df['all_entity_X_phrases']:
                if each not in df['not_overlapped_entity_X_phrases']:
                    all_ngrams_modified.append(each)
            
    elif df['not_overlapped_entity_X_phrases'] == [] and df['all_entity_X_phrases'] != []:
        all_ngrams_modified = df['all_entity_X_phrases']
        
    return(all_ngrams_modified)

# 14/09/2018 : modification de la fonction "overlap_ngrams"
def overlap_ngrams(x):
    ngrams_with_overlap = []
    
    for i in range(len(x)):
#         print ("\n#####################################")
#         print (x[i][0])
        # On extrait tous les mots qui composent le ngram "x[i]"
    
        if len(x) > 1:
            words_i = word_tokenize(x[i])
#             print (words_i)
            intersection_temp = []
            cpt_no_overlap = 0
            for j in range(len(x)):

                if j!=i :
    #                 print ("\n Un autre ngram est :",x[j][0])
                    words_j = word_tokenize(x[j])
    #                 print (words_j)
                    intersection_words_i_j = [x for x in words_i if x in set(words_j)]

                    # On incrémente le compteur:
                    cpt_no_overlap += 1
                   
                    if intersection_words_i_j != []:
#                         print (intersection_words_i_j, "sont en communs")
    #                     print ("La valeur de cpt est : ",cpt_no_overlap)
    #                     print ("La valeur à atteindre est :",len(x) - 1)
#                         if intersection_words_i_j == ['jacques', 'prieur']:
#                             print (cpt_no_overlap)
#                             print ("len - 1",len(x) - 1)

#                         if x[i] == 'jacques prieur':
#                             print("TEST !!!", cpt_no_overlap)
#                             print("TEST !!!", intersection_words_i_j)
#                             print("TEST !!!", len(x) - 1)
                        intersection_temp.append(intersection_words_i_j)
                            
            if intersection_temp != [] and cpt_no_overlap == len(x) - 1:
                # Le ngram concerné ne s'overlappe avec aucun autre ngram, on le garde
#                 print ("ajout de", x[i])
                ngrams_with_overlap.append(x[i])

#                     else:
#                         print ("Présence de mots en commun !")
                        
#         else:
#             ngrams_with_no_overlap = x[i]
    return(ngrams_with_overlap)


def keep_ngrams_which_contains_others(x):
    ngrams_with_overlap = []

    for i in range(len(x)):
        cpt = 0
        for j in range(len(x)):
            if j!=i :
                if x[j] in x[i]:
                    cpt += 1
        if cpt == len(x) - 1:
            ngrams_with_overlap.append(x[i])
            
    return ngrams_with_overlap