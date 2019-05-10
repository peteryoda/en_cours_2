def list_of_slugs(df):
    temp = []
    resultat = []
    temp.append(df['slug_one'])
    temp.append(df['slug_two'])
    resultat.append(temp)
    return resultat

def split_into_words(x):
    temp_0 = []
    for each in x:
        for word in x[0][0].split('-'):
            temp_0.append(word)
        for word in x[0][1].split('-'):
            temp_0.append(word)
    temp = sorted(temp_0)
        
    resultat = ''
    for each in temp:
        resultat += each
      
    return resultat

def create_couples(df):
        
    couples = []
    temp_1 = []
    temp_1.append(df['slug_x'])
    temp_1.append(df['distributeur_x'])
    temp_1.append(df['xbrand_x'])
    temp_1.append(df['xtitle_x'])
    temp_1.append('1.0')
        
    temp_2 = []
    temp_2.append(df['slug_y'])
    temp_2.append(df['distributeur_y'])
    temp_2.append(df['xbrand_y'])
    temp_2.append(df['xtitle_y'])
    temp_2.append('1.0')
        
    couples.append(temp_1)
    couples.append(temp_2)
        
    return couples

# 15/04/2019 : nouvelles fonctions pour restituer 
#   des couples valides ie il existe un unique couple qui matche
#   pour chaque combinaison "distibuteur_one" x "distributeur_two"

def slug_one_transform(df):
    
    if (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'ntr' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'gwz'):
        resultat = df['slug_two']
    else:
        resultat = df['slug_one'] 
    return resultat

def slug_two_transform(df):
    if (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'ntr' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'gwz'):
        resultat = df['slug_one']
    else:
        resultat = df['slug_two']
    return resultat

def xtitle_one_transform(df):
    if (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'ntr' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'gwz'):
        resultat = df['xtitle_two']
    else:
        resultat = df['xtitle_one']
    return resultat

def xtitle_two_transform(df):
    if (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'ntr' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'gwz'):
        resultat = df['xtitle_one']
    else:
        resultat = df['xtitle_two']
    return resultat

def distributeur_one_transform(df):
    if (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'ntr' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'gwz'):
        resultat = df['distributeur_two']
    else:
        resultat = df['distributeur_one']
    return resultat

def distributeur_two_transform(df):
    if (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'ntr' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'gwz'):
        resultat = df['distributeur_one']
    else:
        resultat = df['distributeur_two']
    return resultat

def brand_one_transform(df):
    if (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'ntr' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'gwz'):
        resultat = df['brand_two']
    else:
        resultat = df['brand_one']    
    return resultat

def brand_two_transform(df):
    if (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'ntr' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'gwz'):
        resultat = df['brand_one']
    else:
        resultat = df['brand_two']
    return resultat

def breadcrumb_one_transform(df):
    if (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'ntr' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'gwz'):
        resultat = df['breadcrumb_two']
    else:
        resultat = df['breadcrumb_one']  
    return resultat

def breadcrumb_two_transform(df):
    if (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'ntr' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'gwz'):
        resultat = df['breadcrumb_one']
    else:
        resultat = df['breadcrumb_two']
    return resultat

def price_one_transform(df):
    if (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'ntr' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'gwz'):
        resultat = df['price_two']
    else:
        resultat = df['price_one']
    return resultat

def price_two_transform(df):
    if (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'ntr' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'gwz'):
        resultat = df['price_one']
    else:
        resultat = df['price_two']
    return resultat

def url_one_transform(df):
    if (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'ntr' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'gwz'):
        resultat = df['URL_two']
    else:
        resultat = df['URL_one']  
    return resultat

def url_two_transform(df):
    if (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'ntr' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'crf') or (df['distributeur_one'] == 'gwz' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'ntr') or (df['distributeur_one'] == 'wbe' and df['distributeur_two'] == 'gwz'):
        resultat = df['URL_one']
    else:
        resultat = df['URL_two']
    return resultat