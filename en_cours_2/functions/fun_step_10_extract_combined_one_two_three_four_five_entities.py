import itertools

def extraction_one_entity(x):
    resultat = []
    for each in x.split('|'):
        if each != []:
            resultat.append(each)
    return resultat

def extraction_two_entities(x):
    resultat = list(itertools.combinations(x, 2))
    return resultat

def extraction_three_entities(x):
    resultat = list(itertools.combinations(x, 3))
    return resultat

def extraction_four_entities(x):
    resultat = list(itertools.combinations(x, 4))
    return resultat

def extraction_five_entities(x):
    resultat = list(itertools.combinations(x,5))
    return resultat

