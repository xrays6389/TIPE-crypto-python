from cryptography.fernet import Fernet 
import os

#V1.3
#Modification afin d'utiuliser la fonction cryptage depuis un autre documents
'''
- faire en sorte de pouvoir crypter plusieurs documents 
    *le fichier contenant les clés doit pouvoir etre parcouru pour trouver la bonne clé
'''

def cryptage(doc,ch_dep): 
    
     # Génération et sauvegarde de la clé
    key = Fernet.generate_key()
    with open(os.path.join(ch_dep, "key.key"), "wb") as key_file:
        key_file.write(key)

    #recupere le fichier a crypter et l'encode en bytes
    with open(doc, "r", encoding="utf-8") as file:
        contenu = file.read().encode()  # Encodage en bytes ('.encode'=>transforme les caracteres en bytes)

    #cryptage du document
    fernet = Fernet(key)
    crypt=Fernet(key).encrypt(contenu) #crypte seulement des bytes

    # Écriture dans un nouveau fichier
    fichier_out = doc
    chemin = os.path.join(ch_dep, doc) #permet d'enregistrer le fichier à l'emplacement voulu
    with open(chemin, "wb") as file:
        file.write(crypt)

    #permet d'ajouter un suffixe au fichier crypté

    #marche pas a regarder 
    suffixe = "_crypt" 
    base, ext = os.path.splitext(fichier_out)
    out = base + suffixe + ext

    return out
