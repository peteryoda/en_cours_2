

def strip_and_lower_title_splitted_uppercase(x):
    resultat = []
    # print (x)
    for each in x:
        resultat.append((each.strip()).lower())
        
    return resultat

def split_title_splitted_uppercase(x):
    resultat = []
    for each in x:
        list_of_words = each.split(' ')
        for word in list_of_words:
            resultat.append(word)
            
    return resultat

def test_presence_words(df):
    words_to_remove = []
    flag_presence_word = False
    # Nb de mots présents dans "words_title_uppercase_without_stopwords"
    # nb_words_in_words_title_uppercase_without_stopwords = len(df['words_title_uppercase_without_stopwords'])
    nb_words_in_words_title_uppercase_without_stopwords = len(df['words_title_uppercase'])
    words_count = 0
    #     for word in df['words_title_uppercase_without_stopwords']:
    for word in df['words_title_uppercase']:
    #         print (df['final_result_X_phrases_bis'])
    #         if word in df['final_result_X_phrases_bis']:
        for entity in df['final_result_X_phrases_bis']:
            if word in entity.split(' '):
    #                 print(word)
                words_count += 1
                words_to_remove.append(word)
    #             elif word in df['final_result_X_phrases_bis'] and words_count == nb_words_in_words_title_uppercase_without_stopwords:
    #                 words_to_remove.append(word)
            elif  word in entity.split(' ') and words_count == nb_words_in_words_title_uppercase_without_stopwords:
                words_to_remove.append(word)
        
    return words_to_remove


def add_real_entity_uppercase(df):

    if df['title_splitted_uppercase'] !=  [] :
            
        if df['temp_words'] !=  []:
            
            if df['final_result_X_phrases_bis']  !=  []:
                    
                     # Enlever dans "final_result_X_phrases_bis" les mots contenus dans les entités à ajouter
                temp = [entity for entity in df['final_result_X_phrases_bis']]
                for each in df['temp_words']:
                    for element in temp:
    #                         24/02/2019 : correction
    #                         if each == element:
    #                         if each in element:
                        if each in element.split(' '):
    #                             24/02/2019 : correction
    #                             temp.remove(each)
    #                             print ("each", each, "et element", element)
                            temp.remove(element)
                
                    # Ajouter les entités
    #                 print (temp)
                resultat = temp

                for each in df['title_splitted_uppercase']:
    #                     print ("CAS 1 : ajout de ", each,"a ",resultat,"\n")
                    resultat.append(each)
                    
    #             else:
    #                 for each in df['title_uppercase_without_stopwords']:
    #                     resultat = []
    #                     print ("CAS 2 : ajout de ", each,"a ",resultat,"\n")
    #                     resultat.append(each)
                    
        else:
            temp = [entity for entity in df['final_result_X_phrases_bis']]
            resultat = temp
            for each in df['title_splitted_uppercase']:
    #                 print ("CAS 3 : ajout de ", each,"a ",resultat,"\n")
                resultat.append(each)
                       
    else:
    #         resultat = [word for word in df['final_result_X_phrases_bis']]
    #         print(df['title_splitted_uppercase'], "et", df['final_result_X_phrases_bis'])
        resultat = df['final_result_X_phrases_bis']
    #     print ("resultat: ", resultat)
            
    return resultat