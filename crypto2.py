from cryptography.fernet import Fernet
import os

#V1.1
#Version qui ecrase le contenu dans le fichier en le remplacant par le contenu crypté
'''
Chose a faire :
-interface graphique
    *pouvoir choisir le fichier a crypter
    *pouvoir choisir le chemin d'enregistrement du fichier crypté ainsi que du fichier contenant
     les clés

- faire en sorte de pouvoir crypter plusieurs documents 
    *le fichier contenant les clés doit pouvoir etre parcouru pour trouver la bonne clé
'''

def cryptage(doc): 
     # Génération et sauvegarde de la clé
    key = Fernet.generate_key()
    with open(r"d:\Baptiste\Perso\CPE Prépa\TIPE crypto python\key.key", "ab") as key_file:
        key_file.write(key)

    #recupere le fichier a crypter et l'encode en bytes
    with open(doc, "r", encoding="utf-8") as file:
        contenu = file.read().encode()  # Encodage en bytes ('.encode'=>transforme les caracteres en bytes)

    #cryptage du document
    fernet = Fernet(key)
    crypt=Fernet(key).encrypt(contenu) #crypte seulement des bytes

    # Écriture dans un nouveau fichier
    fichier_out = doc
    chemin = os.path.join(r"d:\\Baptiste\\Perso\\CPE Prépa\\TIPE crypto python", doc) #permet d'enregistrer le fichier à l'emplacement voulu
    with open(chemin, "wb") as file:
        file.write(crypt)

    #permet d'ajouter un suffixe au fichier crypté

    #marche pas a regarder 
    suffixe = "_crypt" 
    base, ext = os.path.splitext(fichier_out)
    out = base + suffixe + ext

    return out


doc = r"d:\Baptiste\Perso\CPE Prépa\TIPE crypto python\test2.txt"

#permet de verifier que le fichier est bien trouvé par le programme
with open(doc, "r", encoding="utf-8") as file:
    contenu = file.read()
    print("Fichier trouvé et ouvert avec succès !")

#doc = input("Nom_fichier.txt :")
doc = doc.strip()
doc = cryptage(doc)
print (doc)