from crypto5 import *
from decrypto4 import *
from interface3 import *

#V1.1

#chemin de depart
ch_dep = choisir_dossier()

#doc a crypter
doc = choisir_fichier()

crypt = window_crypt(doc, ch_dep)

#choix = input("Choissisez si vous voulez crypter ou decrypter un fichier :")


"""
#cryptage
if choix == "crypter" or choix == "cryptage" :

    #permet de verifier que le fichier est bien trouvé par le programme
    with open(doc, "r", encoding="utf-8") as file:
        contenu = file.read()
        print("Fichier trouvé et ouvert avec succès !")

    #chiffrement
    doc = doc.strip()
    doc = cryptage(doc,ch_dep)
    print (doc)

#decryptage 
elif choix == "decrypter" or choix == "decryptage" :
    # Chargement de la clé
    key = load_key(ch_dep)

    # Nom du fichier crypté
    fichier_crypté = "antho.txt"  #doit etre choisis a partir de l'interface graphique

    #permet de verifier que le fichier est bien trouvé par le programme
    with open(doc, "r", encoding="utf-8") as file:
        contenu = file.read()
        print("Fichier trouvé et ouvert avec succès !")

    # Déchiffrement du fichier
    fichier_decrypte = decrypto(fichier_crypté, ch_dep, key)
    print(f"Fichier déchiffré sauvegardé sous : {fichier_decrypte}")
"""
    