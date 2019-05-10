 # pattern_year = re.compile('\d{4}')
def list_entity_to_str(x):
    i = 0
    #     print (x)
    if x != []:
        for each in x:
            i += 1
            if i == 1:
                resultat = each
            else:
                resultat = resultat + '|' + each
    else:
        resultat = ''

    return resultat


def nodup_entities(x):
    resultat = []
    for each in x:
        if each not in resultat and each != '' and each != 'bio':
            resultat.append(each)

    return resultat

# def filter_confidence_score(x):
def no_filter_confidence_score(df):
    # global df_with_x_confidence_rate

    #     df_with_x_confidence_rate  = df_temp[df_temp['confidence_score'] >= x]
    df_with_x_confidence_rate  = df

    df_with_x_confidence_rate['str_result'] = df_with_x_confidence_rate['nodup_final_result_X_phrases_with_uppercase_and_guillemets_entity'].map(list_entity_to_str)
    df_with_x_confidence_rate['liste_id'] = df_with_x_confidence_rate['id'].apply(list)
        
    return df_with_x_confidence_rate