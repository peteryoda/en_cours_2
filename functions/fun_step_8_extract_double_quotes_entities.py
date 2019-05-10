import re

# from functions import fun_data_cleansing as fd
def extract_remove_guillemets(x):
    resultat = []
    #     pattern_guillemets = r'(\"[a-z]+\")|(\"[a-z]+)|([a-z]+\")'
    #     for each in x:
    #         temp = re.findall(pattern_guillemets,each)
            
    #         if temp != []:
    #             for each in temp:
    #                 for element in each:
    #                     if element != '':
    #                         print (element)
    #                         resultat.append(element)

    #     finalement on enlève les guillemets
    for each in x:
    #         print (each)
        each_without_guillemet =  re.sub('"','',each)
        resultat.append(each_without_guillemet)
    return resultat

def test_presence_words_guillemets(df):
    words_to_remove = []
    flag_presence_word = False
    # Nb de mots présents dans "words_title_uppercase_without_stopwords"
    #     nb_words_in_words_title_uppercase_without_stopwords = len(df['words_title_uppercase_without_stopwords'])
    nb_words_in_words_title_uppercase_without_stopwords = len(df['title_splitted_guillemets'])
    words_count = 0
    #     for word in df['words_title_uppercase_without_stopwords']:
    for word in df['words_title_guillemets']:
    #         print (word)
        if word in df['temp_entity_without_guillemets']:
            words_count += 1
                # print (word)
            words_to_remove.append(word)
        elif word in df['temp_entity_without_guillemets'] and words_count == nb_words_in_words_title_uppercase_without_stopwords:
                # print (word)
                # print ("\n")
            words_to_remove.append(word)
            
    return words_to_remove


def add_real_entity_guillemets(df):

    if df['title_splitted_guillemets'] !=  [] :
            
        if df['temp_words_guillemets'] !=  []:
            
            if df['temp_entity_without_guillemets']  !=  []:
                    
                # Enlever dans "final_result_X_phrases_bis" les mots contenus dans les entités à ajouter
                temp = [word for word in df['temp_entity_without_guillemets']]
                for each in df['temp_words_guillemets']:
                        
                    for element in temp:
                        if each == element:
                            # print ("Suppression de :",each, "dans :",temp)
                            temp.remove(each)
                
                # Ajouter les entités
    #                 print (temp)
                resultat = temp

                for each in df['title_splitted_guillemets']:
    #                     print ("CAS 1 : ajout de ", each,"a ",resultat,"\n")
                    resultat.append(each)
                    
    #             else:
    #                 for each in df['title_uppercase_without_stopwords']:
    #                     resultat = []
    #                     print ("CAS 2 : ajout de ", each,"a ",resultat,"\n")
    #                     resultat.append(each)
                    
        else:
            temp = [word for word in df['temp_entity_without_guillemets']]
            resultat = temp
            for each in df['title_splitted_guillemets']:
    #                 print ("CAS 3 : ajout de ", each,"a ",resultat,"\n")
                    resultat.append(each)
                       
    else:
        resultat = df['temp_entity_without_guillemets']

    return resultat