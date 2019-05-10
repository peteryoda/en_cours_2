# Pour extraire les "chunks" 
from pattern.fr import parsetree

# Déf de la fonction qui extrait les chunks
def X_phrases_extraction(x):
    resultat = []
    s = parsetree(x)
    for sentence in s:
        for chunk in sentence.chunks:
    #        print (chunk.words)
            resultat.append([chunk.type, ' '.join([w.string for w in chunk.words])])
    return resultat
