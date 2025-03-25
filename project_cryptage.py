from crypto4 import *
from decrypto3 import *
from interface2 import *

#V1.0.

#chemin de depart
ch_dep = r"d:\Baptiste\Perso\CPE Prépa\TIPE crypto python" #doit etre choisis a partir de l'interface graphique

#doc a crypter
doc = r"d:\Baptiste\Perso\CPE Prépa\TIPE crypto python\antho.txt" #doit etre choisis a partir de l'interface graphique

choix = input("Choissisez si vous voulez crypter ou decrypter un fichier :")

#cryptage
if choix == "crypter" or choix == "cryptage" :
    #doc a crypter
    doc = r"d:\Baptiste\Perso\CPE Prépa\TIPE crypto python\antho.txt"

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

    